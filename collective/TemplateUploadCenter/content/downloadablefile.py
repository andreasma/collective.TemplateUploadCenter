"""Definition of the Downloadablefile content type
"""
import re
from AccessControl import ClassSecurityInfo
from Products.CMFCore import permissions
from collective.TemplateUploadCenter.storage import DynamicStorage
from Products.Archetypes.atapi import DisplayList


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
    
    atapi.TextField('description',
        default='',
        required=1,
        searchable=1,
        accessor="Description",
        widget=atapi.TextAreaWidget(
            label=u"Description of the file and it's features",
            description=u"Give a Description of the file that you upload; especially of it's featrures",
            i18n_domain="collective.TemplateUploadCenter",
            rows=6,  
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
  
  
    atapi.StringField(
        name='license',
        required=1,
        vocabulary='getLicenseVocab',
        widget=atapi.SelectionWidget(
            format = 'radio',
            label=u"License",
            description=u"License of the file: Please examine carefully which license you choose for your contribution. You can't  change it after the release.",
            i18n_domain='collective.TemplateUploadCenter',
        ),
    ),
                           
  
    atapi.StringField(
        name='license2',
        required=0,
        vocabulary='getLicenseVocab',
        widget=atapi.SelectionWidget(
            format = 'radio',
            label=u"Second License",
            description=u"Second License (if published under different licenses)",
            i18n_domain='collective.TemplateUploadCenter',
        ),
    ),
                                                                             
  
    atapi.StringField(
        name='license3',
        required=0,
        vocabulary='getLicenseVocab',
        widget=atapi.SelectionWidget(
            format = 'radio',
            label=u"Third License",
            description=u"Third License (if published under different licenses).",
            i18n_domain='collective.TemplateUploadCenter',
        ),
    ),                                                                             



    atapi.LinesField(
        name='compatibility',
        required=1,
        searchable=1,
        index='KeywordIndex:schema',
        vocabulary='getCompatibilityVocab',
        widget=atapi.MultiSelectionWidget(
            label=u"Compatibility",
            description=u"Tested and working with the following versions:",
            i18n_domain='collective.TemplateUploadCenter',
        ),
    ),



    atapi.BooleanField('acceptdisclaimer',
        required=1,
        widget=atapi.BooleanWidget(
             label=u"Accept the Legal Disclaimer and Limitations below:",
             description=u"<h3>Legal Disclaimers and Limitations</h3><p>The text for the disclaimer and limitations go here.</p>",
             i18n_domain="collective.TemplateUploadCenter",               
        ),
    ),
                                                                             
                                                                                 
    atapi.TextField('contributors',
        widget=atapi.TextAreaWidget(
            i18n_domain='collective.TemplateUploadCenter',
            visible = {'edit' : 'hidden', 'view' : 'hidden'},
                                    ),
                    ),

                                                                             
    atapi.TextField('rights',
        widget=atapi.TextAreaWidget(
            i18n_domain='collective.TemplateUploadCenter',
            visible = {'edit' : 'hidden', 'view' : 'hidden'},
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
    immediate_view = default_view = 'ctu_file_view'
    suppl_views = ()
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
        
    security.declareProtected(permissions.View, 'getLicenseVocab')
    def getLicenseVocab(self):
        """Get the available licenses from the parent project area via
         acqusition.
        """
        return self.getAvailableLicensesAsDisplayList()
    
    security.declareProtected(permissions.View, 'getCompatibilityVocab')
    def getCompatibilityVocab(self):
        """Get the available compatability versions from the parent project
           area via acqusition.
        """
        return self.getAvailableVersionsAsDisplayList()
            

atapi.registerType(Downloadablefile, PROJECTNAME)
