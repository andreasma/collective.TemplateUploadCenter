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
    
    atapi.TextField(
         name='description',
         accessor='Description',
         widget=atapi.TextAreaWidget(
                label=u'Description',
                label_msgid='description',
                description=u'Description for the Template Upload Center.',
                i18n_domain='collective.TemplateUploadCenter',
                rows=6,
                ),
         searchable=True,
         ),
         
    atapi.StringField('product_title',
        default='Templates',
        widget=atapi.StringWidget(
            label=u'Product Title',
            label_msgid='product_title',
            description=u"Title of products when using the project view. For example, 'Add-on Product', 'Extension', or 'Template'.",
            i18n_domain='collective.TemplateUploadCenter',
            ),
    ),     

    atapi.TextField('product_description',
         default='Templates Templates offer you a way to avoid duplicating repetitive actions when creating new text documents, spreadsheets, or presentations. They also offer a way to maintain consistency of document layout and standard content, and may, for example, be used to maintain consistent branding elements when used in a work place.',
         widget=atapi.TextAreaWidget(
                label=u'Description of the Product',
                label_msgid='productdescription',
                description=u'Please provide some text to introduce the product.',
                i18n_domain='collective.TemplateUploadCenter',
                ),
       ),         

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
