from setuptools import setup, find_packages
import sys, os

setup(
    name='z3c.objpath',
    version='0.1dev',
    description="Paths to to objects.",
    long_description="""""",
    classifiers=[],
    keywords='',
    author='Martijn Faassen',
    author_email='faassen@startifact.com',
    url='http://dev.inghist.nl/eggs/',
    license='',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zope.interface',
        ],
    entry_points={},
    )
