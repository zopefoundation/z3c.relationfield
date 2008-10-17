from setuptools import setup, find_packages
import sys, os

setup(
    name='z3c.relationfield',
    version='0.1dev',
    description="A relation field framework.",
    long_description="""z3c.relationfield defines a Zope 3 schema field to
    manage relations, and a widget to set them. Relations are automatically
    indexed and can be queried, using zc.relation as a base.""",
    classifiers=[],
    keywords='',
    author='Martijn Faassen',
    author_email='faassen@startifact.com',
    license='',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'grok',
        'z3c.schema2xml',
        'z3c.objpath',
        'zc.relation',
        ],
    entry_points={},
    )
