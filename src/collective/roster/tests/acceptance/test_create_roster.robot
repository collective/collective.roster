*** Settings ***

Meta: Id  38652139
Meta: Title  As a ME, I Want to create personnel roster

Resource  common.robot

Suite Setup  Background

*** Test Cases ***

Create Personnel
    Given the personnel roster is created

    When I create person
     And I fill the necessary information for person
     And I click 'Save'
    Then new person is created


*** Keywords ***

#### ROSTER ####

The personnel roster is created
    When I add a new roster
     And I fill the necessary information for roster
     And I click 'Save'
    Then new roster is created

Background
    Given the personnel roster product is activated
      And I'm logged in as a site manager

The personnel roster product is activated
    Product is activated  collective.roster

I add a new roster
    Go to  ${PLONE_URL}
    Open menu  plone-contentmenu-factories
    Click link  collective-roster-roster

I fill the necessary information for roster
    Input text  form.widgets.IBasic.title  Roster
    Input text  form.widgets.IBasic.description  Personnel roster
    Input text  form.widgets.groups  Members
    select from list  form.widgets.columns_hidden.from
    ...               collective.roster.personnellisting.title
    select from list  form.widgets.columns_hidden.from
    ...               collective.roster.personnellisting.email
    select from list  form.widgets.columns_hidden.from
    ...               collective.roster.personnellisting.phone_number
    Click button  from2toButton

I click 'save'
    Click button  Save


#### PERSON ####

I create person
    Go to  ${PLONE_URL}/roster
    Open menu  plone-contentmenu-factories
    Click link  collective-roster-person

I fill the necessary information for person
    Input text  form.widgets.first_name  Foo
    Input text  form.widgets.last_name  Bar
    Input text  form.widgets.salutation  Foobar

#    Select frame  text_ifr
#    Input text  content  ${TEXT}
#    Unselect Frame
#    Input text  xpath=//textarea[@id="text"]  ${TEXT}

New person is created
    Page should contain  Item created


New roster is created
    Page should contain  Item created

Open Menu
    [Arguments]  ${elementId}
    Element Should Be Visible  css=dl#${elementId} span
    Element Should Not Be Visible  css=dl#${elementId} dd.actionMenuContent
    Click link  css=dl#${elementId} dt.actionMenuHeader a
    Wait until keyword succeeds  1  5  Element Should Be Visible  css=dl#${elementId} dd.actionMenuContent

I'm logged in as a site manager
    Enable autologin as  Site Administrator

Log out
    Disable autologin
