"""Common configuration constants
"""
from zLOG import LOG, PROBLEM
import os
from App.Common import package_home

PROJECTNAME = 'collective.TemplateUploadCenter'

SKINS_DIR = 'skins'


HARD_DEPS = ('AddRemoveWidget', 'ArchAddOn', 'DataGridField',)
SOFT_DEPS = 'ATReferenceBrowserWidget',

RELEASES_ID = 'releases'
IMPROVEMENTS_ID = 'roadmap'
DOCUMENTATION_ID = 'documentation'
TRACKER_ID = 'issues'

TEXT_TYPES = (
    'text/structured',
    'text/x-rst',
    'text/html',
    'text/plain',
)

IMAGE_SIZES = {
    'preview': (256, 256),
    'thumb': (128, 128),
    'tile': (64, 64),
    'icon': (32, 32),
    'listing': (16, 16),
}


ADD_PERMISSIONS = {
    # -*- extra stuff goes here -*-
    'Downloadablefile': 'collective.TemplateUploadCenter: Add Downloadablefile',
    'templateproject': 'collective.TemplateUploadCenter: Add templateproject',
    'TemplateUploadCenter': 'collective.TemplateUploadCenter: Add TemplateUploadCenter',
}

# Todo: external storage proof is not included yet
# Trove is not implemented yet.


