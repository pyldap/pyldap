/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */

/*	$Id: CIDict.c,v 1.1.1.1 2000/02/01 05:41:08 leonard Exp $	*/

#include "common.h"
#ifdef USE_CIDICT

/*
 * Case Insensitive dictionary
 *
 * e.g:
 *	>>> foo['Bar'] = 123
 *	>>> print foo['baR']
 *	123
 *
 * This dictionary can be used to hold the replies returned by
 * case-insensitive X.500 directory services, without the
 * caller having to know what case it has converted everything to.
 *
 * XXX I forget whose idea this originally was, but its a good one. - d
 */

#include "Python.h"

/*
 * Return a new object representing a lowercased version of the argument.
 * Typically this is a string -> string conversion.
 */
static PyObject *
case_insensitive(PyObject *o)
{
	char *str, *cp;
	int len, i;
	PyObject *s;

	if (o == NULL)
		return NULL;

	if (!PyString_Check(o)) {
		Py_INCREF(o);
		return o;
	}

	str = PyString_AS_STRING(o);
	len = PyString_GET_SIZE(o);
	cp = malloc(len);
	for (i = 0; i < len; i++)
		cp[i] = tolower(str[i]);
	s = PyString_FromString(cp);
	free(cp);
	return s;
}

/* read-access the dictionary after lowecasing the subscript */

static PyObject *
cid_subscript(PyObject *d, PyObject *k)
{
	PyObject *ret;
	PyObject *cik;

	cik = case_insensitive(k);
	ret = (*PyDict_Type.tp_as_mapping->mp_subscript)(d, cik);
	Py_XDECREF(cik);
	return ret;
}

/* write-access the dictionary after lowecasing the subscript */

static int
cid_ass_subscript(PyObject *d, PyObject *k, PyObject *v)
{
	int ret;
	PyObject *cik;

	cik = case_insensitive(k);
	ret = (*PyDict_Type.tp_as_mapping->mp_ass_subscript)(d, cik, v);
	Py_XDECREF(cik);
	return ret;
}

/* This type and mapping structure gets filled in from the PyDict structs */
 
static PyMappingMethods CIDict_mapping;
PyTypeObject CIDict_Type;

/* Initialise the case-insensitive dictionary type */

static void
CIDict_init()
{
	/*
	 * Duplicate the standard python dictionary type, 
	 * but override the subscript accessor methods
	 */
	memcpy(&CIDict_Type, &PyDict_Type, sizeof CIDict_Type);
	CIDict_Type.tp_name = "cidictionary";
	CIDict_Type.tp_as_mapping = &CIDict_mapping;

	memcpy(&CIDict_mapping, PyDict_Type.tp_as_mapping, 
		sizeof CIDict_mapping);
	CIDict_mapping.mp_subscript = cid_subscript;
	CIDict_mapping.mp_ass_subscript = cid_ass_subscript;
}

/* Create a new case-insensitive dictionary, based on PyDict */

PyObject *
CIDict_New()
{
	PyObject *mp;
	static int initialised = 0;

	if (!initialised) {
		CIDict_init();
		initialised = 1;
	}
		
	mp = PyDict_New();
	mp->ob_type = &CIDict_Type;
	return (mp);
}

#endif USE_CIDICT
