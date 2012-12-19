from setuptools import setup, find_packages

setup(
    name="collective.roster",
    version="0.8.0",
    description="Extendable Personnel Roster",
    long_description=open("README.txt").read() + "\n" +
                open("CHANGES.txt").read(),
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
    ],
    keywords="",
    author="Asko Soukka",
    author_email="asko.soukka@iki.fi",
    url="",
    license="GPL",
    packages=find_packages("src", exclude=["ez_setup"]),
    package_dir={"": "src"},
    namespace_packages=["collective"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "five.grok",
        "zope.schema",
#        "zope.i18n",  # fails on Plone with <includeDependencies />
        "zope.i18nmessageid",
        "plone.indexer",
        "plone.directives.form",
        "plone.app.dexterity",
        "plone.formwidget.contenttree",
        "plone.app.referenceablebehavior",
        "plone.app.viewletmanager",
        "plone.z3ctable",
    ],
    extras_require={"test": [
        "Pillow",
        "robotframework-selenium2library",
        "selenium",  # Python 2.6
        "decorator",  # Python 2.6
        "plone.act",
        "robotsuite",
        "corejet.pivotal",
        "corejet.robot",
    ]},
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
     """
)
