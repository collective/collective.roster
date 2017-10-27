Changelog
=========

2.3.0 (2017-10-27)
------------------

- Change english translation for subject from studysubject to subject
  [Grrandi]


2.2.1 (2017-10-03)
------------------

- Fixed SimpleTerm creation.
  [iham]


2.2.0 (2017-04-04)
------------------

- Add option for groups behavior to mark person a groups leader and sort
  leaders before others in grouped views
  [datakurre]


2.1.4 (2017-04-04)
------------------

- Fix issue where group links on gallery depended on current URL and might have
  been broken
  [datakurre]


2.1.3 (2017-03-29)
------------------

- Fix to require plone.app.registry>=1.2.5 [fixes #6]
  [datakurre]

2.1.2 (2017-01-12)
------------------

- Fix issue where groups adapter returned None
  [datakurre]

2.1.1 (2017-01-11)
------------------

- Fix biography to be primary field
  [datakurre]

2.1.0 (2016-12-19)
------------------

- Make roster views aware of possibly enabled RichText-behavior
  [datakurre]


2.0.3 (2016-12-16)
------------------

- Fix issue where group anchors on groups_view were broken
  [datakurre]


2.0.2 (2016-12-07)
------------------

- Fix alphabetical listing to sort using locale aware sortable title
  [datakurre]


2.0.1 (2016-11-08)
------------------

- Fix issue where empty value for JS bundle broke Plone bundle merge
  on a new site
  [datakurre]


2.0.0 (2016-11-04)
------------------

- Allow short number to be anything between 100 and 9999
  [datakurre]

- Plone 5 compatibility: Optionally import ``checkEmailAddress`` and
  ``EmailAddressInvalid`` from CMFPlone respectively CMFDefault.
  [thet]

- Add file type checking for person portrait image
  [Grrandi, datakurre]

- Change studysubject behavior label from 'Studysubject' to 'Subject'
  [Grrandi, datakurre]

- Refactored grokless public release.
  [datakurre]
