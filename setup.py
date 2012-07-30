from setuptools import setup, find_packages

version = "1.0.0"

setup(name="jyu.roster",
      version=version,
      description="Generic Personnel Roster",
      long_description=open("README.txt").read() + "\n" +
                       open("HISTORY.txt").read(),
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
      namespace_packages=["jyu"],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "setuptools",
          "plone.app.dexterity",
          "plone.app.referenceablebehavior",
          "five.grok",
     
      ],
      extras_require={
          "test": ["plone.app.testing", "corejet.pivotal"],
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """
      )
