from __future__ import unicode_literals

import sys

if sys.version_info[0] <= 2:
    PY2 = True
    text_type = unicode
else:
    PY2 = False
    text_type = str

import ldap, unittest
from . import slapd

from ldap.ldapobject import LDAPObject

server = None


class EditionTests(unittest.TestCase):

    def setUp(self):
        global server
        if server is None:
            server = slapd.Slapd()
            server.start()
            base = server.get_dn_suffix()

            # insert some Foo* objects via ldapadd
            server.ldapadd("\n".join([
                "dn: cn=Foo1,"+base,
                "objectClass: organizationalRole",
                "cn: Foo1",
                "",
                "dn: cn=Foo2,"+base,
                "objectClass: organizationalRole",
                "cn: Foo2",
                "",
                "dn: cn=Foo3,"+base,
                "objectClass: organizationalRole",
                "cn: Foo3",
                "",
                "dn: ou=Container,"+base,
                "objectClass: organizationalUnit",
                "ou: Container",
                "",
                "dn: cn=Foo4,ou=Container,"+base,
                "objectClass: organizationalRole",
                "cn: Foo4",
                "",
            ])+"\n")

        l = LDAPObject(server.get_url(), bytes_mode=False)
        l.protocol_version = 3
        l.set_option(ldap.OPT_REFERRALS,0)
        l.simple_bind_s(server.get_root_dn(), 
                server.get_root_password())
        self.ldap = l
        self.server = server

    def test_add_object(self):
        base = self.server.get_dn_suffix()
        dn = "cn=Added,ou=Container," + base
        self.ldap.add_ext_s(dn, [
            ("objectClass", [b'organizationalRole']),
            ("cn", [b'Added']),
        ])

        # Lookup the object
        result = self.ldap.search_s(base, ldap.SCOPE_SUBTREE, '(cn=Added)', ['*'])
        self.assertEqual(result, [
            ("cn=Added,ou=Container," + base,
                {'cn': [b'Added'], 'objectClass': [b'organizationalRole']}),
        ])


if __name__ == '__main__':
    unittest.main()
