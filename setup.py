import os

from setuptools import setup


def read(*rnames):
    return open(os.path.join(*rnames)).read()


long_description = (
    read("src", "z3c", "relationfield", "README.rst")
    + "\n"
    + read("CHANGES.rst")
    + "\n"
    + "Download\n"
    "********\n"
)

setup(
    name="z3c.relationfield",
    version="3.1.dev0",
    description="A relation field framework for Zope 3.",
    long_description=long_description,
    classifiers=[
        "Development Status :: 6 - Mature",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    keywords="relation field",
    author="Martijn Faassen",
    author_email="zope-dev@zope.dev",
    url="https://github.com/zopefoundation/z3c.relationfield",
    license="ZPL-2.1",
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        "setuptools",
        "z3c.objpath >= 3",
        "zc.relation >= 1.0",
        "zope.intid",
    ],
    extras_require={
        "test": [
            "zope.container",
            "zope.copypastemove",
            "zope.site",
        ],
    },
    entry_points={},
)
