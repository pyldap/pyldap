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

class TestSearch(unittest.TestCase):

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

    def test_reject_bytes_base(self):
        base = self.server.get_dn_suffix()
        l = self.ldap

        with self.assertRaises(TypeError):
            l.search_s(base.encode('utf-8'), ldap.SCOPE_SUBTREE, '(cn=Foo*)', ['*'])
        with self.assertRaises(TypeError):
            l.search_s(base, ldap.SCOPE_SUBTREE, b'(cn=Foo*)', ['*'])
        with self.assertRaises(TypeError):
            l.search_s(base, ldap.SCOPE_SUBTREE, '(cn=Foo*)', [b'*'])

    def test_search_keys_are_text(self):
        base = self.server.get_dn_suffix()
        l = self.ldap
        result = l.search_s(base, ldap.SCOPE_SUBTREE, '(cn=Foo*)', ['*'])
        result.sort()
        dn, fields = result[0]
        self.assertEqual(dn, 'cn=Foo1,%s' % base)
        self.assertEqual(type(dn), text_type)
        for key, values in fields.items():
            self.assertEqual(type(key), text_type)
            for value in values:
                self.assertEqual(type(value), bytes)

    def _get_bytes_ldapobject(self, explicit=True):
        if explicit:
            kwargs = {'bytes_mode': True}
        else:
            kwargs = {}
        l = LDAPObject(server.get_url(), **kwargs)
        l.protocol_version = 3
        l.set_option(ldap.OPT_REFERRALS,0)
        l.simple_bind_s(self.server.get_root_dn().encode('utf-8'),
                self.server.get_root_password().encode('utf-8'))
        return l

    @unittest.skipUnless(PY2, "no bytes_mode under Py3")
    def test_bytesmode_search_requires_bytes(self):
        l = self._get_bytes_ldapobject()
        base = self.server.get_dn_suffix()

        with self.assertRaises(TypeError):
            l.search_s(base.encode('utf-8'), ldap.SCOPE_SUBTREE, '(cn=Foo*)', [b'*'])
        with self.assertRaises(TypeError):
            l.search_s(base.encode('utf-8'), ldap.SCOPE_SUBTREE, b'(cn=Foo*)', ['*'])
        with self.assertRaises(TypeError):
            l.search_s(base, ldap.SCOPE_SUBTREE, b'(cn=Foo*)', [b'*'])

    @unittest.skipUnless(PY2, "no bytes_mode under Py3")
    def test_bytesmode_search_results_have_bytes(self):
        l = self._get_bytes_ldapobject()
        base = self.server.get_dn_suffix()
        result = l.search_s(base.encode('utf-8'), ldap.SCOPE_SUBTREE, b'(cn=Foo*)', [b'*'])
        result.sort()
        dn, fields = result[0]
        self.assertEqual(dn, b'cn=Foo1,%s' % base)
        self.assertEqual(type(dn), bytes)
        for key, values in fields.items():
            self.assertEqual(type(key), bytes)
            for value in values:
                self.assertEqual(type(value), bytes)

    @unittest.skipUnless(PY2, "no bytes_mode under Py3")
    def test_unset_bytesmode_search_warns_bytes(self):
        l = self._get_bytes_ldapobject(explicit=False)
        base = self.server.get_dn_suffix()

        l.search_s(base.encode('utf-8'), ldap.SCOPE_SUBTREE, '(cn=Foo*)', [b'*'])
        l.search_s(base.encode('utf-8'), ldap.SCOPE_SUBTREE, b'(cn=Foo*)', ['*'])
        l.search_s(base, ldap.SCOPE_SUBTREE, b'(cn=Foo*)', [b'*'])

    def test_search_subtree(self):
        base = self.server.get_dn_suffix()
        l = self.ldap

        result = l.search_s(base, ldap.SCOPE_SUBTREE, '(cn=Foo*)', ['*'])
        result.sort()
        self.assertEqual(result,
            [('cn=Foo1,'+base,
               {'cn': [b'Foo1'], 'objectClass': [b'organizationalRole']}),
             ('cn=Foo2,'+base,
               {'cn': [b'Foo2'], 'objectClass': [b'organizationalRole']}),
             ('cn=Foo3,'+base,
               {'cn': [b'Foo3'], 'objectClass': [b'organizationalRole']}),
             ('cn=Foo4,ou=Container,'+base,
               {'cn': [b'Foo4'], 'objectClass': [b'organizationalRole']}),
            ]
        )

    def test_search_onelevel(self):
        base = self.server.get_dn_suffix()
        l = self.ldap

        result = l.search_s(base, ldap.SCOPE_ONELEVEL, '(cn=Foo*)', ['*'])
        result.sort()
        self.assertEqual(result,
            [('cn=Foo1,'+base,
               {'cn': [b'Foo1'], 'objectClass': [b'organizationalRole']}),
             ('cn=Foo2,'+base,
               {'cn': [b'Foo2'], 'objectClass': [b'organizationalRole']}),
             ('cn=Foo3,'+base,
               {'cn': [b'Foo3'], 'objectClass': [b'organizationalRole']}),
            ]
        )

    def test_search_oneattr(self):
        base = self.server.get_dn_suffix()
        l = self.ldap

        result = l.search_s(base, ldap.SCOPE_SUBTREE, '(cn=Foo4)', ['cn'])
        result.sort()
        self.assertEqual(result,
            [('cn=Foo4,ou=Container,'+base, {'cn': [b'Foo4']})]
        )


if __name__ == '__main__':
    unittest.main()
