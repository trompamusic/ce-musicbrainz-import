import requests_cache
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError
from wikidata.client import Client
from urllib.parse import urlparse

from requests.adapters import HTTPAdapter

session = requests_cache.CachedSession()
adapter = HTTPAdapter(max_retries=5)
session.mount("https://", adapter)
session.mount("http://", adapter)


class WikipediaException(Exception):
    pass


def load_person_from_wikidata_url(wikidata_url):

    # TODO: Description, multiple versions for different languages
    # TODO: og:title, og:description, og:image,

    entity = get_entity_for_wikidata(wikidata_url)
    label = entity.label.get('en')
    if label:
        title = f"{label} - Wikidata"
        description = entity.description.get('en')
        return {
            "title": title,
            "name": label,
            "description": description,
            "contributor": "https://wikidata.org",
            "source": wikidata_url,
            "format_": "text/html"
        }
    else:
        return {}


def load_person_from_wikipedia_wikidata_url(wikidata_url, language):
    """Given a wikidata url, get information from wikipedia
    TODO: Allow a wikipedia URL as argument too
    TODO: Check language against valid list
    TODO: Image from wikipedia is different to that of wikidata"""

    entity = get_entity_for_wikidata(wikidata_url)

    wikipedia_url = get_url_for_wikipedia(entity, language)
    # TODO: Remove html tags from the description
    description = get_description_for_wikipedia(entity, language)
    label = entity.label.get(language)
    if label:
        title = f"{label} - Wikipedia"

        return {
            "title": title,
            "name": label,
            "description": description,
            "contributor": "https://wikipedia.org/",
            "source": wikipedia_url,
            "format_": "text/html",
            "language": language
        }
    else:
        return {}


def load_person_from_wikipedia_url(wikipedia_url, language):
    """Given a wikipedia url, get information from wikipedia
    TODO: Check language against valid list
    TODO: Image from wikipedia is different to that of wikidata"""
    try:
        page = get_page_for_wikipedia(wikipedia_url)
    except (DisambiguationError, PageError) as e:
        return None

    label = page.title
    description = page.summary

    if label:
        title = f"{label} - Wikipedia"

        return {
            "title": title,
            "name": label,
            "description": description,
            "contributor": "https://wikipedia.org/",
            "source": wikipedia_url,
            "format_": "text/html",
            "language": language
        }
    else:
        return {}


def _get_normalized_query(data, query):
    """If you query with an _ in a query (e.g. from a wikipedia url, then wikipedia will "normalize" it,
    so that it doesn't have the _ or other characters in it"""
    normalized = data.get("query", {}).get("normalized")
    if normalized:
        for n in normalized:
            if n["from"] == query:
                return n["to"]

    return query


def parse_description_from_wikipedia_response(title, data):
    pages = data.get("query", {}).get("pages")
    title = _get_normalized_query(data, title)
    for pid, pdata in pages.items():
        if pdata["title"] == title:
            return pdata["extract"]
    return ""


def get_wikidata_id_from_wikipedia_url(wp_url):
    """Get the wikidata id for this URL if it exists
    Returns None if the page has no wikidata id"""

    if "en.wikipedia.org" not in wp_url:
        raise WikipediaException("Can only use en.wikipedia.org urls")
    parts = urlparse(wp_url)
    # Remove /wiki/
    # some titles may have / in them so we can't take the last part after splitting on /
    wp_title = "/".join(parts[2:])
    param_url = "https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&titles={}&format=json"
    full_url = param_url.format(wp_title)
    r = session.get(full_url)
    data = r.json()
    title = _get_normalized_query(data, wp_title)
    pages = data.get("query", {}).get("pages")
    for pid, pdata in pages.items():
        if pdata["title"] == title:
            return pdata.get("pageprops", {}).get("wikibase_item")
    return None


def get_description_from_wikipedia_url(wp_url):
    if "en.wikipedia.org" not in wp_url:
        raise WikipediaException("Can only use en.wikipedia.org urls")
    parts = urlparse(wikidata_url)
    # Remove /wiki/
    # some titles may have / in them so we can't take the last part after splitting on /
    wp_title = "/".join(parts[2:])
    return get_description_from_wikipedia(wp_title)


def get_description_from_wikipedia(title):
    desc_url = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=1&format=json&redirects=1&titles={}"
    full_url = desc_url.format(title)

    r = session.get(full_url)
    data = r.json()
    return parse_description_from_wikipedia_response(title, data)


def get_entity_for_wikidata(wikidata_url):
    parts = urlparse(wikidata_url)
    wd_id = parts.path.split("/")[-1]
    c = Client()
    entity = c.get(wd_id, load=True)
    return entity


def get_url_for_wikipedia(wd_entity, language):
    sitelinks = wd_entity.attributes.get("sitelinks", {})
    wikicode = f"{language}wiki"
    wiki = sitelinks.get(wikicode, {})
    url = wiki.get("url")
    return url


def get_description_for_wikipedia(wd_entity, language):
    sitelinks = wd_entity.attributes.get("sitelinks", {})
    wikicode = f"{language}wiki"
    wiki = sitelinks.get(wikicode, {})
    title = wiki.get("title")

    return get_description_from_wikipedia(title)


def get_page_for_wikipedia(wikipedia_url):
    parts = urlparse(wikipedia_url)
    wp_name = parts.path.split("/")[-1].replace("_", " ")
    page = wikipedia.page(wp_name)

    return page
