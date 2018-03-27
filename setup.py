from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name = 'pyldap',
    license = 'Python style',
    version = '3.0.0.post1',
    description = 'DEPRECATED; use python-ldap instead',
    long_description = long_description,
    author = 'pyldap project',
    author_email = 'python-ldap@python.org',
    url = 'https://github.com/pyldap/pyldap/',
    download_url = 'https://pypi.python.org/pypi/pyldap/',
    install_requires = ['python-ldap>=3.0.0b1'],
)
