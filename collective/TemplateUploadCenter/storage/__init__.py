from zope.component import getAdapter
from zope.component import getAdapters
from Acquisition import aq_parent

from collective.TemplateUploadCenter.storage.interfaces import ITUCFileStorage


class DynamicStorage(object):
    """This storage will trigger the right kind of storage
    given the user settings at root level"""

    def get(self, name, instance, **kwargs):
        # XXX Can we do this for now to get through a catalog clear and rebuild ? 
        try:
            return self._getStorage(instance).get(name, instance, **kwargs)
        except:
            pass

    def set(self, name, instance, value, **kwargs):
        return self._getStorage(instance).set(name, instance, value, **kwargs)

    def unset(self, name, instance, **kwargs):
        return self._getStorage(instance).get(name, instance, **kwargs)

    def getName(self):
        return 'dynamic'

    def _getStorage(self, instance):
        """returns the storage name, which is stored at PSC level"""
        # XXX crawl back up - what if the node in not in a PSC instance ?
        # need a better code here
        from collective.TemplateUploadCenter.content.templateuploadcenter import TemplateUploadCenter

        tuc = instance
        while not isinstance(tuc, TemplateUploadCenter) and tuc is not None:
            # Walk up the acquisition chain to the
            # PloneSoftwareCenter.  Note: in the context of browser
            # views the acquisition chain of the context is: context,
            # browser view, context, real parent of context.  So the
            # context is its own grandparent.
            tuc = aq_parent(tuc)

        if tuc is None:
            # Should Not Happen (TM)
            raise Exception("No TemplateUploadCenter found in acquisition "
                            "chain of %r." % instance)
        name = psc.getStorageStrategy()
        return getAdapter(tuc, ITUCFileStorage, name)


def getFileStorageAdapters(context):
    return getAdapters((context, ), ITUCFileStorage)


def getFileStorageVocab(context):
    """Return a vocab for the psc edit form.

    Should probably go on a view somewhere eventually"""
    adapters = getFileStorageAdapters(context)
    return [(name, "%s (%s)" % (storage.title, storage.description))
            for name, storage in adapters]
