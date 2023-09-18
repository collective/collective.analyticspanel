Changelog
=========

2.0.1 (2023-09-18)
------------------

- Fix logic in controlpanel save method.
  [cekk]


2.0.0 (2022-11-23)
------------------

- Major refactoring for python 3.8 and plone 5.2
  [axaroth]


1.0.0 (2019-01-09)
------------------

- Remove custom persistent field from registry.
  [cekk]


0.6.1 (2017-09-15)
------------------

- Fix pypi classifiers
  [cekk]

0.6.0 (2017-09-15)
------------------

- Plone 5 compatibility.
  [cekk, mamico]
- Drop plone 3 compatibility.
  [cekk]
- Fix tests and add travis config.
  [cekk]

0.5.0 (2017-01-20)
------------------

- Added options to block analytics for user's privacy choices
  [keul]
- Don't show analytics in views used on overlays (so with ajax_load paramiter)
  [cekk]

0.4.0 (2014-06-25)
------------------

- Fix bug that prevented viewlet from being shown on plone sites
  located in subfolders (eg. /project/Plone) which is quite common
  when ZODB mountpoints are used. [fRiSi]
- Fixed a bug that randomly hit the installation (See `#2`__) [keul]
- Fixed translations not shown in vocabulary [keul]
- You can now choose to put analytics before the ``body`` tag or
  near the end of it. This close `#1`__

__ https://github.com/RedTurtle/collective.analyticspanel/issues/2
__ https://github.com/RedTurtle/collective.analyticspanel/issues/1

0.3.0 (2012-08-28)
------------------

- Italian i18n fixes [keul]
- Added a way to set rules for subsections and leaf contents inside
  (subcontents that are not folderish) [keul]

0.2.0 (2012-07-13)
------------------

- Some styles fixes in the management panel [keul]
- Added new option: ``apply_to_subsection``
- Added the "*autoresize*" CSS class for textareas
  (in the case you also use `collective.autoresizetextarea`__)
  [keul]

__ http://pypi.python.org/pypi/collective.autoresizetextarea/

0.1.0 (2012-07-04)
------------------

- Initial release
