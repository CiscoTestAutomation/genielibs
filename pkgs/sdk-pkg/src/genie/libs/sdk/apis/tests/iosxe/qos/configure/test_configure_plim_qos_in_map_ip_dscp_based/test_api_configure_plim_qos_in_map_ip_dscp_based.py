from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.qos.configure import configure_plim_qos_in_map_ip_dscp_based


class TestConfigurePlimQosInMapIpDscpBased(TestCase):

    def test_configure_plim_qos_in_map_ip_dscp_based(self):
        self.device = Mock()
        self.device.name = "DeviceA"
        configure_plim_qos_in_map_ip_dscp_based(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['plim qos in map ip dscp-based'],)
        )

    def test_configure_plim_qos_in_map_ip_dscp_based_failure(self):
        self.device = Mock()
        self.device.name = "DeviceA"
        self.device.configure.side_effect = SubCommandFailure("configure error")
        with self.assertRaises(SubCommandFailure):
            configure_plim_qos_in_map_ip_dscp_based(self.device)
