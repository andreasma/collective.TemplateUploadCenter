from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner

import re

class DownloadableFileView(BrowserView):

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)

        self.membership = getToolByName(self.context, 'portal_membership')
        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.portal_url = getToolByName(self.context, 'portal_url')()

        self.context_path = '/'.join(self.context.getPhysicalPath())