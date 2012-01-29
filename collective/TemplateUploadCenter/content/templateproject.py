"""Definition of the templateproject content type
"""

from zope.interface import implements
from zope.component import getMultiAdapter
from AccessControl import ClassSecurityInfo
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.validation import V_SUFFICIENT, V_REQUIRED
from Products.ATContentTypes.content.base import ATCTMixin
try:
    from Products.ATContentTypes.content.base import updateActions
    NEEDS_UPDATE = True
except ImportError:
    NEEDS_UPDATE = False

from zExceptions import Unauthorized
import DateTime    

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from zExceptions import Unauthorized
import DateTime
# -*- Message Factory Imported Here -*-

from collective.TemplateUploadCenter.interfaces import Itemplateproject
from collective.TemplateUploadCenter.config import PROJECTNAME
from collective.TemplateUploadCenter import config

templateprojectSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.StringField('id',
        required=0,
        searchable=1,
        validators=('isNonConflictingProjectId',),
        widget=atapi.IdWidget (
            label=u'Short name',
            description=u"Should not contain spaces, underscores or mixed case. Short Name is part of the item's web address.",
            i18n_domain="collective.TemplateUploadCenter",
        ),
    ),
        
    atapi.TextField('description',
        default='',
        required=1,
        searchable=1,
        accessor="Description",
        #storage=MetadataStorage(),
        widget=atapi.TextAreaWidget(
            label=u'Project Summary',
            description=u'A short summary of the project.',
            i18n_domain="collective.TemplateUploadCenter",
            rows=5,
        ),
    ),
                                                                     

    atapi.TextField('text',
        default='',
        required=1,
        searchable=1,
        primary=1,
        default_content_type='text/plain',
        default_output_type='text/html',
        #allowable_content_types=config.TEXT_TYPES,
        widget=atapi.RichWidget(
            label=u'Full Project Description',
            description=u'The complete project description.',
            i18n_domain="collective.TemplateUploadCenter",
            rows=25,
        ),
    ),                                                                     

    
    atapi.LinesField('classifiers',
        multiValued=1,
        required=0,
        vocabulary='getClassifiersVocab',
        enforceVocabulary=1,
        schemata="metadata",
        index='KeywordIndex:schema',
        widget=atapi.MultiSelectionWidget(
            label=u'Classifiers',
            description=u'Trove classifiers for this item.',
            i18n_domain='collective.TemplateUploadCenter',
            rows=6,
        ),
    ),


    atapi.LinesField('categories',
        multiValued=1,
        required=1,
        vocabulary='getCategoriesVocab',
        enforceVocabulary=1,
        index='KeywordIndex:schema',
        widget=atapi.MultiSelectionWidget(
            label=u'Categories',
            description=u'Categories that this item should appear in.',
            i18n_domain="collective.TemplateUploadCenter",
        ),
    ),

    
    atapi.LinesField('selfCertifiedCriteria',
        multiValued=1,
        required=0,
        vocabulary='getSelfCertificationCriteriaVocab',
        enforceVocabulary=1,
        index='KeywordIndex:schema',
        schemata="review",
        widget=atapi.MultiSelectionWidget(
            label=u'Self-Certification Checklist',
            description=u'Check which criteria this project fulfills.',
            i18n_domain="collective.TemplateUploadCenter",
            format="checkbox",
        ),
    ),
    
    atapi.BooleanField('isApproved',
        required=0,
        #write_permission=ApproveProject,
        schemata="review",
        widget=atapi.BooleanWidget(
            label=u'Approved',
            description=u'Indicate whether this project is approved by product reviewers.',
            i18n_domain="collective.TemplateUploadCenter",
        ),
    ),
    
    atapi.TextField('reviewComment',
        searchable=1,
        required=0,
        schemata="review",
        #write_permission=AddReviewComment,
        widget=atapi.TextAreaWidget(
            label=u'Review Comment',
            description=u'Additional notes by reviewers of this project.',
            i18n_domain="collective.TemplateUploadCenter",
        ),
    ),


    atapi.StringField('contactAddress',
        required=1,
        validators = (('isMailto', V_SUFFICIENT), ('isURL', V_REQUIRED),),
        widget=atapi.StringWidget(
            label=u'Contact address',
            description=u'Contact address for the project. Use mailto: or http:// prefix depending on what contact method you prefer.',
            i18n_domain="collective.TemplateUploadCenter",
        ),
    ),

   atapi.StringField('homepage',
        searchable=1,
        required=0,
        validators=('isURL',),
        widget=atapi.StringWidget(
            label=u'Home page',
            description=u'If the project has an external home page, enter its URL.',
            i18n_domain="collective.TemplateUploadCenter",
        ),
    ),

    atapi.StringField('documentationLink',
        searchable=1,
        required=0,
        validators=('isURL',),
        widget=atapi.StringWidget(
            label=u'URL of documentation repository',
            description=u'If the project has externally hosted documentation, enter its URL.',
            i18n_domain="collective.TemplateUploadCenter",
        ),
    ),

    atapi.StringField('repository',
        searchable=1,
        required=0,
        validators=('isURL',),
        widget=atapi.StringWidget(
            label=u'URL of version control repository',
            description=u'If the project has a code repository, enter its URL.',
            i18n_domain="collective.TemplateUploadCenter",
        ),
    ),

    atapi.StringField('tracker',
        searchable=1,
        required=0,
        validators=('isURL',),
        widget=atapi.StringWidget(
            label=u'Issue tracker URL',
            description=u'If the project has an external issue tracker, enter its URL.',
            i18n_domain="collective.TemplateUploadCenter",
        ),
    ),

    atapi.StringField('mailingList',
        searchable=1,
        required=0,
        validators=('isURL',),
        widget=atapi.StringWidget(
            label=u'Support mailing list or forum URL',
            description=u'URL of mailing list information page/archives or support forum, if the project has one.',
            i18n_domain="plonesoftwarecenter",
        ),
    ),

    atapi.ImageField('logo',
        required=0,
        original_size=(150,75),
        sizes=config.IMAGE_SIZES,
        widget=atapi.ImageWidget(
            label=u'Logo',
            description=u"Add a logo for the project (or organization/company) by clicking the 'Browse' button. Max 150x75 pixels (will be resized if bigger).",
            i18n_domain="collective.TemplateUploadCenter",
        ),
    ),

    atapi.StringField('logoURL',
        searchable=1,
        required=0,
        validators=('isURL',),
        widget=atapi.StringWidget(
            label=u'Logo link',
            description=u'The URL the logo should link to, if applicable.',
            i18n_domain="collective.TemplateUploadCenter",
        ),
    ),

    atapi.ImageField('screenshot',
        required=0,
        original_size=(800,600),
        sizes=config.IMAGE_SIZES,
        widget=atapi.ImageWidget(
            label=u'Screenshot',
            description=u"Add a screenshot by clicking the 'Browse' button. Max 800x600 (will be resized if bigger).",
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
    
    security = ClassSecurityInfo()
        
    security.declareProtected(permissions.View, 'getCategoriesVocab')
    def getCategoriesVocab(self):
        """Get categories vocabulary from parent project area via acquisition.
        """
        return self.getAvailableCategoriesAsDisplayList()
    

atapi.registerType(templateproject, PROJECTNAME)
