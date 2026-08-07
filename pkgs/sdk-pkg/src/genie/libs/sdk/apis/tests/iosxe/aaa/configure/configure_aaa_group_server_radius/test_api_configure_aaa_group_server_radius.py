import unittest
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.aaa.configure import \
    configure_aaa_group_server_radius


class TestConfigureAaaGroupServerRadius(unittest.TestCase):

    def test_configure_aaa_group_server_radius(self):
        device = Mock()
        configure_aaa_group_server_radius(
            device, 'ISG', server_name='host',
            source_interface='GigabitEthernet0/3/7.10',
            vrf='Mgmt-intf', unconfigure_vrf=True)
        device.configure.assert_called_once_with(
            [
                "aaa group server radius ISG",
                "server name host",
                "ip radius source-interface GigabitEthernet0/3/7.10",
                "no ip vrf forwarding Mgmt-intf",
            ]
        )

    def test_configure_aaa_group_server_radius_with_vrf(self):
        device = Mock()
        configure_aaa_group_server_radius(
            device, 'ISG', server_name='host', vrf='Mgmt-intf')
        device.configure.assert_called_once_with(
            [
                "aaa group server radius ISG",
                "server name host",
                "ip vrf forwarding Mgmt-intf",
            ]
        )

    def test_configure_aaa_group_server_radius_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_aaa_group_server_radius(device, 'ISG')
