/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */
/*
 * LDAPMessageObject - wrapper around an LDAPMessage*
 * $Id: message.c,v 1.1.1.1 2000/02/01 05:41:27 leonard Exp $
 */

#include "common.h"
#include "message.h"
#include "errors.h"
#include "CIDict.h"

PyObject*
LDAPmessage_to_python( LDAP*ld, LDAPMessage*m )
{
    /* we convert an LDAP message into a python structure.
     * It is always a list of dictionaries.
     */

     PyObject* result;
     int num_entries;
     int entry_index;
     LDAPMessage* entry;

     num_entries = ldap_count_entries( ld, m );
     result = PyList_New( num_entries );
     for( entry_index=0, entry=ldap_first_entry(ld,m);
          entry_index<num_entries && entry!=NULL;
	  entry_index++, entry=ldap_next_entry(ld,entry) )
     {
	 char *dn;
	 char *attr;
	 BerElement *ber;
	 PyObject* entrytuple; 
	 PyObject* attrdict; 

	 dn = ldap_get_dn( ld, entry );
	 if (dn == NULL) 
	     return LDAPerror( ld, "ldap_get_dn" );

	 entrytuple = PyTuple_New(2);
#ifdef USE_CIDICT
	 attrdict = CIDict_New();
#else /* use standard python dictionary */
	 attrdict = PyDict_New();
#endif /* !CIDICT */

	 PyTuple_SetItem( entrytuple, 0, PyString_FromString(dn) );
	 PyTuple_SetItem( entrytuple, 1, attrdict );

	 PyList_SetItem( result, entry_index, entrytuple );

	 for( attr = ldap_first_attribute( ld, entry, &ber );
	      attr != NULL;
	      attr = ldap_next_attribute( ld, entry, ber )
	 ) {
	     PyObject* valuelist;
	     struct berval ** bvals =
	     	ldap_get_values_len( ld, entry, attr );

	     if ( PyMapping_HasKeyString( attrdict, attr ) ) {
		 valuelist = PyMapping_GetItemString( attrdict, attr );
	     } else {
		 valuelist = PyList_New(0);
		 PyMapping_SetItemString( attrdict, attr, valuelist );
	     }

	     Py_INCREF( valuelist );
	     if (bvals != NULL) {
	        int i;
		for (i=0; bvals[i]; i++) {
		    PyObject *valuestr;

		    valuestr = PyString_FromStringAndSize( 
			    bvals[i]->bv_val, bvals[i]->bv_len 
			);
		    PyList_Append( valuelist, valuestr );
	    	}
	     	ber_bvecfree(bvals);
	     }
	     Py_DECREF( valuelist );
	 }
     }
     ldap_msgfree( m );
     return result;
}
