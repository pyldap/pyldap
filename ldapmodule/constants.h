/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */
#ifndef __h_constants_
#define __h_constants_

/* $Id: constants.h,v 1.1.1.1 2000/02/01 05:41:27 leonard Exp $ */

#include "Python.h"
extern void LDAPinit_constants( PyObject* d );
extern PyObject* LDAPconstant( int );

#endif /* __h_constants_ */
