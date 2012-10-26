from collective.roster.interfaces import IContactInfo

class IContactInfo(form.Schema):
    """ Interface for providing contact info """
    email = schema.TextLine(
        title=_(u"From"),
        description=_(u"Form letter sender"),
    )


