from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner



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
    
