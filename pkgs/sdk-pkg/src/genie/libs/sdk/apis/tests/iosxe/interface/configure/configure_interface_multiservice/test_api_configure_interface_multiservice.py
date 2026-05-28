import unittest
from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_interface_multiservice,
    unconfigure_interface_multiservice,
)


class TestConfigureInterfaceMultiservice(TestCase):

    def test_configure_interface_multiservice_full(self):
        device = Mock()
        result = configure_interface_multiservice(
            device,
            101,
            vrf='vrf1',
            ip_address='10.1.1.1',
            mask='255.255.255.0',
            keepalive=False,
            shutdown=False,
        )
        self.assertIsNone(result)
        device.configure.assert_called_once_with([
            'interface multiservice 101',
            'vrf forwarding vrf1',
            'ip address 10.1.1.1 255.255.255.0',
            'no keepalive',
            'no shutdown',
        ])

    def test_configure_interface_multiservice_minimal(self):
        device = Mock()
        result = configure_interface_multiservice(device, 102)
        self.assertIsNone(result)
        device.configure.assert_called_once_with([
            'interface multiservice 102',
            'no shutdown',
        ])

    def test_configure_interface_multiservice_shutdown(self):
        device = Mock()
        configure_interface_multiservice(device, 103, shutdown=True)
        device.configure.assert_called_once_with([
            'interface multiservice 103',
            'shutdown',
        ])

    def test_configure_interface_multiservice_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_interface_multiservice(device, 101)


class TestUnconfigureInterfaceMultiservice(TestCase):

    def test_unconfigure_interface_multiservice(self):
        device = Mock()
        result = unconfigure_interface_multiservice(device, 101)
        self.assertIsNone(result)
        device.configure.assert_called_once_with('no interface multiservice 101')

    def test_unconfigure_interface_multiservice_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_interface_multiservice(device, 101)


if __name__ == '__main__':
    unittest.main()
