from __future__ import print_function
import pyldap,ldapurl,pprint

from pyldap.controls import LDAPControl,BooleanControl

l = pyldap.initialize('ldap://localhost:1390',trace_level=2)

print(60*'#')

pprint.pprint(l.get_option(pyldap.OPT_SERVER_CONTROLS))
l.manage_dsa_it(1,1)
pprint.pprint(l.get_option(pyldap.OPT_SERVER_CONTROLS))
print(60*'#')

# Search with ManageDsaIT control (which has no value)
pprint.pprint(l.search_ext_s(
  'cn=Test-Referral,ou=Testing,dc=stroeder,dc=de',
  pyldap.SCOPE_BASE,
  '(objectClass=*)',
  ['*','+'],
  serverctrls = [ LDAPControl('2.16.840.1.113730.3.4.2',1,None) ],
))
print(60*'#')

# Search with Subentries control (which has boolean value)
pprint.pprint(l.search_ext_s(
  'dc=stroeder,dc=de',
  pyldap.SCOPE_SUBTREE,
  '(objectClass=subentry)',
  ['*','+'],
  serverctrls = [ BooleanControl('1.3.6.1.4.1.4203.1.10.1',1,1) ],
))

print(60*'#')
