import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import config_ip_on_interface


class TestConfigIpOnInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Galaga-4:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Galaga-4']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_config_ip_on_interface(self):
        result = config_ip_on_interface(self.device, 'Fi1/0/5', '14.1.1.2', '255.255.255.0', None, None, None, None, False, False, '', 'WAN-VRFv4')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_config_duplicate_ip_on_interface(self):
        result = config_ip_on_interface(self.device, 'Fi1/0/5', '14.1.1.4', '255.255.255.0', None, None, None, None, False, False, '', 'WAN-VRFv4')
        expected_output = ['% 14.1.1.0 overlaps with Fi1/0/6', '% 14.1.1.0 overlaps with Fi1/0/6']
        self.assertEqual(result, expected_output)
