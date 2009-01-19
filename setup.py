from setuptools import setup, find_packages
import sys, os

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('src', 'z3c', 'relationfield', 'README.txt')
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Download\n'
    '********\n'
    )

setup(
    name='z3c.relationfield',
    version='0.4dev',
    description="A relation field framework for Zope 3.",
    long_description=long_description,
    classifiers=[],
    keywords='',
    author='Martijn Faassen',
    author_email='faassen@startifact.com',
    license='',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['z3c'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'ZODB3',
        'grokcore.component',
        'zope.app.intid',
        'zope.app.container',
        'z3c.schema2xml >= 1.0',
        'z3c.objpath',
        'zc.relation >= 1.0',
        # for tests
        'zope.app.zcmlfiles',
        'zope.securitypolicy',
        ],
    entry_points={},
    )
