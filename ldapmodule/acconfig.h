/* $Id: acconfig.h,v 1.1.1.1 2000/02/01 05:41:19 leonard Exp $ */

/*
 * Case-insensitive dictionary used for evil LDAP server responses
 */
#undef USE_CIDICT

/*
 * ldap_set_rebind_proc() with three arguments (Solaris, not OpenLDAP)
 */
#undef LDAP_SET_REBIND_PROC_3ARGS

/*
 * 'LDAP' is an opaque data type, struct ldap, in ldap.h (iSolaris, Netscape)
 */
#undef LDAP_TYPE_IS_OPAQUE


#undef HAVE_LDAP_MODRDN2_S
#undef HAVE_LDAP_MODRDN2
 
