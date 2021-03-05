"""Trompa Base model

While the schema.org types and properties are mainly to provide semantic
structure to the data in the CE, the metadata properties are there to provide
for global searches on the basis of search terms. For this reason, all metadata
properties accept scalar type values only.
Any node in the CE represents a web resource. A node’s metadata properties
contain information about either the web resource itself, or about a thing
(real or abstract) or the file that this web resource is about.

https://docs.google.com/document/d/1MBocgsTFcJufvjZXA6PY8bUitkxEIaSKD1lJZf9PToM/edit#heading=h.gnaz5jmaxplv
"""

from dataclasses import dataclass
from datetime import date


@dataclass
class CE_BaseModel():
    """
    Trompa Base model

    Attributes
    ----------
    identifier
        UUID
        An unambiguous reference to the resource within a given context.
        For CE we will use UUID.
        An invalid or non-unique UUID will fail validation.
        If no UUID is passed, one will be generated by the CE (recommended).
    contributor
        Text (Mandatory)
        A person, an organization, or a service responsible for contributing
        the artist to the web resource. This can be either a name or a base
        URL.
    source
        URL
        Url refering to the source
    coverage
        Text
        The spatial or temporal topic of the resource, the spatial
        applicability of the resource, or the jurisdiction under which the
        resource is relevant.
    creator: String!
        Text (Mandatory)
        The person, organization or service who created the thing the web
        resource is about.
    date
        _Neo4jDate
        A point in time associated with an event in the lifecycle of the
        resource. Accepts a date type, year(int) or list with [year, month,
        date] where month and date are optional.
    format
        Text (Mandatory)
        Format the resource is represented in.
    language
        AvailableLanguage
        The language the metadata is written in. Currently supported languages
        are en,es,ca,nl,de,fr.
    publisher
        Text
        The person, organization or service responsible for making the artist
        information available.
    relation
        Text
        A related resource. Any web resource can be used as a relation.
    rights
        Text
        The applicable rights for the resource.
    subject
        Text
        Resource type of the referenced object.
    title
        Text
        Title for the resource.
    description
        Text
        An account of the resource.
        Description may include but is not limited to: an abstract, a table of
        contents, a graphical representation, or a free-text account of the
        resource.
    _type
        Text
        The String scalar type represents textual data, represented as UTF-8
        character sequences. The String type is most often used by GraphQL to
        represent free-form human-readable text.
    _searchScore
        Float
        The Float scalar type represents signed double-precision fractional
        values as specified by IEEE 754.
    """

    def __init__(self, identifier: str, name: str, url: str, contributor: str, creator: str):
        self.identifier = identifier
        self.name = name
        self.title = name
        self.url = url
        self.contributor = contributor
        self.source = url
        self.creator = creator
        self.date = date.today()

    identifier: str = None
    name: str = None
    url: str = None
    source: str = None
    contributor: str = None
    creator: str = None
    coverage: str = None
    date = None
    format: str = "text/html"
    language: str = "en"
    publisher: str = None
    relation: str = None
    rights: str = None
    subject: str = None
    title: str = None
    description: str = None
    _type: str = None
    _searchScore: float = None
