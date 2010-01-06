"""a tool for creating etpkgmanager caches"""

__version__ = "0.1"
__all__ = ["Cache"]

import component
import os, os.path
import shutil
import sys

# TODO
# 1. test the tuple input
# 2. remove dups and clean up
# 3. remove these comments and other pointless BS
# 4. find a reasonable way to re-raise exceptions

# In EPM, patches are stored in the cache.  The path to the cache is found in
# the template.  The (possibly temporary) path to the files or components that
# go into the template comes from the user.  When populating a cache, the
# primary objective is to find components somewhere, and copy them into the
# cache by their hexdigest.  If starting with bare files, the cache module
# must first convert them into components with the component module.

# use this until we have the template in place
CACHE_STUB = os.path.join(r"C:\\", "temp", "epm_cache")

# cache tasks (in no particular order):
#
# 1. copy components from <somewhere> to cache
#   [in the stash() method]
# 2. query template (or get from user) (or use default) path to cache
#   [we can't do this until we have a template]
# 3. if duplicate (cached component already present), call component.py on
#    both, verify identical, inform user [INFO]
# 4. identify self to other cache servers
# 5. find other cache servers or caches
# 6. if component requested, locate and return or None; how is the component
#    requested?  Do we need this right now?
# 7. add components to peer component catalog
# 8. batch add components to the cache (recursively walking a directory?)

class Cache(object):
    """DOCSTRING"""
    def __init__(self):
        self.c = component.Component()

    def stash(self, source):
        """DOCSTRING"""
        # Whether we're creating the component or a component is passed in,
        # the input is a two-tuple (_hash, _path).  _hash is the 40-bit
        # hexdigest, and _path is either the path to the file, or a directory,
        # which is processed recursively.

        # _copy is private to stash()
        def _copy(file_to_copy, cache_path):
            try:
                os.makedirs(cache_path)
            except OSError:
                #   - if OSError (file or directory already exists):
                #       - TODO this is a configuration setting: be conservative
                #       for now; don't change anything; warn the user and continue
                sys.stderr.write("warning: could not make directory: %s\n" % cache_path)
            except:
                sys.stderr.write("something's broken in _copy()!\n")
                sys.exit(1) # until I come up with something else
            shutil.copy2(file_to_copy, cache_path)

        _type = source.__class__.__name__
        _hash = _path = file_to_copy = None

        if _type == 'str':
            if os.path.isfile(source):
                (_hash, _path) = self.c.id(source)
                # the component source file (with path)
                file_to_copy = _path
                cache_path = os.path.join(CACHE_STUB, _hash)
                _copy(file_to_copy, cache_path)

            # recursively process all files in the directory
            elif os.path.isdir(source):
                for root, dirs, files in os.walk(source):
                    for file in files:
                        (_hash, _path) = self.c.id(os.path.join(root, file))
                        file_to_copy = _path
                        cache_path = os.path.join(CACHE_STUB, _hash)
                        _copy(file_to_copy, cache_path)

            else:
                sys.stderr.write("error: string is not a file or directory\n")
                # sys.exit() knocks me out of the interpreter :(
                sys.exit(1)
#                raise

        elif _type == 'tuple':
            # assume it's a two-tuple as returned from component; in this
            # case, it's already a component and just needs to be stashd.
            try:
                (_hash, _path) = source
                file_to_copy = _path
                cache_path = os.path.join(CACHE_STUB, _hash)
#                print file_to_copy, cache_path
                _copy(file_to_copy, cache_path)
            except ValueError:
                sys.stderr.write("error: this doesn't look like a component tuple\n")
                sys.exit(1) # until I come up with something else
#                raise
            except:
                sys.stderr.write("something's broken in stash()!\n")
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
        #   - else:
        #       - TODO write an update to the screen or log (something like
        #       "caching <hexdigest> component <filename>")
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

