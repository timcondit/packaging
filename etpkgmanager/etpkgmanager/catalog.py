"""a tool for creating etpkgmanager catalogs"""

__version__ = "0.1"
__all__ = ["Catalog"]

import hashlib
import os.path
import sys
from optparse import OptionParser


# hustle and flow:
# 0. For now, the catalog is either with the package or it's not present.
#    Later on we may want to specify the path to a config file on the
#    command-line like I'm doing with common-buildtools.  Look for it in
#    __init__().
#
# 1. There's no reason to make a distinction between the reference catalog and
#    others.  There's nothing special about the reference catalog.  It's just
#    guaranteed to be the latest version.

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
