"""Definition of the TemplateUploadCenter content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from AccessControl import ClassSecurityInfo

from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName

from Products.ArchAddOn.Fields import SimpleDataGridField
from Products.ArchAddOn.Widgets import SimpleDataGridWidget
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from Products.ATContentTypes.content.base import ATCTMixin
try:
    from Products.ATContentTypes.content.base import updateActions
    NEEDS_UPDATE = True
except ImportError:
    NEEDS_UPDATE = False


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
                                                                          
    atapi.LinesField('availableVersions',
        default=[
            'LibreOffice 3.3',
            'LibreOffice 3.4',
            'LibreOffice 3.5',
        ],
        widget=atapi.LinesWidget(
            label=u'Available Versions',
            description=u'Define the vocabulary for versions of LibreOffice that the templates can be listed as being compatible with. The first item will be the default selection.',
            i18n_domain='collective.TemplateUploadCenter',
            rows=6,
        ),
    ),
                                                                          
                                                                          
    atapi.LinesField('availablePlatforms',
        default=[
            'All platforms',
            'Linux',
            'Linux-x64',
            'Mac OS X',
            'Windows',
            'BSD',
            'UNIX (other)'
        ],
        widget=atapi.LinesWidget(
            label=u'Platforms',
            description=u'Define the available platforms for software files. The first line is reserved for All platforms or any equivalent labeling.',
            i18n_domain='collective.TemplateUploadCenter',
            rows=6,
        ),
    ),
    
        
    atapi.LinesField('availableSelfCertificationCriteria',
        default=[
            'Internationalized',
            'Unit tests',
            'End-user documentation',
            'Internal documentation (documentation, interfaces, etc.)',
            'Existed and maintained for at least 6 months',
            'Installs and uninstalls cleanly',
            'Code structure follows best practice',
        ],
        widget=atapi.LinesWidget(
            label=u'Self-Certification Checklist',
            description=u'Define the available criteria for developers to self-certify their projects.',
            i18n_domain='collective.TemplateUploadCenter',
            rows=10,
        ),
    ),
                                                                          

    atapi.TextField('product_description',
         default='Templates offer you a way to avoid duplicating repetitive actions when creating new text documents, spreadsheets, or presentations. They also offer a way to maintain consistency of document layout and standard content, and may, for example, be used to maintain consistent branding elements when used in a work place.',
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

# TemplateUploadCenterSchema['title'].storage = atapi.AnnotationStorage()
# TemplateUploadCenterSchema['description'].storage = atapi.AnnotationStorage()
# schemata.finalizeATCTSchema(
#    TemplateUploadCenterSchema,
#    folderish=True,
#    moveDiscussion=False
# )


class TemplateUploadCenter(folder.ATFolder):
    """A Center to upload templates to a Plone site"""
    implements(ITemplateUploadCenter)

    archetype_name= 'Template Center'
    meta_type = "TemplateUploadCenter"
    immediate_view = default_view ="templateuploadcenter_view"
    suppl_views = ()

    global_allow = 1
    filter_content_types = 1
    allowed_content_types = ('PSCProject',)
    schema = TemplateUploadCenterSchema
    _at_rename_after_creation = True

    security = ClassSecurityInfo()
    
    typeDescription = "A container for software projects"

    if NEEDS_UPDATE: # pre Plone3/GS-based install
        actions = updateActions(ATCTMixin,
                                ({
        'id'          : 'local_roles',
        'name'        : 'Sharing',
        'action'      : 'string:${object_url}/sharing',
        'permissions' : (permissions.ManageProperties,),
        },
                                 {
        'id'          : 'view',
        'name'        : 'View',
        'action'      : 'string:${folder_url}/',
        'permissions' : (permissions.View,),
        },
                                 )
                                )
    
    # Vocabulary methods
    security.declareProtected(permissions.View, 
                              'getAvailableTopicsFromClassifiers')
    def getAvailableTopicsFromClassifiers(self):
        """Get categories in DisplayList form, extracted from
        all classifiers that starts with 'Topic'"""
        field = self.getField('availableClassifiers')
        classifiers = field.getAsGrid(field)
        vocab = {}
        for id, title, trove_id in classifiers:
            if trove_id.startswith('Topic'):
                vocab[id] = (title, trove_id)
        return vocab

    security.declareProtected(permissions.View, 
                              'getAvailableCategoriesAsDisplayList')
    def getAvailableCategoriesAsDisplayList(self):
        """Get categories in DisplayList form."""
        return self.getField('availableCategories').getAsDisplayList(self)

    security.declareProtected(permissions.View, 'getAvailableClassifiersAsDisplayList')
    def getAvailableClassifiersAsDisplayList(self):
        return self.getField('availableClassifiers').getAsDisplayList(self)


    security.declareProtected(permissions.View, 'getAvailableLicensesAsDisplayList')
    def getAvailableLicensesAsDisplayList(self):
        """Get licenses in DisplayList form."""
        return self.getField('availableLicenses').getAsDisplayList(self)

    security.declareProtected(permissions.View, 'getAvailableVersionsAsDisplayList')
    def getAvailableVersionsAsDisplayList(self):
        """Get versions in DisplayList form."""
        return DisplayList([(item, item) for item in self.getAvailableVersions()])
    
    security.declareProtected(permissions.View, 'getAvailableVersionsAsDisplayList')
    def getAvailableSelfCertificationCriteriaAsDisplayList(self):
        """Get self-certification criteria in DisplayList form."""
        try: 
            return DisplayList([(item, item) for item in self.getAvailableSelfCertificationCriteria()])
        except:
            return DisplayList([('no','criteria')])
    
    # Mutator methods
    security.declareProtected(permissions.ModifyPortalContent, 'setProjectEvaluators')
    def setProjectEvaluators(self, value, **kw):
        orig = self.getProjectEvaluators()
        self.getField('projectEvaluators').set(self, value, **kw)
        
        usersToDemote = [id for id in orig if id not in value]
        usersToPromote = [id for id in value if id not in orig]
        
        for id in usersToDemote:
            roles = list(self.get_local_roles_for_userid(id))
            while 'PSCEvaluator' in roles:
                roles.remove('PSCEvaluator')
            if not roles:
                self.manage_delLocalRoles([id])
            else:
                self.manage_setLocalRoles(id, roles)
        for id in usersToPromote:
            roles = list(self.get_local_roles_for_userid(id))
            if 'PSCEvaluator' not in roles:
                roles.append('PSCEvaluator')
            self.manage_setLocalRoles(id, roles)

    security.declareProtected(permissions.View, 
                              'getFileStorageStrategyVocab')
    def getFileStorageStrategyVocab(self):
        """returns registered storage strategies"""
        return getFileStorageVocab(self)

    security.declareProtected(permissions.ModifyPortalContent, 'setStorageStrategy')
    def setStorageStrategy(self, value, **kw):
        """triggers an event before changing the field"""
        # the event will raise an error if any
        # project failed to migrate from one storage
        # to another
        old = self.getStorageStrategy()
        if old != value:
            event.notify(StorageStrategyChanging(self, old, value))
        self.getField('storageStrategy').set(self, value, **kw)    
    

#    title = atapi.ATFieldProperty('title')
#    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(TemplateUploadCenter, PROJECTNAME)
