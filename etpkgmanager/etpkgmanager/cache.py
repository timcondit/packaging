"""a tool for creating etpkgmanager caches"""

__version__ = "0.1"
__all__ = ["Cache"]


# In EPM, patches are stored in the cache.  The path to the cache is found in
# the template.  The (possibly temporary) path to the files or components that
# go into the template comes from the user.  When populating a cache, the
# primary objective is to find components somewhere, and copy them into the
# cache by their hexdigest.  If starting with bare files, the cache module
# must first convert them into components with the component module.
class Cache(object):
    """DOCSTRING"""
    def __init__(self):
        pass

