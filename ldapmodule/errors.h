/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */
/* $Id: errors.h,v 1.1.1.1 2000/02/01 05:41:27 leonard Exp $ */

#ifndef __h_errors_
#define __h_errors_

#include "Python.h"
#include "lber.h"
#include "ldap.h"

extern PyObject* LDAPexception_class;
extern PyObject* LDAPerror( LDAP*, char*msg );
extern void LDAPinit_errors( PyObject* );

#endif /* __h_errors */
