"""Definition of the TemplateUploadCenter content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from collective.TemplateUploadCenter.interfaces import ITemplateUploadCenter
from collective.TemplateUploadCenter.config import PROJECTNAME

TemplateUploadCenterSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

TemplateUploadCenterSchema['title'].storage = atapi.AnnotationStorage()
TemplateUploadCenterSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    TemplateUploadCenterSchema,
    folderish=True,
    moveDiscussion=False
)


class TemplateUploadCenter(folder.ATFolder):
    """A Center to upload templates to a Plone site"""
    implements(ITemplateUploadCenter)

    meta_type = "TemplateUploadCenter"
    schema = TemplateUploadCenterSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(TemplateUploadCenter, PROJECTNAME)
