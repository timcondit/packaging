
etpkgmanager
-------------

The Envision Telephony Package Manager (EPM) complements existing customer
installs and will help with future patch installs.  It is run after one or
more software installations to collect identifying information about the files
on the system.

Eventually we intend to have EPM replace Windows installer, but for now our
goals are less ambitious.



The system is designed to be fully autonomous, with updates delivered along
with the patches themselves.  The three main components are the catalog, the
templates and the cache.

The catalog is a possibly out-of-date list of all released components for
every ET application.  Each component is formally identified by a 40-digit
hexidecimal SHA-1 hash value.  Along with that is an
application_ID:destination_path dictionary (the other kind of hash :)), and
possibly informal names for the files themselves.  The canonical catalog is
maintained at Envision.  It is add-only, as once things go in, they stay in.
The catalogs onsite with the installations are complete in that they contain
descriptors for all properly patched files on the system, but they may not be
up to date with respect to the latest version of the catalog.  Catalogs are
versioned with integers, with each patch incrementing the version by 1.  In
this way when a system is scanned and the details sent back to Envision for
troubleshooting, the same catalog that was used onsite can be recovered if
necessary.

<aside>
Note, because of the way hashes work, two files with the same content (but not
necessarily the same name) have the same hash value.  So the hash value is
reusable within an application and potentially even between applications.  In
fact, if we didn't use it this way we'd wind up with collisions and other
trouble.

    >>> import hashlib
    >>> s = hashlib.sha1()
    >>> s.update(open('hh.exe','rb').read())
    >>> s.hexdigest()
    '4bc8c967a6e3ee848c1c136b58d365c202a2b576'
    >>> s2 = hashlib.sha1()
    >>> s2.update(open('c_windows_hh.exe','rb').read())
    >>> s2.hexdigest()
    '4bc8c967a6e3ee848c1c136b58d365c202a2b576'
</aside>


