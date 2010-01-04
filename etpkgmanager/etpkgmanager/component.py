"""a tool for creating etpkgmanager components"""

import hashlib
import os.path
import sys

class Component(object):
    """DOCSTRING"""
    def __init__(self):
        self.srcpath = None
        self.fid = None

    def id(self, _input=None, raw=False):
        """
        return a file's formal ID

        id accepts a file object, or a file's contents (e.g., from
        file.read()) and returns the SHA-1 hexdigest.

        Try to create a digest in the order listed above.  _input should be
        one of:
            (1) a string, optionally representing a file on disk
            (2) the contents of a file object (e.g., somefile.read())
            (3) a file object

        Number (1) is tricky since the string can be used to create a digest
        directly.  And there is no way to know if the intent is to digest the
        string itself, or fetch the file at that location and digest the
        contents of the file to which the string refers.  To remove this
        ambiguity, the 'raw' attribute should be set to True to indicate that
        the string should be digested as-is.  If _input is not a string, the
        raw attribute is ignored.
        """
        self.hash = hashlib.sha1()
        if _input:
            _name = _input.__class__.__name__
#            print "_name: %s" % _name

            if _name == 'str':
                if raw:
                    # no source path
                    to_hash = _input
                else:
                    try:
                        to_hash = file(_input, 'rb').read()
                        self.srcpath = _input
                        #self.srcpath = os.path.normpath(_input)
                    except IOError:
                        sys.stderr.write("unhashable input: %s\n" % _input)
                        raise
            elif _name == 'file':
                try:
                    to_hash = file(_input, 'rb').read()
                    self.srcpath = _input
                    #self.srcpath = os.path.normpath(_input)
                except IOError:
                    sys.stderr.write("unhashable input: %s\n" % component)
                    raise
            else:
                print("something's broken in id()!")
                return

            try:
                self.hash.update(to_hash)
                self.fid = self.hash.hexdigest()
            except TypeError:
                # http://blog.ianbicking.org/2007/09/12/re-raising-exceptions/
                sys.stderr.write("unhashable input: %s\n" % component)
                raise
#        return self.fid
#        return {self.fid: self.srcpath}
        return [self.fid, self.srcpath]

