"""a tool for creating etpkgmanager caches"""

__version__ = "0.1"
__all__ = ["Cache"]

import component
import os, os.path
import shutil
import sys

# In EPM, patches are stored in the cache.  The path to the cache is found in
# the template.  The (possibly temporary) path to the files or components that
# go into the template comes from the user.  When populating a cache, the
# primary objective is to find components somewhere, and copy them into the
# cache by their hexdigest.  If starting with bare files, the cache module
# must first convert them into components with the component module.

# use this until we have the template in place
CACHE_STUB = os.path.join(r"C:\\", "temp", "epm_cache")

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
        self.c = component.Component()

    def cache(self, source):
        """DOCSTRING"""
        # Whether we're creating the component or a component is passed in,
        # the input is a two-tuple (_hash, _path).  _hash is the 40-bit
        # hexdigest, and _path is the path to the file, optionally including
        # it's name.  If _path is a directory, it must contain EXACTLY ONE
        # file -- the contents to use to create a component.  Anything else is
        # an unrecoverable error.
        _type = source.__class__.__name__
        _hash = _path = file_to_copy = None

        if _type == 'str':
            if os.path.isfile(source):
                (_hash, _path) = self.c.id(source)
                # the component source file (with path)
                file_to_copy = _path
            elif os.path.isdir(source):
                dirlist = os.listdir(source)
                if len(dirlist) == 1:
                    # fetch the zero'th (only) item from dirlist
                    (_hash, _path) = self.c.id(os.path.join(source, dirlist[0]))
                    file_to_copy = _path
                else:
                    sys.stderr.write("error: wrong number of files in directory: %s\n" % source)
                    sys.exit(1) # until I come up with something else
#                    raise
            else:
                sys.stderr.write("error: string is not a file or directory\n")
                sys.exit(1) # until I come up with something else
#                raise
        elif _type == 'tuple':
            # assume it's a two-tuple as returned from component; in this
            # case, it's already a component and just needs to be cached.
            try:
                (_hash, _path) = source
                file_to_copy = _path
            except ValueError:
                sys.stderr.write("error: this doesn't look like a component tuple\n")
                sys.exit(1) # until I come up with something else
#                raise
            except:
                sys.stderr.write("something's broken in cache()!\n")
                sys.exit(1) # until I come up with something else
#                raise
        else:
            sys.stderr.write("unknown source: %s\n" % source)
            sys.exit(1) # until I come up with something else
#            raise

        if _hash is None or _path is None:
            sys.stderr.write("huh?\n")
            sys.exit(1)

        # do the caching
        #
        # TODO implement the real template
        #
        # 1. makedirs CACHE_STUB/<hexdigest>
        #   - if OSError (file or directory already exists):
        #       - TODO this is a configuration setting: be conservative for
        #         now; don't change anything; warn the user and continue
        # 2. copy file at _path to CACHE_STUB/<hexdigest>
        #   - this is DIFFERENT from what Dan and I talked about.  He wants to
        #     use the hexdigest as the file name.  I don't think that's a
        #     very good idea, since that means you need the catalog to figure
        #     out what file you're looking at.  Plus, that leaves us with
        #     nowhere to put any metadata that we may need in the future.
        #     (Although that's a violation of YAGNI.)
        #
        #     On the other hand, the file may have different names in
        #     different places (the WI "duplicate file" feature), so this
        #     isn't foolproof either.

#        print("CACHE_STUB: %s" % CACHE_STUB)
#        print("_hash: %s" % _hash)
#        print("file_to_copy: %s" % file_to_copy)
        cache_path = os.path.join(CACHE_STUB, _hash)
#        print("cache_path: %s" % cache_path)

        try:
            os.makedirs(cache_path)
        except OSError:
            #   - if OSError (file or directory already exists):
            #       - TODO this is a configuration setting: be conservative
            #       for now; don't change anything; warn the user and continue
            sys.stderr.write("warning: could not make directory: %s\n" % cache_path)
        except:
            sys.stderr.write("something's broken in cache()!\n")
            sys.exit(1) # until I come up with something else
#            raise
        shutil.copy2(file_to_copy, cache_path)

