collective.roster
=================

.. include:: _robot.rst


Add a new roster
================

.. figure:: roster-add-form.png
.. code:: robotframework

    Creating a roster
        Go to  ${PLONE_URL}/++add++collective.roster.roster

        Input text  form.widgets.IBasic.title  Roster
        Input text  form.widgets.IBasic.description  Personnel roster
        Input text  form.widgets.IGroupsProvider.groups
        ...         directors|Directors\nall|All
        Select from list  form.widgets.columns_display.from
        ...               collective.roster.personnellisting.name
        Click button  from2toButton
        Select from list  form.widgets.columns_display.from
        ...               collective.roster.personnellisting.email
        Click button  from2toButton
        Select from list  form.widgets.columns_display.from
        ...               collective.roster.personnellisting.phone_number
        Click button  from2toButton

        Capture and crop page screenshot  roster-add-form.png  css=#content
