import os
import unittest
from unittest.mock import Mock

from pyats.topology import loader

from genie.libs.sdk.apis.iosxe.rommon.configure import configure_rommon_tftp
from genie.libs.sdk.libs.utils.utils import (
    get_recovery_tftp_server, get_tftp_server_address)


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
        self.device = self.testbed.devices["ott-c9300-63"]
        self.device.connect(mit=True)

    def tearDown(self):
        self.device.disconnect()

    def test_configure_rommon_tftp_1(self):
        # To test the TFTP_FILE rommon variable
        self.device.clean.images = ["flash:/test.bin"]
        result = configure_rommon_tftp(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_rommon_tftp_2(self):
        # To test the TFTP_FILE rommon variable
        self.device.clean.images = {"image": ["flash:/test.bin"]}
        result = configure_rommon_tftp(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_rommon_tftp_3(self):
        # To test the TFTP_FILE rommon variable
        self.device.clean.images = {"image": {"file": ["flash:/test.bin"]}}
        result = configure_rommon_tftp(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_rommon_tftp_4(self):
        self.device.clean.images = ["faulty_image.bin"]
        result = configure_rommon_tftp(self.device, image_path="valid_image.bin")
        expected_output = None
        self.assertEqual(result, expected_output)


class TestTftpServerSelection(unittest.TestCase):

    @staticmethod
    def _device(servers):
        device = Mock()
        device.testbed.servers = servers
        return device

    def test_prefers_lowest_ordered_tftp_service(self):
        device = self._device({
            "tftp": {
                "address": "192.168.1.254",
                "protocol": "tftp",
                "services": {
                    "legacy-tftp": {
                        "order": 20,
                        "protocol": "tftp",
                        "type": "file_transfer",
                    }
                },
            },
            "tftp-morpheus": {
                "address": "10.8.0.16",
                "services": {
                    "morpheus-tftp": {
                        "order": 10,
                        "protocol": "tftp",
                        "type": "file_transfer",
                    }
                },
            },
        })

        self.assertEqual(get_tftp_server_address(device), "10.8.0.16")

    def test_supports_legacy_top_level_protocol(self):
        device = self._device({
            "proxy": {
                "address": "10.0.0.1",
                "protocol": "scp",
            },
            "legacy-server": {
                "address": "192.0.2.10",
                "protocol": "tftp",
            },
        })

        self.assertEqual(get_tftp_server_address(device), "192.0.2.10")

    def test_non_mapping_testbed_servers_returns_empty_address(self):
        device = Mock()

        self.assertEqual(get_tftp_server_address(device), "")

    def test_false_clean_data_falls_back_to_testbed(self):
        device = self._device({
            "tftp-morpheus": {
                "address": "10.8.0.16",
                "services": {
                    "morpheus-tftp": {
                        "order": 10,
                        "protocol": "tftp",
                    }
                },
            },
        })
        device.name = "uut"
        device.clean = False

        self.assertEqual(get_recovery_tftp_server(device), "10.8.0.16")

    def test_clean_recovery_tftp_server_takes_precedence(self):
        device = self._device({
            "tftp-morpheus": {
                "address": "10.8.0.16",
                "protocol": "tftp",
            },
        })
        device.name = "uut"
        device.clean = {
            "device_recovery": {
                "tftp_boot": {"tftp_server": "configured-tftp"},
            },
        }

        with self.assertLogs(
                "genie.libs.sdk.libs.utils.utils", level="INFO") as logs:
            result = get_recovery_tftp_server(device)

        self.assertEqual(result, "configured-tftp")
        self.assertIn("from clean data", " ".join(logs.output))
