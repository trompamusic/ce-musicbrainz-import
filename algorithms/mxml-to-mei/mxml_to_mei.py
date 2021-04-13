"""
Given a MediaObject node that refers to a musixml file (from cpdl or imslp), download it,
convert it to mei using verovio, and create a new MediaObject node

If the file is an imslp zip, the musicxml file is extracted first. If the file is a .mxl
(compressed zip), the .xml file inside the zip is extracted.

The new node is linked to the work (exampleOfWork), and the musicxml file (derivedFrom)

TODO: we assume that the basename of all files is unique. Should we use a uuid instead? or a prefix
TODO: Need to check that the file doesn't already exist before creating it
TODO: Duplicate imslp access methods in other algorithms. Can these be factored out?
"""

import io
import os
import sys
import tempfile
import zipfile
from urllib.parse import urlparse, urlunparse

import boto3
import click
import requests
import verovio
from trompace.config import config
from trompace.connection import submit_query
from trompace.mutations import mediaobject
import trompace.mutations.application as mutations_application
import trompace.queries.application as queries_application
from trompace.queries.mediaobject import query_mediaobject


config.load()

ACCESS_KEY = os.environ['S3_ACCESS_KEY']
SECRET_KEY = os.environ['S3_SECRET_KEY']
S3_HOST = os.environ['S3_HOST']
S3_BUCKET = 'meiconversion'
# This is an s3 policy for a bucket called 'meiconversion' that allows anyone to download items from it
S3_POLICY = '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"AWS":["*"]},"Action":["s3:GetBucketLocation","s3:ListBucket"],"Resource":["arn:aws:s3:::meiconversion"]},{"Effect":"Allow","Principal":{"AWS":["*"]},"Action":["s3:GetObject"],"Resource":["arn:aws:s3:::meiconversion/*"]}]}'


def get_or_create_verovio_application():
    tk = verovio.toolkit()
    version = tk.getVersion()
    creator = "https://github.com/trompamusic/ce-data-import/tree/master/algorithms/mxml-to-mei"
    source = "https://www.verovio.org"

    query_application = queries_application.query_softwareapplication(
        creator=creator,
        source=source,
        softwareversion=version
    )
    app_response = submit_query(query_application, auth_required=True)
    app = app_response.get('data', {}).get('SoftwareApplication', [])
    if app:
        return app[0]["identifier"]
    else:
        mutation_create = mutations_application.mutation_create_application(
            name="Verovio",
            contributor="https://www.verovio.org",
            creator=creator,
            source=source,
            language="en",
            title="Verovio",
            softwareversion=version
        )
        create_response = submit_query(mutation_create, auth_required=True)
        app = create_response.get('data', {}).get('CreateSoftwareApplication', {})
        return app["identifier"]


def imslp_file_url_to_download_url(file_url):
    """Take a MediaWiki File: page (e.g. File:PMLP129863-HandAbO.zip)
    and use the mediawiki api to get the actual URL of the file"""

    params = {"action": "query",
              "prop": "imageinfo",
              "titles": file_url,
              "format": "json",
              "iiprop": "url"}
    url = 'https://imslp.org/api.php'

    r = requests.get(url, params=params)
    r.raise_for_status()
    try:
        j = r.json()
    except ValueError:
        return []

    pages = j['query']['pages']
    for k, v in pages.items():
        info = v.get('imageinfo')
        if info:
            if file_url in info[0]["descriptionurl"]:
                return "https:" + info[0]["url"]


def uncompress_mxl_to_xml(mxl_file):
    """an mxl is a zip file that contains a manifest and the actual xml file."""
    with zipfile.ZipFile(mxl_file) as zipfp:
        names = zipfp.namelist()
        xmlnames = [n for n in names if "/" not in n and n.lower().endswith(".xml")]
        if len(xmlnames) == 0:
            raise ValueError("Cannot find any xml file")
        elif len(xmlnames) > 1:
            raise ValueError("Found more than one xml in the root?")
        else:
            return zipfp.read(xmlnames[0]).decode("utf-8")


def convert_mxml_to_mei_file(inputdata, inputname):
    # TODO: If it's compressed, need to undo it (current version of verovio doesn't support mxl)

    if inputname.endswith(".mxl"):
        data = uncompress_mxl_to_xml(inputdata)
    else:
        data = inputdata

    tk = verovio.toolkit()
    tk.loadData(data)
    mei = tk.getMEI('')
    return mei


def upload_mei_to_s3(meidata, filename):
    client = boto3.client(
        's3',
        endpoint_url=S3_HOST,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )

    try:
        client.create_bucket(Bucket=S3_BUCKET)
        client.put_bucket_policy(Policy=S3_POLICY, Bucket=S3_BUCKET)
    except client.exceptions.BucketAlreadyOwnedByYou:
        pass
    client.upload_fileobj(meidata, S3_BUCKET, filename)

    file_path = os.path.join(S3_BUCKET, filename)
    host_parsed = list(urlparse(S3_HOST))
    host_parsed[2] = file_path

    return urlunparse(host_parsed)


def find_existing_mei(expected_filename):
    pass


def create_mei_node(meiurl):
    filename = os.path.basename(meiurl)

    imslp_mei = mediaobject.mutation_create_media_object(
        creator="https://github.com/trompamusic/ce-data-import/tree/master/algorithms/mxml-to-mei",
        # Who this data came from
        contributor="https://trompamusic.eu",
        # URL on the web that matches contentUrl
        source=meiurl,
        # The <title> of `source`
        title=filename,
        # The mimetype of `source`
        format_="application/mei+xml",
        name=filename,
        # The page that describes the resource
        url=meiurl,
        contenturl=meiurl,
        encodingformat="application/mei+xml"
    )
    mei_response = submit_query(imslp_mei, auth_required=True)
    mei = mei_response.get('data', {}).get('CreateMediaObject', {})
    if mei:
        return mei["identifier"]
    else:
        return None


def join_existing_and_new_mei(musiccomposition_id, mxml_mo_id, mei_mo_id):
    """
    # All of the MediaObjects are examples of the MusicComposition
    example_of_work_pdf = mediaobject.mutation_merge_mediaobject_example_of_work(pdf_id, work_identifier=work_id)
    # In the case of CPDL, we know that scores are written in an editor and then rendered to PDF.
    # Therefore, the PDF wasDerivedFrom the xml (http://www.w3.org/ns/prov#wasDerivedFrom)
    pdf_derived_from_xml = mediaobject.mutation_merge_media_object_wasderivedfrom(pdf_id, xml_id)

    application created by:
    mutation_add_actioninterface_result
    """

    application_id = get_or_create_verovio_application()
    example_mutation = mediaobject.mutation_merge_mediaobject_example_of_work(mei_mo_id, work_identifier=musiccomposition_id)
    submit_query(example_mutation, auth_required=True)
    derivedfrom_mutation = mediaobject.mutation_merge_media_object_wasderivedfrom(mei_mo_id, mxml_mo_id)
    submit_query(derivedfrom_mutation, auth_required=True)
    used_mutation = mediaobject.mutation_add_media_object_used(mei_mo_id, application_id)
    submit_query(used_mutation, auth_required=True)


def process_cpdl(file_url):
    r = requests.get(file_url)
    file_content = io.BytesIO(r.content)
    mei_content = convert_mxml_to_mei_file(file_content, file_url)

    parsed = urlparse(file_url)
    original_name = os.path.basename(parsed.path)
    original_parts = os.path.split(original_name)
    mei_filename = original_parts[0] + ".mei"

    mei_fp = io.BytesIO(mei_content.encode("utf-8"))
    mei_url = upload_mei_to_s3(mei_fp, mei_filename)
    mei_id = create_mei_node(mei_url)

    return mei_id


def find_imslp_download_url(imslp_file):
    cookie = {"imslpdisclaimeraccepted": "yes"}
    r = requests.get(download_url, cookies=cookie)
    zipfp = io.BytesIO(r.content)


def convert_ce_node(mediaobject_id, temporary_dir):
    """Take a MediaObject
    Ensure that encodingFormat is one of the musicxml ones
    - if the contenturl is a content url, then find it (special-case imslp), otherwise just download it
    - do conversion
    - create mediaobject, link to input file, link to composition, upload to s3"""

    return_items = ["identifier", "name", "contributor", "url", "contentUrl", {"exampleOfWork": ["identifier"]}]
    mo_query = query_mediaobject(identifier=mediaobject_id, return_items=return_items)
    mo_response = submit_query(mo_query)
    mo = mo_response.get('data', {}).get('MediaObject', [])
    if mo:
        mo = mo[0]
        mo_id = mo['identifier']
        mo_contributor = mo['contributor']
        mo_contenturl = mo['contentUrl']
        mo_url = mo['url']
        work = mo['exampleOfWork']
        if not work:
            print('Unexpectedly this MediaObject has no exampleOfWork', file=sys.stderr)
        work_id = work[0]['identifier']

        if mo_contributor == "https://cpdl.org":
            mei_id = process_cpdl(mo_contenturl)
        elif mo_contributor == "https://imslp.org":
            mei_id = process_imslp(mo_url, temporary_dir)
        else:
            print("Contributor isn't one of cpdl or imslp", file=sys.stderr)
            return
        join_existing_and_new_mei(musiccomposition_id=work_id, mxml_mo_id=mo_id, mei_mo_id=mei_id)


@click.group()
def cli():
    pass


@cli.command("convert-mxml-to-mei-node")
@click.argument("mediaobject_id")
def convert_mxml_to_mei_node_command(mediaobject_id):
    """0c297551-6a77-47a5-aa18-b8b114d64691"""
    with tempfile.TemporaryDirectory() as tmpdir:
        convert_ce_node(mediaobject_id, tmpdir)


@cli.command("convert-mxml-to-mei-file")
@click.argument("inputpath")
@click.argument("outputpath")
def convert_mxml_to_mei_file_command(inputpath, outputpath):
    convert_mxml_to_mei_file(inputpath, outputpath)


if __name__ == '__main__':
    cli()
