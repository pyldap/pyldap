/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */

/*
 * errors that arise from ldap use
 * $Id: errors.c,v 1.1.1.1 2000/02/01 05:41:27 leonard Exp $
 *
 * Most errors become their own exception
 */

#include "common.h"
#include "errors.h"

/* the base exception class */

PyObject*
LDAPexception_class;

/* list of error objects */

#define NUM_LDAP_ERRORS		LDAP_NO_MEMORY+1
static PyObject* 
errobjects[ NUM_LDAP_ERRORS ];

/* convert an LDAP error into a python exception */

PyObject*
LDAPerror( LDAP*l, char*msg ) 
{
	if (l == NULL) {
		PyErr_SetFromErrno( LDAPexception_class );
	} else {
		int errnum;
		PyObject* errobj;
		PyObject *info;

#ifdef LDAP_TYPE_IS_OPAQUE
		PyErr_SetString(LDAPexception_class,
			"unknown error (C API does not expose error)");
#else
		errnum = l->ld_errno;
		if (errnum<0 || errnum>=NUM_LDAP_ERRORS)
		    	Py_FatalError("LDAPerror - invalid error");

		errobj = errobjects[errnum];
		
		if (errnum == LDAP_NO_MEMORY)
			PyErr_NoMemory();

		info = PyDict_New();

		PyDict_SetItemString( info, "desc", 
				PyString_FromString(ldap_err2string(errnum)));

		if (l->ld_matched != NULL && *l->ld_matched != '\0') 
		   PyDict_SetItemString( info, "matched", 
		   		PyString_FromString(l->ld_matched) );

		if (l->ld_error != NULL && *l->ld_error != '\0') 
		   PyDict_SetItemString( info, "info", 
		   		PyString_FromString(l->ld_error) );
		PyErr_SetObject( errobj, info );
#endif
	}
	return NULL;
}


/* initialisation */

void
LDAPinit_errors( PyObject*d ) {
        
        /* create the base exception class */
        LDAPexception_class = PyErr_NewException("ldap.LDAPError",
                                                  NULL,
                                                  NULL);
        PyDict_SetItemString( d, "LDAPError", LDAPexception_class );

	/* XXX - backward compatibility with pre-1.8 */
        PyDict_SetItemString( d, "error", LDAPexception_class );
	Py_INCREF( LDAPexception_class );

	/* create each LDAP error object */

#	define seterrobj2(n,o) \
		PyDict_SetItemString( d, #n, (errobjects[LDAP_##n] = o) ); \
		Py_INCREF( errobjects[LDAP_##n] )


#	define seterrobj(n) \
		seterrobj2( n, PyErr_NewException("ldap." #n, \
                                                  LDAPexception_class, \
                                                  NULL))

#	define seterrobjas(n,existing) \
		seterrobj2( n, existing )

	seterrobj(SUCCESS);
	seterrobj(OPERATIONS_ERROR);
	seterrobj(PROTOCOL_ERROR);
	seterrobj(TIMELIMIT_EXCEEDED);
	seterrobj(SIZELIMIT_EXCEEDED);
	seterrobj(COMPARE_FALSE);
	seterrobj(COMPARE_TRUE);
#ifdef LDAP_STRONG_AUTH_NOT_SUPPORTED
	seterrobj(STRONG_AUTH_NOT_SUPPORTED);
#endif
	seterrobj(STRONG_AUTH_REQUIRED);
	seterrobj(PARTIAL_RESULTS);
	/* seterrobjas(NO_SUCH_ATTRIBUTE, PyExc_AttributeError); */
	seterrobj(NO_SUCH_ATTRIBUTE);
	seterrobj(UNDEFINED_TYPE);
	seterrobj(INAPPROPRIATE_MATCHING);
	seterrobj(CONSTRAINT_VIOLATION);
	seterrobj(TYPE_OR_VALUE_EXISTS);
	seterrobj(INVALID_SYNTAX);
	/* seterrobjas(NO_SUCH_OBJECT, PyExc_NameError); */
	seterrobj(NO_SUCH_OBJECT);
	seterrobj(ALIAS_PROBLEM);
	seterrobj(INVALID_DN_SYNTAX);
	seterrobj(IS_LEAF);
	seterrobj(ALIAS_DEREF_PROBLEM);
	seterrobj(INAPPROPRIATE_AUTH);
	seterrobj(INVALID_CREDENTIALS);
	seterrobj(INSUFFICIENT_ACCESS);
	seterrobj(BUSY);
	seterrobj(UNAVAILABLE);
	seterrobj(UNWILLING_TO_PERFORM);
	seterrobj(LOOP_DETECT);
	seterrobj(NAMING_VIOLATION);
	seterrobj(OBJECT_CLASS_VIOLATION);
	seterrobj(NOT_ALLOWED_ON_NONLEAF);
	seterrobj(NOT_ALLOWED_ON_RDN);
	seterrobj(ALREADY_EXISTS);
	seterrobj(NO_OBJECT_CLASS_MODS);
	seterrobj(RESULTS_TOO_LARGE);
	seterrobj(OTHER);
	seterrobj(SERVER_DOWN);
	seterrobj(LOCAL_ERROR);
	seterrobj(ENCODING_ERROR);
	seterrobj(DECODING_ERROR);
	seterrobj(TIMEOUT);
	seterrobj(AUTH_UNKNOWN);
	seterrobj(FILTER_ERROR);
	seterrobj(USER_CANCELLED);
	/* seterrobjas(PARAM_ERROR, PyExc_ValueError); */
	seterrobj(PARAM_ERROR);
	seterrobj(NO_MEMORY);
}
