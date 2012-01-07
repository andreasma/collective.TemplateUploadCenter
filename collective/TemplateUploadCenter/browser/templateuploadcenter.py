from urllib import quote

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner

class TemplateCenterView(BrowserView):
    
    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        
        self.membership = getToolByName(self.context, 'portal_membership')
        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.portal_url = getToolByName(self.context, 'portal_url')()
        
        self.context_path = '/'.join(self.context.getPhysicalPath())
        
                
    def rss_url(self):
        """Get the URL to the RSS feed for the project center
        """
        return "%s/search_rss?" \
                "portal_type=PSCRelease&" \
                "sort_on=Date&sort_order=reverse&"\
                "review_state=alpha&review_state=beta&" \
                "review_state=release-candidate&review_state=final" \
                % self.context.absolute_url()
    
        