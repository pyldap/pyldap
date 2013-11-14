/* See http://www.python-ldap.org/ for details.
 * $Id: ldapmodule.c,v 1.9 2009/04/17 12:19:09 stroeder Exp $ */

#include "common.h"
#include "version.h"
#include "constants.h"
#include "errors.h"
#include "functions.h"
#include "schema.h"
#include "ldapcontrol.h"

#include "LDAPObject.h"

PyMODINIT_FUNC PyInit__ldap(void);

/* dummy module methods */

static PyMethodDef methods[]  = {
	{ NULL, NULL }
};

/* module initialisation */


PyMODINIT_FUNC
PyInit__ldap()
{
	PyObject *m, *d;

#if defined(MS_WINDOWS) || defined(__CYGWIN__)
	LDAP_Type.ob_type = &PyType_Type;
#endif

	/* Create the module and add the functions */
#if PY_MAJOR_VERSION >= 3
        static struct PyModuleDef ldap_moduledef = {
                PyModuleDef_HEAD_INIT,
                "_ldap",              /* m_name */
                "",                   /* m_doc */
                -1,                   /* m_size */
                methods,              /* m_methods */
        };
        m = PyModule_Create(&ldap_moduledef);
#else
	m = Py_InitModule("_ldap", methods);
#endif

        PyType_Ready(&LDAP_Type);

	/* Add some symbolic constants to the module */
	d = PyModule_GetDict(m);

	LDAPinit_version(d);
	LDAPinit_constants(d);
	LDAPinit_errors(d);
	LDAPinit_functions(d);
	LDAPinit_schema(d);
	LDAPinit_control(d);

	/* Check for errors */
	if (PyErr_Occurred())
		Py_FatalError("can't initialize module _ldap");

        return m;
}
