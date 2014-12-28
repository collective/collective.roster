.. code:: robotframework

   *** Settings ***

   Resource  plone/app/robotframework/server.robot
   Resource  plone/app/robotframework/keywords.robot
   Resource  Selenium2Screenshots/keywords.robot

   Library  OperatingSystem

   Suite Setup  Run keywords  Suite Setup  Test Setup
   Suite Teardown  Run keywords  Test Teardown  Suite Teardown

   *** Variables ***

   ${FIXTURE}  collective.roster.testing.ROSTER_ROBOT_TESTING
   @{DIMENSIONS}  640  1024

   *** Keywords ***

   Suite Setup
       Run keyword if  'bin/robot' not in sys.argv[0]
       ...             Setup Plone site  ${FIXTURE}
       Run keyword if  'bin/robot' in sys.argv[0]
       ...             Open test browser
       Run keyword and ignore error  Set window size  @{DIMENSIONS}

   Test Setup
       Import library  Remote  ${PLONE_URL}/RobotRemote

       Run keyword if  'bin/robot' in sys.argv[0]
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
       Run keyword if  'bin/robot' in sys.argv[0]
       ...             Remote ZODB TearDown  ${FIXTURE}

   Suite Teardown
       Run keyword if  'bin/robot' not in sys.argv[0]
       ...             Teardown Plone Site
       Run keyword if  'bin/robot' in sys.argv[0]
       ...             Close all browsers

   *** Test Cases ***
