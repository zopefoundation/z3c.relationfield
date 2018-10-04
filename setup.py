from setuptools import setup, find_packages
import os


def read(*rnames):
    return open(os.path.join(*rnames)).read()

long_description = (
    read('src', 'z3c', 'relationfield', 'README.rst')
    + '\n' +
    read('CHANGES.rst')
    + '\n' +
    'Download\n'
    '********\n'
)

setup(
    name='z3c.relationfield',
    version='0.7.1.dev0',
    description="A relation field framework for Zope 3.",
    long_description=long_description,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='',
    author='Martijn Faassen',
    author_email='faassen@startifact.com',
    license='ZPL 2.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['z3c'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'z3c.objpath',
        'zc.relation >= 1.0',
        'zope.intid',
    ],
    extras_require={
        'test': [
            'zope.container',
            'zope.copypastemove',
            'zope.site',
        ],
        'xml': ['z3c.schema2xml >= 1.0',
                'lxml'],
    },
    entry_points={},
)
