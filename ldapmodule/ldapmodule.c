/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */
/* 
 * LDAP module
 * $Id: ldapmodule.c,v 1.1.1.1 2000/02/01 05:41:27 leonard Exp $
 */

#include "version.h"
#include "common.h"
#include "constants.h"
#include "errors.h"
#include "functions.h"
/* #include "string_translators.h" */

#include "Python.h"
#include "LDAPObject.h"

/* dummy module methods */

static PyMethodDef methods[]  = {
	{ NULL, NULL }
};

/* module initialisation */

void
initldap()
{
	PyObject *m, *d;

#ifdef WIN32
	/* See http://www.python.org/doc/FAQ.html#3.24 */
	LDAP_Type.ob_type = &PyType_Type;
#endif

	/* Create the module and add the functions */
	m = Py_InitModule("ldap", methods);

	/* Add some symbolic constants to the module */
	d = PyModule_GetDict(m);

	LDAPinit_version(d);
	LDAPinit_constants(d);
	LDAPinit_errors(d);
	LDAPinit_functions(d);
/*	LDAPinit_string_translators(d); */

	/* Check for errors */
	if (PyErr_Occurred())
		Py_FatalError("can't initialize module ldap");
}
