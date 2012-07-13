.. contents:: **Table of contents**

Introduction
============

This product will replace the basic Plone feature for **adding statistical and analytics JavaScript to your site**
with an advanced version that:

* add possibility to add specific JavaScript when the user is **inside error page**
  (useful for special code when on the "*Page not found*")
* add possibility to **customize code for a site area** or a single content
* not display JavaScript code for specific area of the site

How to use it
=============

When installed, the basic Plone feature for handling JavaScript for statistics is hidden from the standard
"*Site settings*" (in facts, it's moved to a new configuration panel called "*Analytics settings*") and
new options are now available.

JavaScript for web statistics support 
-------------------------------------

.. image:: http://keul.it/images/plone/collective.analyticspanel/collective.analyticspanel-0.1.0-01.png
   :alt: Basic feature

Nothing new there: this is simply the basic Plone feature about JavaScript inclusion, just moved in this
separate panel. This is always the default code included when other options don't match.

JavaScript to be included when an error message is get 
------------------------------------------------------

.. image:: http://keul.it/images/plone/collective.analyticspanel/collective.analyticspanel-0.1.0-02.png
   :alt: Code for error page

When this product is installed you can control JavaScript code based on error messages (ignoring the default one).
The main motivation is to use this for the ``NotFound`` (HTTP 404) error.

However this feature is still generic... you could probably use it for other error code (like ``ValueError``)
if this make sense for you!

JavaScript to be included inside specific site's paths 
------------------------------------------------------

.. image:: http://keul.it/images/plone/collective.analyticspanel/collective.analyticspanel-0.2.0-01.png
   :alt: Code for specific site's path

You can use this section for putting a list of absolute site subsection you want to control, adding a specific
JavaScript section and ignoring the default one.

When more than a provided path match the current URL, the most specific ones is used.

You can also uncheck the availability of the rule in the whole site subtree.

Hiding
------

You can also use this product for hiding analytics code from specific site areas or error pages, leaving a default
one for the rest of the site.

Just configure options with empty code!

Dependencies
============

This product has been tested on:

* Plone 3.3 (read below)
* Plone 4.2

It's based on `plone.app.registry`__ that it not part of Plone on 3.3 version. You need to be sure that a compatible
version is used (in my experience: use `version 1.0b1`__)

__ http://pypi.python.org/pypi/plone.app.registry
__ http://pypi.python.org/pypi/plone.app.registry/1.0b1

Credits
=======
  
Developed with the support of:

* `Regione Emilia Romagna`__

* `Provincia di Ferrara`__

  .. image:: http://www.provincia.fe.it/Distribuzione/logo_provincia.png
     :alt: Provincia di Ferrara - logo

All of them supports the `PloneGov initiative`__.

__ http://www.regione.emilia-romagna.it/
__ http://www.provincia.fe.it/
__ http://www.plonegov.it/

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
