#!/bin/ksh
# $Id: make-tar.sh,v 1.1.1.1 2000/02/01 05:41:27 leonard Exp $
#
# Create a tar file for distribution .. and install it in the web area
#

print () { awk 'END {printf(w);}' w="$1" </dev/null ; }

OLD_VERSION=`tr -d \" < version_str.h`

if [ "X$1" != "X-force" ]; then
    echo "The current version is: $OLD_VERSION"
    print "What should it be now? [$OLD_VERSION]: "
    read new_version
    if test -z "$new_version"; then 
	    new_version="$OLD_VERSION"; 
    else
	    echo '"'$new_version'"' > version_str.h
	    cvs commit -m "version $new_version" version_str.h
    fi

else
    new_version="$OLD_VERSION"
    echo "version: $new_version"
fi

VERSION="RELEASE_`echo "$new_version" | tr -c '\n0-9A-Za-z' _ `" #"
echo "new version is $new_version, release is $VERSION"

if [ "X$1" != "X-force" ]; then
    echo "checking to see if you have committed everything..."
    DIFF=/tmp/diff
    cvs diff -u 2>/dev/null >$DIFF
    if test -s "$DIFF"; then
	    echo "You haven't committed! see $DIFF for details"
	    grep '^[+][+][+]' $DIFF
	    : exit 1
    else
	    rm $DIFF 
    fi

fi

echo "cleaning..."
sh clean.sh

echo "autoconfiguring..."
if autoheader && autoconf; then
	: ok
else
	echo "autoconf failed!!"
	exit 1
fi

if test "X$1" != "X-force"; then
  echo "checking to see if it will build after being cleaned..."
  if  sh openldap.sh && configure && make -f Makefile.pre.in boot && make distclean && make -f Makefile.pre.in boot && make && (cd Doc && make clean && make) && python -c 'import ldap; print ldap.__doc__'; then
	: ok
else
	echo "makes failed!"
	if [ "X$1" != "X-force" ]; then 
	        echo "i refuse to commit."
		exit 1
	else
		echo ".. but you're forcing me to continue"
	fi
fi
fi

# tar the distribution up

TAR=/opt/local/gnu/bin/tar
WEBDIR=/homes/leonard/www/dc-prj/ldapmodule
TARFILE="${WEBDIR}/ldapmodule-${new_version}-alpha.tar.gz"

echo "creating $TARFILE"
( cd ..
  chmod +x ldapmodule/openldap.sh
  ${TAR} fcvz ${TARFILE} \
	`find ldapmodule \
	     -name 'CVS' -prune -o \
	     '(' \
	        '!' -type d \
	        '!' -name '*~' \
	        '!' -name '*.o' \
	        '!' -name '*.a' \
	        '!' -name '*.so' \
	        '!' -name '*.ps' \
	        '!' -name '*.sl' \
	        '!' -name 'so_locations' \
	        '!' -name '.nfs*' \
	        '!' -name 'config.?' \
	        '!' -name 'sedscript' \
	        '!' -name 'Setup' \
	        '!' -name 'Setup.in' \
	        '!' -name 'python' \
	        '!' -name 'core' \
	        '!' -name 'tags' \
	        '!' -name '*.swp' \
	        '!' -name 'Makefile' \
	        '!' -name 'Makefile.pre' \
	        '!' -name 'Makefile.pre.in' \
	        '!' -name 'make-tar.sh' \
	        '!' -name 'clean.sh' \
	        '!' -name '*.aux' \
	        '!' -name '*.dvi' \
	        '!' -name '*.idx' \
	        '!' -name '*.log' \
	     ')' \
	     -print | sort`
)

cp CHANGES ${WEBDIR}/
cp README ${WEBDIR}/

ls -l "$TARFILE" ${WEBDIR}/CHANGES ${WEBDIR}/README

# tag the committed files
echo "tagging files"
cvs -q tag -F $VERSION

# copy the PDF file
echo "copying Doc.pdf"
cp Doc/Doc.pdf $WEBDIR/

# rebuild the web page
echo "rebuilding index file"
( cd $WEBDIR; ./home.html.pl )

echo "*** Don't forget to rename $TARFILE"
