*** Settings ***
Library     pyats.robot.pyATSRobot
Library     genie.libs.robot.GenieRobot
Library     genie.libs.robot.GenieRobotApis
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

