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


=======

etpkgmanager
-------------

[misc. notes]
* I use the word file in the traditional sense and component to mean a file
  that is known to EPM.
* Generally, my comments and asides in this document are in <angle brackets>,
  while section headers are in [square brackets].


[intro]
The Envision Telephony Package Manager (EPM) complements existing customer
installs and will help with future patch installs.  It is run after one or
more software installations to collect identifying information about the
components on the system.


[project goals]
Eventually we intend to have EPM replace Windows installer for Envision's
installs, but our short term goals are less ambitious.

I'll describe goals in terms of time (short, medium, and long-term), and main
users (usually Support&customers or CET&QA, or both).

Short-term goals
* automate patch installation and rollback
* report on all patches on all ET applications for a particular host machine;
  this includes generating "forensic" reports showing the original source of
  specific components for known (released) components.
* maintain a repository of all components from which any known release (e.g.,
  anything stored at \\Bigfoot\Releases is eligible) or patch can be recreated
* 



[ ... ]
The system is designed to be fully autonomous, with updates delivered along
with the patches themselves.  The three main components are the catalog, the
templates and the cache.

The catalog is a possibly out-of-date list of all released components for
every ET application.  Each component is formally identified by a 40-digit
hexidecimal SHA-1 hash value.  Along with that is an
application_ID:destination_path dictionary (the other kind of hash :)), and
possibly informal names for the components themselves.  The canonical catalog
is maintained at Envision.  It is add-only, as once things go in, they stay
in.  The catalogs onsite with the installations are complete in that they
contain descriptors for all properly patched components on the system, but
they may not be up to date with respect to the latest version of the catalog.
Catalogs are versioned with integers, with each patch incrementing the version
by 1.  In this way when a system is scanned and the details sent back to
Envision for troubleshooting, the same catalog that was used onsite can be
recovered if necessary.

<aside>
Note, because of the way hashes work, two components with the same content
(but not necessarily the same name) have the same hash value.  So the hash
value is reusable within an application and potentially even between
applications.  In fact, if we didn't use it this way we'd wind up with
collisions and other trouble.

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


[cache file format]
The goal here is that each entry of the cache fully describes a single
component for the purposes of patching.  Each component needs a formal identifier
based on the component's contents (NOT it's name), and an informal identifier for
the users of the system.

It also needs some dependency information, and this is where things get
tricky.  First, there are two kinds of dependencies: required and optional.
Second, dependencies can be considered bi-directional:

# Scenario 1
# fileA -> fileB
# fileA <- fileB

We care only about one-directional dependencies, in other words, from the
point of view of the file itself.  With this view, Scenario 1 is actually two
one-directional dependencies, rather than two halves of the same dependency:

# Scenario 2
# fileA -> fileB
# fileB -> fileA

<TODO: I don't recall what I was thinking of here.>
Finally, there is dependency in terms of context: are we talking about
dependency in the general (e.g., reference catalog) sense, or dependency on
the user's system?
</TODO>

For example, the pdb for a dll is an optional dependency from

[running the pkgmanager]
First you need to create the catalog.  For this you need a set of files.
Usually, but not always, this will be an installed but unmodified release.
The tool will walk the directory structure, collecting files and generating
hashes for each, relative to the application root.  The hash is the formal
identifier for a component.  Some kind of informal identifier will be stored in the
catalog as well.

    # unresolved aside: what to use for the informal identifier?
    #
    # First I thought of using the bare filename appended with _1, _2, _3,
    # etc., for subsequent files of the same name in different (relative)
    # locations.  But this defines a relationship, however tenuous, between
    # unrelated components.  I'd rather not go this route unless nothing better
    # comes along.
    #
    # Next I thought of using the bare file name plus ${__path_to_file}, but
    # this naming scheme is misleading for the second and subsequent components
    # with the same contents but different locations from the first (which has
    # its path in the component's informal name).
    #
    # I haven't come up with anything else yet.

