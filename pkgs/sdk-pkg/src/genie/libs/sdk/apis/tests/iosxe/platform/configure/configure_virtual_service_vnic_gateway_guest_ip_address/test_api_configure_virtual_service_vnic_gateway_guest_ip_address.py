import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.configure import configure_virtual_service_vnic_gateway_guest_ip_address


class TestConfigureVirtualServiceVnicGatewayGuestIpAddress(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          n08HA:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9500
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['n08HA']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_virtual_service_vnic_gateway_guest_ip_address(self):
        result = configure_virtual_service_vnic_gateway_guest_ip_address(self.device, 'VirtualPortGroup1', '16.18.27.2', '255.255.255.0', 'enable', '228.10.10.2')
        expected_output = None
        self.assertEqual(result, expected_output)
