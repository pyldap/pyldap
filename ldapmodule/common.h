/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */
/*
 * common utility macros
 *
 * $Id: common.h,v 1.1.1.1 2000/02/01 05:41:19 leonard Exp $ 
 */

#ifndef __h_common 
#define __h_common 

#ifndef WIN32
#include "config.h"
#include <netdb.h>
#include <sys/time.h>
#include <sys/types.h>
#else
#include <winsock.h>
#endif
#include <string.h>
#define streq( a, b ) \
	( (*(a)==*(b)) && 0==strcmp(a,b) )

#include "Python.h"
void LDAPadd_methods( PyObject*d, PyMethodDef*methods );
#define PyNone_Check(o) ( o == Py_None )

#endif /* __h_common_ */

