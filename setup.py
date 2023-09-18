from setuptools import setup, find_packages
import os

version = "2.0.1"

tests_require = [
    "plone.app.testing",
    "plone.app.contenttypes",
    "plone.app.robotframework[debug]",
    "unittest2",
]

setup(
    name="collective.analyticspanel",
    version=version,
    description="Add more control over the inclusion of JavaScript analytics code of your Plone site",
    long_description=open("README.rst").read()
    + "\n"
    + open(os.path.join("docs", "HISTORY.rst")).read(),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="plone analytics plonegov",
    author="RedTurtle Technology",
    author_email="sviluppoplone@redturtle.it",
    url="http://plone.org/products/collective.analyticspanel",
    license="GPL",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["collective"],
    include_package_data=True,
    zip_safe=False,
    tests_require=tests_require,
    extras_require=dict(test=tests_require),
    install_requires=[
        "setuptools",
        "collective.z3cform.datagridfield",
        "plone.app.registry",
        "plone.app.vocabularies",
        "plone.api",
    ],
    entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
