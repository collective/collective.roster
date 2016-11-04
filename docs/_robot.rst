..  code:: robotframework

    *** Settings ***

    Resource  plone/app/robotframework/server.robot
    Resource  plone/app/robotframework/keywords.robot
    Resource  Selenium2Screenshots/keywords.robot

    Resource  ${RESOURCE_DIR}/_selectors.robot

    Library  OperatingSystem
    Library  String

    Suite Setup  Run keywords  Suite Setup  Test Setup
    Suite Teardown  Run keywords  Test teardown  Suite Teardown

    *** Variables ***

    ${FIXTURE}  collective.roster.testing.ROSTER_ACCEPTANCE_TESTING
    @{DIMENSIONS}  1200  900
    ${RESOURCE_DIR}  ${CURDIR}

    *** Keywords ***

    Suite Setup
        Run keyword if  not sys.argv[0].startswith('bin/robot-sphinx')
        ...             Setup Plone site  ${FIXTURE}
        Run keyword if  sys.argv[0].startswith('bin/robot-sphinx')
        ...             Open test browser
        Run keyword if  '${CMFPLONE_VERSION}'.startswith('5.')
        ...             Import resource  ${RESOURCE_DIR}/_selectors-5.x.robot
        Run keyword and ignore error  Set window size  @{DIMENSIONS}

    Test Setup
        Import library  Remote  ${PLONE_URL}/RobotRemote

        Run keyword if  sys.argv[0].startswith('bin/robot-sphinx')
        ...             Remote ZODB SetUp  ${FIXTURE}

        ${language} =  Get environment variable  LANGUAGE  'en'
        Set default language  ${language}

        Enable autologin as  Manager
        ${user_id} =  Translate  user_id
        ...  default=jane-doe
        ${user_fullname} =  Translate  user_fullname
        ...  default=Jane Doe
        Create user  ${user_id}  Member  Editor  fullname=${user_fullname}
        Set autologin username  ${user_id}

    Test Teardown
        Run keyword if  sys.argv[0].startswith('bin/robot-sphinx')
        ...             Remote ZODB TearDown  ${FIXTURE}

    Suite Teardown
        Run keyword if  not sys.argv[0].startswith('bin/robot-sphinx')
        ...             Teardown Plone Site
        Run keyword if  sys.argv[0].startswith('bin/robot-sphinx')
        ...             Close all browsers

    *** Test Cases ***
