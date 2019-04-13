from setuptools import setup, find_packages


setup(
    name='collective.roster',
    version='2.3.2.dev0',
    description='Personnel Roster',
    long_description=(open('README.rst').read() + '\n' +
                      open('CHANGELOG.rst').read()),
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone :: 5.0',
    ],
    keywords='',
    author='Asko Soukka',
    author_email='asko.soukka@iki.fi',
    url='https://github.com/collective/collective.roster',
    license='EUPL',
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=['ez_setup']),
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
        'plone.app.registry>=1.2.5',
        'plone.autoform',
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
        # 'corejet.core',
        'plone.app.testing',
        # 'plone.app.imaging',
        'plone.app.robotframework',
    ]},
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
