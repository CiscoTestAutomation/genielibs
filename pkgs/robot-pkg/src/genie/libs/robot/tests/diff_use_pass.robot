*** Settings ***
Library     pyats.robot.pyATSRobot
Library     genie.libs.robot.GenieRobot    use_pass_fail=${TRUE}
Suite setup  Setup

*** Keywords ***
Setup
    use genie testbed "diff_testbed.yaml"
    connect to device "r1"

*** Test Cases ***
Profile config on uut
    Profile the system for "config" on devices "uut" as "snap1"

Profile config on uut, Compare it with previous snapshot
    Profile the system for "config" on devices "uut" as "snap2"
    Compare profile "snap2" with "snap1" on devices "uut"
    # The following statement should not be executed when use_pass_fail=${TRUE}
    Set Global Variable    $CONTINUED    ${TRUE}

Test Did Not Continue
    ${value}=    Get Variable Value    ${CONTINUED}
    Should be True    $value is None    msg=The previous test case did continue
