import os
from pyats.topology import loader
from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.verify import verify_ip_address_on_interface


class TestVerifyIpAddressOnInterface(TestCase):
    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          S21-9300:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: cat9k
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['S21-9300']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_ip_address_on_interface(self):
        result = verify_ip_address_on_interface(self.device, 'GigabitEthernet0/0', '10.76.119.164', 20, 5)
        expected_output = True
        self.assertEqual(result, expected_output)
