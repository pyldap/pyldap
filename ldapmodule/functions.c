/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */

/* 
 * functions - functions available at the module level
 * $Id: functions.c,v 1.1.1.1 2000/02/01 05:41:27 leonard Exp $
 */

#include "common.h"
#include "functions.h"
#include "LDAPObject.h"
#include "errors.h"

/* ldap_open */

static PyObject*
l_ldap_open(PyObject* unused, PyObject *args)
{
    char *host;
    int port = 0;
    LDAP *ld;

    if (!PyArg_ParseTuple(args, "s|i", &host, &port))
    	return NULL;

    /* Look up the ldap service from /etc/services if not port not given. */
    if (port == 0) {
#ifdef WIN32
	port = LDAP_PORT;
#else
        struct servent *se = getservbyname("ldap", "tcp");
	if (se != NULL)
	    port = ntohs(se->s_port);
	else
	    port = LDAP_PORT;
#endif
    }

    Py_BEGIN_ALLOW_THREADS
    ld = ldap_open(host, port);
    Py_END_ALLOW_THREADS
    if (ld == NULL)
    	return LDAPerror(ld, "ldap_open");
    return (PyObject*)newLDAPObject(ld);
}

static char doc_open[] = 
"open(host [,port=PORT]) -> LDAPObject\n\n"
"\tOpens a new connection with an LDAP server, and returns an LDAP object\n"
"\trepresentative of this.";

/* ldap_dn2ufn */

static PyObject*
l_ldap_dn2ufn( PyObject* unused, PyObject *args )
{
    char *dn;
    char *ufn;
    PyObject *result;

    if (!PyArg_ParseTuple( args, "s", &dn )) return NULL;

    ufn = ldap_dn2ufn(dn);
    if (ufn == NULL) {
    	PyErr_NoMemory();
	return NULL;
    }
    result = PyString_FromString( ufn );
    free(ufn);
    return result;
}

static char doc_dn2ufn[] =
"dn2ufn(dn) -> string\n\n"
"\tTurns the DN into a more user-friendly form, stripping off type names.\n"
"\tSee RFC 1781 ``Using the Directory to Achieve User Friendly Naming''\n"
"\tfor more details on the UFN format.";

/* ldap_explode_dn */

static PyObject*
l_ldap_explode_dn( PyObject* unused, PyObject *args )
{
    char *dn;
    int notypes = 0;
    char **exploded;
    PyObject *result;
    int i;

    if (!PyArg_ParseTuple( args, "s|i", &dn, &notypes )) return NULL;

    exploded = ldap_explode_dn(dn, notypes);

    if (exploded == NULL) 
    	return LDAPerror(NULL,"ldap_explode_dn");

    result = PyList_New(0);
    for(i=0; exploded[i]; i++)
    	PyList_Append( result, PyString_FromString( exploded[i] ) );

    ldap_value_free(exploded);
    return result;
}

static char doc_explode_dn[] =
"explode_dn(dn [, notypes=0]) -> list\n\n"
"\tThis function takes the DN and breaks it up into its component parts.\n"
"\tEach part is known as an RDN (Relative Distinguished Name). The notypes\n"
"\tparameter is used to specify that only the RDN values be returned\n"
"\tand not their types. For example, the DN \"cn=Bob, c=US\" would be\n"
"\treturned as either [\"cn=Bob\", \"c=US\"] or [\"Bob\",\"US\"]\n"
"\tdepending on whether notypes was 0 or 1, respectively.";

/* ldap_is_ldap_url */

static PyObject*
l_ldap_is_ldap_url( PyObject* unused, PyObject *args )
{
    char *url;

    if (!PyArg_ParseTuple( args, "s", &url )) return NULL;
    return PyInt_FromLong( ldap_is_ldap_url( url ));
}

static char doc_is_ldap_url[] = 
"is_ldap_url(url) -> int\n\n"
"\tThis function returns true if url `looks like' an LDAP URL\n"
"\t(as opposed to some other kind of URL).";

/* methods */

static PyMethodDef methods[] = {
    { "open",		(PyCFunction)l_ldap_open,		METH_VARARGS,
    	doc_open },
    { "dn2ufn",		(PyCFunction)l_ldap_dn2ufn,		METH_VARARGS,
    	doc_dn2ufn },
    { "explode_dn",	(PyCFunction)l_ldap_explode_dn,		METH_VARARGS,
    	doc_explode_dn },
    { "is_ldap_url",	(PyCFunction)l_ldap_is_ldap_url,	METH_VARARGS,
    	doc_is_ldap_url },
    { NULL, NULL }
};

/* initialisation */

void
LDAPinit_functions( PyObject* d ) {
    LDAPadd_methods( d, methods );
}
