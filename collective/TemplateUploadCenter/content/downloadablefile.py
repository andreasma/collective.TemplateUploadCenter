"""Definition of the Downloadablefile content type
"""
import re
from AccessControl import ClassSecurityInfo
from Products.CMFCore import permissions
from collective.TemplateUploadCenter.storage import DynamicStorage


from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from collective.TemplateUploadCenter.interfaces import IDownloadablefile
from collective.TemplateUploadCenter.config import PROJECTNAME

# added for virus scanning
from Products.ATContentTypes.content.base import ATCTFileContent
from Products.validation import V_REQUIRED

DownloadablefileSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

      
    atapi.TextField('title',
        default='',
        searchable=1,
        accessor="Title",
        widget=atapi.StringWidget(
            label=u'File Description',
            description=u"File name: Write the name of the file. Remember to use proper file extension, e.g.'oxt' for LibreOffice extensions or 'otp' for presentation templates.",
            i18n_domain="collective.TemplateUploadCenter",
            visible = {'edit' : 'hidden', 'view' : 'visible'},
            
        ),
    ),

    atapi.FileField('downloadableFile',
        primary=1,
        required=1,
        validators = (('isNonEmptyFile', V_REQUIRED),
                      ('isVirusFree', V_REQUIRED),),
        widget=atapi.FileWidget(
            label=u"File",
            description="Click 'Browse' to upload a release file.",
            i18n_domain="collective.TemplateUploadCenter",
        ),
        storage=DynamicStorage(),
    ),
                                    

    atapi.BooleanField('acceptdisclaimer',
        required=1,
        widget=atapi.BooleanWidget(
             label=u"Accept the Legal Disclaimer and Limitations below:",
             description=u"<h3>Legal Disclaimers and Limitations</h3><p>The text for the disclaimer and limitations go here.</p>",
             i18n_domain="collective.TemplateUploadCenter",               
        ),
    ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

DownloadablefileSchema['title'].storage = atapi.AnnotationStorage()
DownloadablefileSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(DownloadablefileSchema, moveDiscussion=False)


class Downloadablefile(ATCTFileContent):
    """Downloadble file"""
    implements(IDownloadablefile)
    archetype_name = 'Downloadable File'
    meta_type = "Downloadablefile"
    content_icon = 'file_icon.gif'
    schema = DownloadablefileSchema
    global_allow=False

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    security = ClassSecurityInfo()

    # XXX: This should go away once ATCT is fixed to not mangle filenames
    def _cleanupFilename(self, filename, encoding=None, **kw):
        """Cleans the filename from unwanted or evil chars
        """
        # Do nothing for now, ATCT is too liberal with this.
        return filename

    security.declareProtected(permissions.View, 'getPlatformVocab')
    def getPlatformVocab(self):
        """Get the platforms available for selection via acquisition from
        the top-level projects container.
        """
        #return DisplayList([(item, item) for item in \
        #                    self.getAvailablePlatforms()])

    security.declareProtected(permissions.ModifyPortalContent, 'setDownloadableFile')
    def setDownloadableFile(self, value, **kwargs):
        """Set id to uploaded id
        """
        self._setATCTFileContent(value, **kwargs)

atapi.registerType(Downloadablefile, PROJECTNAME)
