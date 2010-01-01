# a file abstraction
#
#

import hashlib
import os.path
import sys

class Component(object):
    """DOCSTRING"""
    # What do I want this to be?  We need [[ some information ]] about each
    # file (and directory?) that is eligible to become an epm component.
    #
    # 1. path from root
    # 2. absolute path?  Probably not necessary.
    # 3. statistics?  atime, ctime, etc.
    # 4. SHA-1 hexdigest
    # 5. name?
    def __init__(self):
#        self.hash = hashlib.sha1()
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
            print "_name: %s" % _name

            if _name == 'str':
                if raw:
                    # it's ready to go as-is
                    to_hash = _input
                else:
                    # it's a path - resolve the filename and fetch the file
#                if os.path.isfile(_input):
                    to_hash = file(_input, 'rb').read()
#                else:
#                    pass

            # (2) the contents of a file object (e.g., somefile.read())
            elif _name == 'file':
                to_hash = file(_input, 'rb').read()

            else:
                print("something's broken in id()!")
                return

            # (3) a file object
            try:
                self.hash.update(to_hash)
                self.fid = self.hash.hexdigest()
            except TypeError:
                # I don't know what sort of exceptions we may run into here.
                # http://blog.ianbicking.org/2007/09/12/re-raising-exceptions/
                sys.stderr.write("unhashable input: %s" % component)
                raise

#                try:
#                    self.hash.update(_input.read())
#                    self.fid = self.hash.hexdigest()
#                except:
#                    # TODO fix this (find Ian Bicking notes)
#                    print "got some kind of exception"

            # Maybe better would be to just try and update _input.  If it
            # fails, then try to open and read the file object.
#            if isinstance(_input, file):
#                fr = _input.read()
#                try:
#                    self.hash.update(fr)
#                    self.fid = self.hash.hexdigest()
#                except TypeError:
#                    # TODO fix this (find Ian Bicking notes)
#                    print "got a TypeError"
#                except:
#                    print "got some kind of exception"
        return self.fid

