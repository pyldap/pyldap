#! /bin/sh
#
# David Leonard, <david.leonard@csee.uq.edu.au> 1999. Public domain.
#
# This script provides a simple way of downloading, configuring, and
# building OpenLDAP 1.2.7 for use with the Python ldapmodule.
# Run this script first and then run the configure script in the ldapmodule
# directory (it will notice that this script has been run.)
#
# $Id: openldap.sh,v 1.1.1.1 2000/02/01 05:41:27 leonard Exp $

# Edit these if you need to
PREFIX=/tmp/ldap-pfx
PYTHON=python
GZIP=gzip
MAKE=make
LYNX=lynx

case "$1" in
  -alpha)
    SRCDIR=openldap-2.0-alpha3
    OPENLDAP="openldap-alpha/${SRCDIR}"
    MD5HASH=0f08e59f5dd8a9b70ddc6bddb40d21d7
    ;;
  *)
    SRCDIR=ldap
    OPENLDAP=openldap-release/openldap-1.2.7
    MD5HASH=be5866cfa50fdf083f5230b3837181e8
    ;;
esac

#URL="http://mirror.aarnet.edu.au/pub/OpenLDAP/${OPENLDAP}.tgz"
URL="ftp://ftp.openldap.org/pub/OpenLDAP/${OPENLDAP}.tgz"
CONFIGURE_ARGS="--disable-slapd --disable-slurpd --disable-libui --without-threads --disable-shared"

set -e

#
# try downloading a file using either Python's urllib, or lynx.
#
download () {
	URL="$1"
	TMPFILE="$2"

	trap 'rm -f "${TMPFILE}"; exit 1' 0 1 2

	#-- try python first
	if ${PYTHON} -c 'import sys, urllib, mimetools; mimetools.copybinary(urllib.urlopen(sys.argv[1]), sys.stdout)' "${URL}" >"${TMPFILE}"; then
		: success
	#-- try lynx next
	#   XXX sometimes lynx will decode using the Content-Encoding
	#       header added by some WWW proxies..
	elif ${LYNX} -source "${URL}" >"${TMPFILE}"; then
		: possible success
	#-- give up
	else
		echo "Could not use ${PYTHON} or ${LYNX} to download ${URL}"
		exit 1
	fi

	trap exit 0 1 2 2>/dev/null
	trap >/dev/null 2>/dev/null
}

#-- compute the md5 checksum of a file
md5 () {
	${PYTHON} -c 'import sys, md5, string; print string.join(map(lambda x:"%02x"%ord(x), md5.new(sys.stdin.read()).digest()),"")' <"$1" >"$2"
}

#-- make directories to 'install' openldap into
for d in lib include src; do
    if test '!' -d "${PREFIX}/$d"; then
	echo "@@ creating directory ${PREFIX}/$d"
    	mkdir -p "${PREFIX}/$d"
    fi
done

#-- download the openldap distribution
if test '!' -f "${PREFIX}.tar.gz"; then
    echo "@@ downloading ${URL} into ${PREFIX}.tar.gz ..."
    download "${URL}" "${PREFIX}.tar.gz"
fi

#-- check the MD5 hash of the ldap distribution 
if test '!' -z "${MD5HASH}"; then
	echo "@@ checking ${PREFIX}.tar.gz checksum ..."
	if md5 "${PREFIX}.tar.gz" "${PREFIX}.tar.gz.md5"; then
		if test x"${MD5HASH}" != x`cat "${PREFIX}.tar.gz.md5"`; then
		    echo " *** FILE MAY BE CORRUPTED"
		    echo " *** ${MD5HASH} != `cat ${PREFIX}.tar.gz.md5`"
		    exit 1
		fi
	else
		echo "(Could not generate MD5 checksum to check.)"
	fi
fi

#-- extract the distribution into .../src
if test '!' -f "${PREFIX}/src/${SRCDIR}/include/ldap.h"; then
    echo "@@ extracting ${URL} into ${PREFIX}/src ..."
    (cd "${PREFIX}/src"; ${GZIP} -dc | tar fx -) < "${PREFIX}.tar.gz" 
    echo "@@ putting sane permissions on source files"
    chmod -R u+w "${PREFIX}/src"
fi

cd "${PREFIX}/src/${SRCDIR}"

#-- configure
if test '!' -f "${PREFIX}/src/${SRCDIR}/config.status"; then
    echo "@@ configuring with --prefix=${PREFIX} ${CONFIGURE_ARGS}"
    sh ./configure --prefix="${PREFIX}" ${CONFIGURE_ARGS}
fi

#-- build and install the very smallest bits
if test '!' -f ${PREFIX}/include/ldap.h; then
    echo "@@ building includes"
    (cd include && ${MAKE} && ${MAKE} install)
fi
if test '!' -f ${PREFIX}/lib/liblber.a; then
    echo "@@ building basic encoding routines library"
    (cd libraries/liblber && ${MAKE} && ${MAKE} install)
fi
if test '!' -f ${PREFIX}/lib/libldap.a; then
    echo "@@ building ldap library"
    (cd libraries/libldap && ${MAKE} && ${MAKE} install)
fi

#-- mention to the user
echo "@@ It all seems to be done."
if test x"/tmp/ldap-pfx" != x"${PREFIX}"; then
    echo "You should now configure ldap module with --with-ldap=${PREFIX}"
    echo "and then type 'make'."
else
    echo "You should now run 'configure' and then type 'make'."
fi
echo "Later, you can delete ${PREFIX}.tar.gz and ${PREFIX}"

exit 0
