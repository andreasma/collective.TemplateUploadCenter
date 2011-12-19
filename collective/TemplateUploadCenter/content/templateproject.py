"""Definition of the templateproject content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from collective.TemplateUploadCenter.interfaces import Itemplateproject
from collective.TemplateUploadCenter.config import PROJECTNAME

templateprojectSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

templateprojectSchema['title'].storage = atapi.AnnotationStorage()
templateprojectSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    templateprojectSchema,
    folderish=True,
    moveDiscussion=False
)


class templateproject(folder.ATFolder):
    """A template project for LibreOffice"""
    implements(Itemplateproject)

    meta_type = "templateproject"
    schema = templateprojectSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(templateproject, PROJECTNAME)
