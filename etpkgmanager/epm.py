"""epm: top-level driver for etpkgmanager"""

__version__ = "0.1"
#__all__ = ["EPM"]

import etpkgmanager.repl as repl

#class EPM(object):
#    """DOCSTRING"""
#
#    def __init__(self):
#        """DOCSTRING"""
#        pass

if __name__ == "__main__":
    loop = repl.Loop()
    loop.mainloop()
