# For documentation, see comments in Module/LDAPObject.c and the
# pyldap.sasl module documentation.
from __future__ import print_function

import pyldap,pyldap.sasl

pyldap.sasl._trace_level=0

pyldap.set_option(pyldap.OPT_DEBUG_LEVEL,0)

for ldap_uri,sasl_mech,sasl_cb_value_dict in [
  (
    "ldap://nb2.stroeder.local:1390/",
    'CRAM-MD5',
    {
      pyldap.sasl.CB_AUTHNAME    :'fred',
      pyldap.sasl.CB_PASS        :'secret',
    }
  ),
  (
    "ldap://nb2.stroeder.local:1390/",
    'PLAIN',
    {
      pyldap.sasl.CB_AUTHNAME    :'fred',
      pyldap.sasl.CB_PASS        :'secret',
    }
  ),
  (
    "ldap://nb2.stroeder.local:1390/",
    'LOGIN',
    {
      pyldap.sasl.CB_AUTHNAME    :'fred',
      pyldap.sasl.CB_PASS        :'secret',
    }
  ),
  (
    "ldapi://%2Ftmp%2Fopenldap-socket/",
    'EXTERNAL',
    { }
  ),
  (
    "ldap://nb2.stroeder.local:1390/",
    'GSSAPI',
    { }
  ),
  (
    "ldap://nb2.stroeder.local:1390/",
    'NTLM',
    {
      pyldap.sasl.CB_AUTHNAME    :'fred',
      pyldap.sasl.CB_PASS        :'secret',
    }
  ),
  (
    "ldap://nb2.stroeder.local:1390/",
    'DIGEST-MD5',
    {
      pyldap.sasl.CB_AUTHNAME    :'fred',
      pyldap.sasl.CB_PASS        :'secret',
    }
  ),
]:
  sasl_auth = pyldap.sasl.sasl(sasl_cb_value_dict,sasl_mech)
  print(20*'*',sasl_auth.mech,20*'*')
  # Open the LDAP connection
  l = pyldap.initialize(ldap_uri,trace_level=0)
  # Set protocol version to LDAPv3 to enable SASL bind!
  l.protocol_version = 3
  try:
    l.sasl_interactive_bind_s("", sasl_auth)
  except pyldap.LDAPError as e:
    print('Error using SASL mechanism',sasl_auth.mech,str(e))
  else:
    print('Sucessfully bound using SASL mechanism:',sasl_auth.mech)
    try:
      print('Result of Who Am I? ext. op:',repr(l.whoami_s()))
    except pyldap.LDAPError as e:
      print('Error using SASL mechanism',sasl_auth.mech,str(e))
    try:
      print('OPT_X_SASL_USERNAME',repr(l.get_option(pyldap.OPT_X_SASL_USERNAME)))
    except AttributeError:
      pass

  l.unbind()
  del l
