from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.mac.configure import (
    configure_interface_mka_pre_share_key,
    unconfigure_interface_mka_pre_share_key,
)


class TestConfigureInterfaceMkaPreShareKey(TestCase):

    def test_configure_interface_mka_pre_share_key(self):
        self.device = Mock()
        interface = "GigabitEthernet1/0/1"
        key_name = "MY_KEY"
        configure_interface_mka_pre_share_key(self.device, interface=interface, key_name=key_name)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ([
                f"interface {interface}",
                f"mka pre-share key {key_name}",
            ],)
        )

    def test_unconfigure_interface_mka_pre_share_key(self):
        self.device = Mock()
        interface = "GigabitEthernet1/0/2"
        key_name = "TEST_KEY"
        unconfigure_interface_mka_pre_share_key(self.device, interface=interface, key_name=key_name)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ([
                f"interface {interface}",
                f"no mka pre-share key {key_name}",
            ],)
        )
