"""The schema.org Organization model.

For reference see schema.org: https://schema.org/Organization
"""

from dataclasses import dataclass

from . import Thing


@dataclass
class Organization(Thing):
    """
    The schema.org Organization model

    Attributes
    ----------
    actionableFeedbackPolicy
        CreativeWork or URL
        For a NewsMediaOrganization or other news-related Organization, a
        statement about public engagement activities (for news media, the
        newsroom’s), including involving the public - digitally or otherwise --
        in coverage decisions, reporting and activities after publication.
    address
        PostalAddress or Text
        Physical address of the item.
    aggregateRating
        AggregateRating
        The overall rating, based on a collection of reviews or ratings, of the
        item.
    alumni
        Person
        Alumni of an organization.
        Inverse property: alumniOf.
    areaServed
        AdministrativeArea or GeoShape or Place or Text
        The geographic area where a service or offered item is provided.
        Supersedes serviceArea.
    award
        Text
        An award won by or for this item. Supersedes awards.
    brand
        Brand or Organization
        The brand(s) associated with a product or service, or the brand(s)
        maintained by an organization or business person.
    contactPoint
        ContactPoint
        A contact point for a person or organization. Supersedes contactPoints.
    correctionsPolicy
        CreativeWork or URL
        For an Organization (e.g. NewsMediaOrganization), a statement
        describing (in news media, the newsroom’s) disclosure and correction
        policy for errors.
    department
        Organization
        A relationship between an organization and a department of that
        organization, also described as an organization (allowing different
        urls, logos, opening hours). For example: a store with a pharmacy, or a
        bakery with a cafe.
    dissolutionDate
        Date
        The date that this organization was dissolved.
    diversityPolicy
        CreativeWork or URL
        Statement on diversity policy by an Organization e.g. a
        NewsMediaOrganization. For a NewsMediaOrganization, a statement
        describing the newsroom’s diversity policy on both staffing and
        sources, typically providing staffing data.
    diversityStaffingReport
        Article or URL
        For an Organization (often but not necessarily a
        NewsMediaOrganization), a report on staffing diversity issues. In a
        news context this might be for example ASNE or RTDNA (US) reports, or
        self-reported.
    duns
        Text
        The Dun & Bradstreet DUNS number for identifying an organization or
        business person.
    email
        Text
        Email address.
    employee
        Person
        Someone working for this organization. Supersedes employees.
    ethicsPolicy
        CreativeWork or URL
        Statement about ethics policy, e.g. of a NewsMediaOrganization
        regarding journalistic and publishing practices, or of a Restaurant, a
        page describing food source policies. In the case of a
        NewsMediaOrganization, an ethicsPolicy is typically a statement
        describing the personal, organizational, and corporate standards of
        behavior expected by the organization.
    event
        Event
        Upcoming or past event associated with this place, organization, or
        action. Supersedes events.
    faxNumber
        Text
        The fax number.
    founder
        Person
        A person who founded this organization. Supersedes founders.
    foundingDate
        Date
        The date that this organization was founded.
    foundingLocation
        Place
        The place where the Organization was founded.
    funder
        Organization or Person
        A person or organization that supports (sponsors) something through
        some kind of financial contribution.
    globalLocationNumber
        Text
        The Global Location Number (GLN, sometimes also referred to as
        International Location Number or ILN) of the respective organization,
        person, or place. The GLN is a 13-digit number used to identify parties
        and physical locations.
    hasCredential
        EducationalOccupationalCredential
        A credential awarded to the Person or Organization.
    hasMerchantReturnPolicy
        MerchantReturnPolicy
        Indicates a MerchantReturnPolicy that may be applicable. Supersedes
        hasProductReturnPolicy.
    hasOfferCatalog
        OfferCatalog
        Indicates an OfferCatalog listing for this Organization, Person, or
        Service.
    hasPOS
        Place
        Points-of-Sales operated by the organization or person.
    interactionStatistic
        InteractionCounter
        The number of interactions for the CreativeWork using the WebSite or
        SoftwareApplication. The most specific child type of InteractionCounter
        should be used. Supersedes interactionCount.
    isicV4
        Text
        The International Standard of Industrial Classification of All Economic
        Activities (ISIC), Revision 4 code for a particular organization,
        business person, or place.
    knowsAbout
        Text or Thing or URL
        Of a Person, and less typically of an Organization, to indicate a topic
        that is known about - suggesting possible expertise but not implying it.
        We do not distinguish skill levels here, or relate this to educational
        content, events, objectives or JobPosting descriptions.
    knowsLanguage
        Language or Text
        Of a Person, and less typically of an Organization, to indicate a known
        language. We do not distinguish skill levels or reading/writing/
        speaking/signing here. Use language codes from the IETF BCP 47 standard.
    legalName
        Text
        The official name of the organization, e.g. the registered company
        name.
    leiCode
        Text
        An organization identifier that uniquely identifies a legal entity as
        defined in ISO 17442.
    location
        Place or PostalAddress or Text
        The location of for example where the event is happening, an
        organization is located, or where an action takes place.
    logo
        ImageObject or URL
        An associated logo.
    makesOffer
        Offer
        A pointer to products or services offered by the organization or
        person.
        Inverse property: offeredBy.
    member
        Organization or Person
        A member of an Organization or a ProgramMembership. Organizations can
        be members of organizations; ProgramMembership is typically for
        individuals. Supersedes members, musicGroupMember.
        Inverse property: memberOf.
    memberOf
        Organization or ProgramMembership
        An Organization (or ProgramMembership) to which this Person or
        Organization belongs.
        Inverse property: member.
    naics
        Text
        The North American Industry Classification System (NAICS) code for a
        particular organization or business person.
    numberOfEmployees
        QuantitativeValue
        The number of employees in an organization e.g. business.
    ownershipFundingInfo
        AboutPage or CreativeWork or Text or URL
        For an Organization (often but not necessarily a
        NewsMediaOrganization), a description of organizational ownership
        structure; funding and grants. In a news/media setting, this is with
        particular reference to editorial independence. Note that the funder is
        also available and can be used to make basic funder information
        machine-readable.
    owns
        OwnershipInfo or Product
        Products owned by the organization or person.
    parentOrganization
        Organization
        The larger organization that this organization is a subOrganization of,
        if any. Supersedes branchOf.
        Inverse property: subOrganization.
    publishingPrinciples
        CreativeWork or URL
        The publishingPrinciples property indicates (typically via URL) a
        document describing the editorial principles of an Organization (or
        individual e.g. a Person writing a blog) that relate to their
        activities as a publisher, e.g. ethics or diversity policies. When
        applied to a CreativeWork (e.g. NewsArticle) the principles are those
        of the party primarily responsible for the creation of the
        CreativeWork.

        While such policies are most typically expressed in natural language,
        sometimes related information (e.g. indicating a funder) can be
        expressed using schema.org terminology.
    review
        Review
        A review of the item. Supersedes reviews.
    seeks
        Demand
        A pointer to products or services sought by the organization or person
        (demand).
    slogan
        Text
        A slogan or motto associated with the item.
    sponsor
        Organization or Person
        A person or organization that supports a thing through a pledge,
        promise, or financial contribution. e.g. a sponsor of a Medical Study
        or a corporate sponsor of an event.
    subOrganization
        Organization
        A relationship between two organizations where the first includes the
        second, e.g., as a subsidiary. See also: the more specific 'department'
        property.
        Inverse property: parentOrganization.
    taxID
        Text
        The Tax / Fiscal ID of the organization or person, e.g. the TIN in the
        US or the CIF/NIF in Spain.
    telephone
        Text
        The telephone number.
    unnamedSourcesPolicy
        CreativeWork or URL
        For an Organization (typically a NewsMediaOrganization), a statement
        about policy on use of unnamed sources and the decision process
        required.
    vatID
        Text
        The Value-added Tax ID of the organization or person.

    Attributes derived from Thing
    -----------------------------
    identifier
        PropertyValue or Text or URL
        The identifier property represents any kind of identifier for any kind
        of Thing, such as ISBNs, GTIN codes, UUIDs etc. Schema.org provides
        dedicated properties for representing many of these, either as textual
        strings or as URL (URI) links. See background notes for more details.
    name
        Text
        The name of the item.
    description
        Text
        A description of the item.
    url
        URL
        URL of the item.
    additionalType
        URL
        An additional type for the item, typically used for adding more
        specific types from external vocabularies in microdata syntax. This is
        a relationship between something and a class that the thing is in. In
        RDFa syntax, it is better to use the native RDFa syntax - the 'typeof'
        attribute - for multiple types. Schema.org tools may have only weaker
        understanding of extra types, in particular those defined externally.
    alternateName
        Text
        An alias for the item.
    disambiguatingDescription
        Text
        A sub property of description. A short description of the item used to
        disambiguate from other, similar items. Information from other
        properties (in particular, name) may be necessary for the description
        to be useful for disambiguation.
    image
        ImageObject or URL
        An image of the item. This can be a URL or a fully described
        ImageObject.
    mainEntityOfPage
        CreativeWork or URL
        Indicates a page (or other CreativeWork) for which this thing is the
        main entity being described. See background notes for details.
        Inverse property: mainEntity.
    potentialAction
        Action
        Indicates a potential Action, which describes an idealized action in
        which this thing would play an 'object' role.
    sameAs
        URL
        URL of a reference Web page that unambiguously indicates the item's
        identity. E.g. the URL of the item's Wikipedia page, Wikidata entry, or
        official website.
    subjectOf
        CreativeWork or Event
        A CreativeWork or Event about this Thing. Inverse property: about.
    """

    actionableFeedbackPolicy = None
    address = None
    aggregateRating = None
    alumni = None
    areaServed = None
    award: str = None
    brand = None
    contactPoint = None
    correctionsPolicy = None
    department = None
    dissolutionDate = None
    diversityPolicy = None
    diversityStaffingReport = None
    duns: str = None
    email: str = None
    employee = None
    ethicsPolicy = None
    event = None
    faxNumber: str = None
    founder = None
    foundingDate = None
    foundingLocation = None
    funder = None
    globalLocationNumber: str = None
    hasCredential = None
    hasMerchantReturnPolicy = None
    hasOfferCatalog = None
    hasPOS = None
    interactionStatistic = None
    isicV4: str = None
    knowsAbout = None
    knowsLanguage = None
    legalName: str = None
    leiCode: str = None
    location = None
    logo = None
    makesOffer = None
    member = None
    memberOf = None
    naics: str = None
    numberOfEmployees = None
    ownershipFundingInfo = None
    owns = None
    parentOrganization = None
    publishingPrinciples = None
    review = None
    seeks = None
    slogan: str = None
    sponsor = None
    subOrganization = None
    taxID: str = None
    telephone: str = None
    unnamedSourcesPolicy = None
    vatID: str = None
