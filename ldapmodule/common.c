/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */

/*
 * Miscellaneous common routines
 * $Id: common.c,v 1.1.1.1 2000/02/01 05:41:19 leonard Exp $
 */

#include "common.h"

/* dynamically add the methods into the module dictionary d */

void
LDAPadd_methods( PyObject* d, PyMethodDef* methods ) 
{
    PyMethodDef *meth;

    for( meth = methods; meth->ml_meth; meth++ ) {
        PyObject *f = PyCFunction_New( meth, NULL );
        PyDict_SetItemString( d, meth->ml_name, f );
        Py_DECREF(f);
    }
}
