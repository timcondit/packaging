"""a tool for creating etpkgmanager catalogs"""

__version__ = "0.1"
__all__ = ["Catalog"]

import component
import hashlib
import os.path
import sys
from optparse import OptionParser


# A generic catalog is not much more than a collection of components
# identified by SHA-1 hexdigest, the component's source path, and the catalog
# itself.  This class iterates over a set of files or recursively from some
# location in the local filesystem, generates components, and creates the
# catalog.  Maybe it should also cache and verify each component.
#
# Something else to consider is "catalog discovery", where a catalog is
# generated or modified by inspecting the local cache and any other peer
# caches that the client has access to.

# methods:
#
# make()
#   description: 
#   in: 
#   out: 
#
# show()
#   description: 
#   in: 
#   out: 

class Catalog(object):
    """generate the component catalog"""

    def __init__(self):
        """DOCSTRING"""
        self.sha1 = hashlib.sha1()
        self._catfile()

    # I don't want to jump right into making a catalog if it's not found.
    # Either it should be an option or we should go right into a REPL.  The
    # REPL might be nice later, but for now, I like command-driven.  This
    # module is not the place for interactivity in any event.
    def _catfile(self):
        catfile = os.path.join(os.getcwd(), "catalog.txt")
        if os.path.exists(catfile):
            print("found component catalog %s" % catfile)
        else:
            print("component catalog not found")

    def hash(self, component):
        """return the SHA-1 hash for a string or binary file"""
        # Is component hashable?  hashlib accepts a string or a read-only
        # buffer.  The idiomatic Python approach is to assume component is the
        # right type, and deal with exceptions as they appear.
        try:
            self.sha1.update(open(component, 'rb').read())
            return self.sha1.hexdigest()
        except:
            # I don't know what sort of exceptions we may run into here.
            # http://blog.ianbicking.org/2007/09/12/re-raising-exceptions/
            sys.stderr.write("unhashable input: %s" % component)
            raise

    def version(self, current=None):
        """get or set the catalog file version"""
        pass


if __name__ == "__main__":
    cat = Catalog()
