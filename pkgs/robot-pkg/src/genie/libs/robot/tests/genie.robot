*** Settings ***
Library     pyats.robot.pyATSRobot
Library     genie.libs.robot.GenieRobot
Library     genie.libs.robot.GenieRobotApis
Suite setup  Setup

*** Test Cases ***
Test genie parser
    parse "show version" on device "R1"

Test genie API
    get_platform_type    device=R1

*** Keywords ***
Setup
    use testbed "testbed.yaml"
    connect to device "R1"
