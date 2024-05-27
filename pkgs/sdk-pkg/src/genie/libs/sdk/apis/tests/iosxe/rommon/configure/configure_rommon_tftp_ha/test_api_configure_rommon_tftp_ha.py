import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.rommon.configure import configure_rommon_tftp_ha


class TestConfigureRommonTftpHA_1(unittest.TestCase):
    """
    Test to configure rommon variables, if both rps are in rommon
    """
    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          ott-c9400-05:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state rommon
                protocol: unknown
              b:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state rommon
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: cat9k
            management:
              address:
                ipv4: 4.4.4.4/16
              gateway:
                ipv4: 3.3.3.3
              interface: GigabitEthernet0/0
            rommon:
              rp0:
                address:
                  ipv4: 5.5.5.5/16
                gateway:
                  ipv4: 1.1.1.1
              rp1:
                address:
                  ipv4: 6.6.6.6/16
                gateway:
                  ipv4: 2.2.2.2
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
        self.device = self.testbed.devices['ott-c9400-05']
        # To test the TFTP_FILE rommon variable
        self.device.clean.images = ["flash:/test.bin"]
        self.device.connect(
            mit=True
        )

    def test_configure_rommon_tftp(self):
        result = configure_rommon_tftp_ha(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)


class TestConfigureRommonTftpHA_2(unittest.TestCase):
    """
    Test to configure rommon variables, if both one rp in enable and another in rommon
    """

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          ott-c9400-05:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state enable
                protocol: unknown
              b:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state rommon
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: cat9k
            management:
              address:
                ipv4: 4.4.4.4/16
              gateway:
                ipv4: 3.3.3.3
              interface: GigabitEthernet0/0
            rommon:
              rp0:
                address:
                  ipv4: 5.5.5.5/16
                gateway:
                  ipv4: 1.1.1.1
              rp1:
                address:
                  ipv4: 6.6.6.6/16
                gateway:
                  ipv4: 2.2.2.2
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
        self.device = self.testbed.devices['ott-c9400-05']
        # To test the TFTP_FILE rommon variable
        self.device.clean.images = ["flash:/test.bin"]
        self.device.connect(
            mit=True
        )

    def test_configure_rommon_tftp(self):
        result = configure_rommon_tftp_ha(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)



class TestConfigureRommonTftpHA_3(unittest.TestCase):
    """
    Test to configure rommon variables, if both one rp in disable and another in rommon
    """

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          ott-c9400-05:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state disable
                protocol: unknown
              b:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state rommon
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: cat9k
            management:
              address:
                ipv4: 4.4.4.4/16
              gateway:
                ipv4: 3.3.3.3
              interface: GigabitEthernet0/0
            rommon:
              rp0:
                address:
                  ipv4: 5.5.5.5/16
                gateway:
                  ipv4: 1.1.1.1
              rp1:
                address:
                  ipv4: 6.6.6.6/16
                gateway:
                  ipv4: 2.2.2.2
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
        self.device = self.testbed.devices['ott-c9400-05']
        # To test the TFTP_FILE rommon variable
        self.device.clean.images = ["flash:/test.bin"]
        self.device.connect(
            mit=True
        )

    def test_configure_rommon_tftp(self):
        result = configure_rommon_tftp_ha(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
