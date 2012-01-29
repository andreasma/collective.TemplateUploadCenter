from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner
from Products.Archetypes.atapi import DisplayList
import re



class TemplateProjectView(BrowserView):
    
    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        
        self.membership = getToolByName(self.context, 'portal_membership')
        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.portal_url = getToolByName(self.context, 'portal_url')()
        
        self.context_path = '/'.join(self.context.getPhysicalPath())
        
        
    def get_title_legaldownloaddisclaimer(self):
        tuc = self.context.getParentNode()
        return tuc.getTitle_legaldownloaddisclaimer()
    
    def get_subtitle_legaldownloaddisclaimer(self):
        tuc = self.context.getParentNode()
        return tuc.getSubtitle_legaldownloaddisclaimer()
    
    def get_legal_downloaddisclaimer(self):
        tuc = self.context.getParentNode()
        return tuc.getLegal_downloaddisclaimer()
    
    def compatibility_vocab(self):
        """Get the available compatability versions from the parent project
           area via acqusition.
        """
        return self.context.getAvailableVersionsAsDisplayList()

    def license_vocab(self):
        """Get the available licenses from the parent project area via
         acqusition.
        """
        return self.context.getAvailableLicensesAsDisplayList()

    
