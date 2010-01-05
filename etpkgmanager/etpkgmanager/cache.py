"""a tool for creating etpkgmanager caches"""

__version__ = "0.1"
__all__ = ["Cache"]

import component

# In EPM, patches are stored in the cache.  The path to the cache is found in
# the template.  The (possibly temporary) path to the files or components that
# go into the template comes from the user.  When populating a cache, the
# primary objective is to find components somewhere, and copy them into the
# cache by their hexdigest.  If starting with bare files, the cache module
# must first convert them into components with the component module.

# cache tasks
#
# 1. copy components from <somewhere> to cache
# 2. query template (or get from user) (or use default) path to cache
# 3. if duplicate (cached component already present), call component.py on
#    both, verify identical, inform user [INFO]
# 4. identify self to other cache servers
# 5. find other cache servers or caches
# 6. if component requested, locate and return or None
# 7. add components to peer component catalog

class Cache(object):
    """DOCSTRING"""
    def __init__(self):
        pass

    def cache(self, source):
        """DOCSTRING"""
        # if source is not a component, convert it first
        #
        # how to figure out if it is a component?
