*** Settings ***

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

Background
    Given the personnel roster product is activated
      And I'm logged in as a site manager

The personnel roster is created
    When I add a new roster
     And I fill the necessary information for roster
     And I click 'Save'
    Then new roster is created

The personnel roster product is activated
    Product is activated  collective.roster

I add a new roster
    Go to  ${PLONE_URL}
    Wait until element is visible  ${SELECTOR_ADD_NEW_MENU}
    Click link  ${SELECTOR_ADD_NEW_MENU}
    Wait until element is visible  id=collective-roster-roster
    Click link  collective-roster-roster
    Wait until page contains  Add Roster

I fill the necessary information for roster
    Input text  form.widgets.IBasic.title  Roster
    Input text  form.widgets.IBasic.description  Personnel roster
    Input text  form.widgets.IGroupsProvider.groups  Members
    select from list  form.widgets.columns_display.from
    ...               collective.roster.personnellisting.name
    select from list  form.widgets.columns_display.from
    ...               collective.roster.personnellisting.email
    select from list  form.widgets.columns_display.from
    ...               collective.roster.personnellisting.phone_number
    Click button  from2toButton

I click 'save'
    Click button  Save


#### PERSON ####

I create person
    Go to  ${PLONE_URL}/roster
    Wait until element is visible  ${SELECTOR_ADD_NEW_MENU}
    Click link  ${SELECTOR_ADD_NEW_MENU}
    Wait until element is visible  id=collective-roster-person
    Click link  collective-roster-person
    Wait until page contains  Add Person

I fill the necessary information for person
    Input text  form.widgets.first_name  Foo
    Input text  form.widgets.last_name  Bar
    Input text  form.widgets.position  Foobar

#    Select frame  text_ifr
#    Input text  content  ${TEXT}
#    Unselect Frame
#    Input text  xpath=//textarea[@id="text"]  ${TEXT}

New person is created
    Page should contain  Item created

New roster is created
    Page should contain  Item created

I'm logged in as a site manager
    Enable autologin as  Site Administrator

I'm logged out
    Disable autologin
