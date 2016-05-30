# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='collective.roster',
    version='2.0.0a1',
    description='Personnel Roster',
    long_description=(open('README.rst').read() + '\n' +
                      open('CHANGES.rst').read()),
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Programming Language :: Python',
    ],
    keywords='',
    author='Asko Soukka',
    author_email='asko.soukka@iki.fi',
    url='',
    license='EUPL',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'Products.CMFCore',
        'Products.CMFPlone',
        'Zope2',
        'borg.localrole',
        'plone.api',
        'plone.app.dexterity',
        'plone.app.textfield',
        'plone.app.viewletmanager',
        'plone.autoform',
        'plone.formwidget.contenttree',
        'plone.formwidget.namedfile',
        'plone.indexer',
        'plone.memoize',
        'plone.namedfile [blobs]',
        'plone.supermodel',
        'plone.z3ctable',
        'python-magic',
        'zope.component',
        'zope.i18n',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.publisher',
        'zope.schema',
    ],
    extras_require={'test': [
        'Pillow',
        'corejet.core',
        'plone.app.testing',
        'plone.app.robotframework'
    ]},
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """
)
