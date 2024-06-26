import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.rommon.configure import configure_rommon_tftp


class TestConfigureRommonTftp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          ott-c9300-63:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: cat9k
            management:
              address:
                ipv4: 5.5.5.5/16
              gateway:
                ipv4: 1.1.1.1
              interface: GigabitEthernet0/0
        testbed:
          servers:
            tftp:
              address: 2.2.2.2
              credentials:
                default:
                  password: ''
                  username: ''
                enable:
                  password: ''
              protocol: tftp
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['ott-c9300-63']
        self.device.connect(
            mit=True
        )

    def tearDown(self):
        self.device.disconnect()

    def test_configure_rommon_tftp_1(self):
        # To test the TFTP_FILE rommon variable
        self.device.clean.images = ['flash:/test.bin']
        result = configure_rommon_tftp(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_rommon_tftp_2(self):
        # To test the TFTP_FILE rommon variable
        self.device.clean.images = {'image': ['flash:/test.bin']}
        result = configure_rommon_tftp(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_rommon_tftp_3(self):
        # To test the TFTP_FILE rommon variable
        self.device.clean.images = {'image': {'file': ['flash:/test.bin']}}
        result = configure_rommon_tftp(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
