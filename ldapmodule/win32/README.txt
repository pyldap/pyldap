$Id: README.txt,v 1.1.1.1 2000/02/01 05:41:34 leonard Exp $

Windows users should not forget to check that the directory containing the
ldap.pyd file is in their PYTHONPATH.

Also, you need LDAP32.DLL in your PATH 
(available from ftp://terminator.rs.itd.umich.edu/ldap/windows/)

Here is Mauro Cicognini's original post to comp.lang.python (abbreviated):

------------------------------------------------------------
From mcicogni@siosistemi.it Wed Feb 10 10:11:54 1999
Date: Mon, 08 Feb 1999 12:47:50 +0100
From: Mauro Cicognini <mcicogni@siosistemi.it>
To: PSA MEMBERS <psa-members@python.org>
Cc: Fredrik Lundh <fredrik@pythonware.com>,
     David Leonard <David.Leonard@csee.uq.edu.au>
Newsgroups: comp.lang.python
Subject: Re: Compiling LDAP under WIN32

[...]

I attach a ZIP file containing everything one should need to build the
module under WIN32, and also the compiled binaries as a convenience.
The makefiles are in the format of a MSVC 6.0 workspace and project. I
also include an exported makefile (and the dependency file) but I
haven't tested it, and used the native files to build the module.

These assume to reside in a "win32" subdirectory of the "ldapmodule"
directory which is created by the standard distribution, and that there
are the distributions of Python 1.5.1 and the UMich LDAP in two
directories parallel to ldapmodule, i.e.
    .--|
       |-- ldapmodule
       |    |
       |    |-- win32
       |
       |-- python-1.5.1
       |
       |-- UMichLDAP

In fact the only things that matter about Python and UMich LDAP are the
include and library files, so I'm sure that anyone interested can tweak
the makefiles to find them wherever they wish.

[...]

Thanx to everybody

Mauro Cicognini

------------------------------------------------------------
In fact you (obviously?) need to have UMich's LDAP client library somewhere on
your PATH... which is exactly what the python module is looking for. Under UN*X
it's a shared object, under M$WIN it's a DLL called LDAP32.DLL.
[...]
Anyway, the UMich distribution of their LDAP library already includes the
pre-compiled Windows binaries: it even has the 16-bit and static library
versions. If the guy doesn't already have the DLL, he only needs to download
the archive from UMich, decompress it, look for LDAP32.DLL and copy it on his
PATH. If he already has it and he didn't know that DLLs need to be on the PATH
he's really a rookie... any OS needs to have some way to find the executables.
[...]

Mauro

