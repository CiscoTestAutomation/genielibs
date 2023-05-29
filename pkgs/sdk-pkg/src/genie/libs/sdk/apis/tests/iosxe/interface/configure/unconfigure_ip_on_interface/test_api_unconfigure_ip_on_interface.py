import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_ip_on_interface


class TestUnconfigureIpOnInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-nyquist-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-nyquist-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_ip_on_interface(self):
        result = unconfigure_ip_on_interface(self.device, 'Gi1/0/7', '5.5.5.5', '255.255.255.0', None, 'sap', None, None, True, 'test', None, None, False)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_ip_on_interface_1(self):
        result = unconfigure_ip_on_interface(self.device, 'Gi1/0/7', '5.5.5.5', '255.255.255.0', None, None, None, None, True, '', None, None, False)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_ip_on_interface_2(self):
        result = unconfigure_ip_on_interface(self.device, 'Gi1/0/7', '5.5.5.5', '255.255.255.0', None, 'arpa', None, None, False, '', None, None, True)
        expected_output = None
        self.assertEqual(result, expected_output)
