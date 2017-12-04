from setuptools import setup

setup(
    name = 'pyldap',
    license = 'Python style',
    version = '3.0.0',
    description = 'DEPRECATED; use python-ldap instead',
    long_description = """
        The pyldap fork was merged back into python-ldap,
        and will be released as python-ldap 3.0.0.
    """,
    author = 'pyldap project',
    author_email = 'python-ldap@python.org',
    url = 'https://github.com/pyldap/pyldap/',
    download_url = 'https://pypi.python.org/pypi/pyldap/',
    install_requires = ['python-ldap>=3.0.0b1'],
)
