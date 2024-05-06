import logging
import unittest

from unittest.mock import Mock, call

from genie.libs.clean.stages.iosxe.stages import ResetConfiguration
from pyats.topology import loader
from pyats.aetest.steps import Steps
from pyats.results import Passed, Passx, Errored
from pyats.aetest.signals import TerminateStepSignal

class TestIosXEConnect(unittest.TestCase):
    """ Run unit testing on a mocked IOSXE cat9k device """

    @classmethod
    def setUpClass(self):
        testbed = """
       devices:
        FW-9300-7:
            connections:
                defaults:
                    class: unicon.Unicon
                a:
                    command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                    protocol: unknown
            os: iosxe
            platform: c9300
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['FW-9300-7']
        self.data = """
        Building configuration...

Current configuration : 9162 bytes
!
! Last configuration change at 22:06:12 UTC Tue Mar 19 2024
!
version 17.15
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname FW-9300-7
!
!
vrf definition Mgmt-vrf
 !
 address-family ipv4
 exit-address-family
 !
 address-family ipv6
 exit-address-family
!
no logging console
aaa new-model
!
!
!
!
aaa session-id common
switch 1 provision c9300-24u
!
!
!
!
!
!
!
!
!
!
!
!
login on-success log
!
!
!
!
!
!
!
!
crypto pki trustpoint TP-self-signed-4016338086
 enrollment selfsigned
 subject-name cn=IOS-Self-Signed-Certificate-4016338086
 revocation-check none
 rsakeypair TP-self-signed-4016338086
 hash sha256
!
crypto pki trustpoint SLA-TrustPoint
 enrollment pkcs12
 revocation-check crl
 hash sha256
!
license boot level network-advantage addon dna-advantage
memory free low-watermark processor 105485
!
diagnostic bootup level minimal
!
spanning-tree mode rapid-pvst
spanning-tree extend system-id
!
!
!
!
username admin privilege 15 password 0 Secret12345
!
redundancy
 mode sso
!
!
!
!
!
transceiver type all
 monitoring
!
interface GigabitEthernet0/0
 vrf forwarding Mgmt-vrf
 ip address 10.1.1.1 255.255.0.0
 negotiation auto
!
interface GigabitEthernet1/0/1
!
interface GigabitEthernet1/0/2
!
interface GigabitEthernet1/0/3
!
interface GigabitEthernet1/0/4
!
interface GigabitEthernet1/0/5
!
interface GigabitEthernet1/0/6
!
interface GigabitEthernet1/0/7
!
interface GigabitEthernet1/0/8
!
interface GigabitEthernet1/0/9
!
interface GigabitEthernet1/0/10
!
interface GigabitEthernet1/0/11
!
interface GigabitEthernet1/0/12
!
interface GigabitEthernet1/0/13
!
interface GigabitEthernet1/0/14
!
interface GigabitEthernet1/0/15
!
interface GigabitEthernet1/0/16
!
interface GigabitEthernet1/0/17
!
interface GigabitEthernet1/0/18
!
interface GigabitEthernet1/0/19
!
interface GigabitEthernet1/0/20
!
interface GigabitEthernet1/0/21
!
interface GigabitEthernet1/0/22
!
interface GigabitEthernet1/0/23
!
interface GigabitEthernet1/0/24
!
interface GigabitEthernet1/1/1
!
interface GigabitEthernet1/1/2
!
interface GigabitEthernet1/1/3
!
interface GigabitEthernet1/1/4
!
interface TenGigabitEthernet1/1/1
!
interface TenGigabitEthernet1/1/2
!
interface TenGigabitEthernet1/1/3
!
interface TenGigabitEthernet1/1/4
!
interface TenGigabitEthernet1/1/5
!
interface TenGigabitEthernet1/1/6
!
interface TenGigabitEthernet1/1/7
!
interface TenGigabitEthernet1/1/8
!
interface FortyGigabitEthernet1/1/1
!
interface FortyGigabitEthernet1/1/2
!
interface TwentyFiveGigE1/1/1
!
interface TwentyFiveGigE1/1/2
!
interface AppGigabitEthernet1/0/1
!
interface Vlan1
 no ip address
 shutdown
!
ip forward-protocol nd
ip http server
ip http secure-server
ip ssh bulk-mode 131072
!
!
!
!
!
!
!
!
control-plane
 service-policy input system-cpp-policy
!
!
!
line con 0
 exec-timeout 0 0
line vty 0 4
 exec-timeout 0 0
 transport input all
line vty 5 31
 transport input telnet ssh
!
!
!
!
!
!
!
end
"""
    
    def test_reset_configuration_pass(self):

        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the following methods to be mocked to simulate the stage.
        self.device.execute = Mock(return_value=self.data)
        self.device.tclsh = Mock()
        self.device.sendline = Mock()
        self.device.spawn = Mock()
        self.device.expect = Mock()
        self.device.state_machine = Mock()
        self.device.enable = Mock()
        self.device.configure = Mock()
        self.reset_configuration = ResetConfiguration()
        self.reset_configuration(steps=steps, device=self.device)

        # Check the results is as expected.
        self.assertEqual(Passed, steps.details[0].result)
        self.device.configure.assert_has_calls([call('hostname FW-9300-7')])
        self.device.execute.assert_has_calls([call('show running-config')])
        self.device.sendline.assert_has_calls([call('puts [open "base_config.txt" w+] {')])
        config_text = """
!
! Last configuration change
!
hostname FW-9300-7
no logging console
service timestamps debug datetime msec
service timestamps log datetime msec
vrf definition Mgmt-vrf
 address-family ipv4
 exit-address-family
 address-family ipv6
aaa new-model
aaa session-id common
switch 1 provision c9300-24u
login on-success log
crypto pki trustpoint TP-self-signed-4016338086
 enrollment selfsigned
 subject-name cn=IOS-Self-Signed-Certificate-4016338086
 revocation-check none
 rsakeypair TP-self-signed-4016338086
 hash sha256
crypto pki trustpoint SLA-TrustPoint
 enrollment pkcs12
 revocation-check crl
 hash sha256
license boot level network-advantage addon dna-advantage
memory free low-watermark processor 105485
diagnostic bootup level minimal
spanning-tree mode rapid-pvst
spanning-tree extend system-id
username admin privilege 15 password 0 Secret12345
redundancy
 mode sso
transceiver type all
 monitoring
interface GigabitEthernet0/0
 vrf forwarding Mgmt-vrf
 negotiation auto
interface Vlan1
 no ip address
 shutdown
ip forward-protocol nd
ip http server
ip http secure-server
ip ssh bulk-mode 131072
control-plane
 service-policy input system-cpp-policy
line vty 0 4
 transport input all
line vty 5 31
 transport input telnet ssh
end"""
        config_lines = config_text.splitlines()
        for line in config_lines:
            yield self.device.sendline.assert_has_calls([call(line),])

    def test_reset_configuration_fail__1(self):

        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        data = """
        This will apply all necessary additions and deletions
        to replace the current running configuration with the
        contents of the specified configuration file, which is
        assumed to be a complete configuration, not a partial
        configuration. Enter Y if you are sure you want to proceed. ? [no]: Y

        Total number of passes: 0
        Rollback aborted
        """

        # And we want the execute method to raise an exception when called.
        self.device.execute = Mock(return_value=data)
        self.device.configure = Mock()

        # We expect this step to fail
        self.reset_configuration = ResetConfiguration()
        self.reset_configuration.reset_configuration(
                steps=steps, device=self.device
            )

        # Check the overall result is as expected
        self.assertEqual(Passx, steps.details[0].result)

    def test_reset_configuration_fail__2(self):

        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute method to raise an exception when called.
        self.device.execute = Mock(side_effect=Exception)

        self.reset_configuration = ResetConfiguration()
        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(Exception):
            self.reset_configuration(
                steps=steps, device=self.device
            )

        # Check the overall result is as expected
        self.assertEqual(Errored, steps.details[0].result)
