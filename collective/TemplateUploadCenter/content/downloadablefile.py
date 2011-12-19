"""Definition of the Downloadablefile content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from collective.TemplateUploadCenter.interfaces import IDownloadablefile
from collective.TemplateUploadCenter.config import PROJECTNAME

DownloadablefileSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

DownloadablefileSchema['title'].storage = atapi.AnnotationStorage()
DownloadablefileSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(DownloadablefileSchema, moveDiscussion=False)


class Downloadablefile(base.ATCTContent):
    """Downloadble file"""
    implements(IDownloadablefile)

    meta_type = "Downloadablefile"
    schema = DownloadablefileSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Downloadablefile, PROJECTNAME)
