import unittest
import logging

from unittest.mock import Mock, MagicMock, call, ANY
from collections import OrderedDict

from genie.libs.clean.stages.iosxe.stages import ConfigureReplace
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed, Passx
from pyats.aetest.signals import TerminateStepSignal

logger = logging.getLogger(__name__)

class TestConfigureReplace(unittest.TestCase):

    def setUp(self):

        self.cls = ConfigureReplace()
        self.device = create_test_device('PE1', os='iosxe')

        self.data = {
            'configure replace bootflash:test.cfg force': '''
                % Topology global::IPv4 Unicast::base is currently being deconfigured.
% BGP context not been initialized properly.
% Topology global::IPv4 Unicast::base is currently being deconfigured.
% BGP context not been initialized properly.
% Topology global::IPv4 Unicast::base is currently being deconfigured.
% Topology global::IPv4 Unicast::base is currently being deconfigured.
% Topology global::IPv4 Unicast::base is currently being deconfigured.
% Topology global::IPv4 Unicast::base is currently being deconfigured.
% Topology global::IPv4 Unicast::base is currently being deconfigured.
% Topology global::IPv4 Unicast::base is currently being deconfigured.Global Ethernet MTU is set to 1500 bytes.
Note: this is the Ethernet payload size, not the total
Ethernet frame size, which includes the Ethernet
header/trailer and possibly other tags, such as ISL or
802.1q tags.

% ipv6 addresses from all interfaces in VRF vrf-lite have been removed
% ipv4 addresses from all interfaces in VRF vrf-lite have been removed
% ipv6 addresses from all interfaces in VRF vpnv4 have been removed
% ipv4 addresses from all interfaces in VRF vpnv4 have been removed
% ipv6 addresses from all interfaces in VRF global_evpn have been removed
% ipv4 addresses from all interfaces in VRF global_evpn have been removed
VTP version is already in V1.
VTP version is already in V1.
VTP version is already in V1.
VTP version is already in V1.
VTP version is already in V1.
The rollback configlet from the last pass is listed below:
********
!List of Rollback Commands:
vtp version 1
end
********


Rollback aborted after 5 passes''',
        }

    def test_configure_replace_failed_known_arguments(self):
        steps = Steps()

        self.device.execute = Mock(side_effect=lambda x, **y: self.data[x])

        with self.assertRaises(TerminateStepSignal):
            self.cls.configure_replace(steps=steps, device=self.device,
                                       path='bootflash:', file='test.cfg',
                                       config_replace_options='force', known_warnings=['vtp version 2'],
                                       timeout=60)

        self.assertEqual(Failed, steps.details[0].result)

    def test_configure_replace_failed(self):

        steps = Steps()

        self.device.execute = Mock(side_effect=lambda x, **y: self.data[x])

        with self.assertRaises(TerminateStepSignal):
            self.cls.configure_replace(steps=steps, device=self.device,
                                       path='bootflash:', file='test.cfg',
                                       config_replace_options='force', timeout=60)

        self.assertEqual(Failed, steps.details[0].result)

    def test_configure_replace_pass_known_arguments(self):
        steps = Steps()

        self.device.execute = Mock(side_effect=lambda x, **y: self.data[x])

        self.cls.configure_replace(steps=steps, device=self.device,
                                    path='bootflash:', file='test.cfg',
                                    config_replace_options='force', known_warnings = ['vtp version 1'],
                                    timeout=60)

        self.assertEqual(Passx, steps.details[0].result)

    def test_configure_replace_exception(self):
        steps = Steps()

        self.device.execute = Mock(side_effect=Exception)

        with self.assertRaises(TerminateStepSignal):
            self.cls(steps=steps, device=self.device, path='bootflash:', file='base.cfg')

        self.assertEqual(Failed, steps.details[0].result)

    def test_configure_replace_pass_rollback_complete(self):
        data = {'configure replace bootflash:base.cfg force':'''Total number of passes: 1
Rollback Done'''}
        steps = Steps()

        self.device.execute = Mock(side_effect=lambda x, **y: data[x])

        self.cls.configure_replace(steps=steps, device=self.device,
                                    path='bootflash:', file='base.cfg',
                                    config_replace_options='force', known_warnings = ['vtp version 1'],
                                    timeout=60)

        self.assertEqual(Passed, steps.details[0].result)
