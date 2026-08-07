import os
import unittest
from unittest.mock import Mock, patch
from pyats.topology import loader
from unicon.core.errors import SubCommandFailure
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
        self.device = self.testbed.devices["ott-c9400-05"]
        # To test the TFTP_FILE rommon variable
        self.device.clean.images = ["flash:/test.bin"]
        self.device.connect(mit=True)

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
        self.device = self.testbed.devices["ott-c9400-05"]
        # To test the TFTP_FILE rommon variable
        self.device.clean.images = ["flash:/test.bin"]
        self.device.connect(mit=True)

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
        self.device = self.testbed.devices["ott-c9400-05"]
        # To test the TFTP_FILE rommon variable
        self.device.clean.images = ["flash:/test.bin"]
        self.device.connect(mit=True)

    def test_configure_rommon_tftp(self):
        result = configure_rommon_tftp_ha(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)


class TestConfigureRommonTftpHA_4(unittest.TestCase):
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
        self.device = self.testbed.devices["ott-c9400-05"]
        self.device.clean.images = ["faulty_image"]
        self.device.connect(mit=True)

    def test_configure_rommon_tftp(self):
        result = configure_rommon_tftp_ha(self.device, image_path="valid_image.bin")
        expected_output = None
        self.assertEqual(result, expected_output)


class TestConfigureRommonTftpHA_5(unittest.TestCase):

    @staticmethod
    def _get_device(aliases, rommon):
        device = Mock()
        device.name = 'ott-c9600-7-02'
        device.is_ha = True
        device.subconnections = [Mock() for _ in aliases]
        for alias, connection in zip(aliases, device.subconnections):
            connection.alias = alias
            connection.state_machine.current_state = 'rommon'
        device.management = {'rommon': rommon}
        return device

    def test_missing_rp_recovery_information(self):
        device = self._get_device(
            ('a', 'b'),
            {
                'rp0': {
                    'address': {'ipv4': '5.5.5.5/16'},
                    'gateway': {'ipv4': '1.1.1.1'},
                },
                'metadata': {'description': 'not an RP entry'},
            })

        with self.assertRaisesRegex(
                SubCommandFailure,
                r"(?s)Missing ROMMON recovery information for "
                r"subconnection 'b':.*"
                r'ROMMON IPv4 address \(address.ipv4\).*'
                r'ROMMON IPv4 gateway \(gateway.ipv4\)'):
            configure_rommon_tftp_ha(device, image_path='test.bin')

    def test_missing_rp_recovery_information_ipv6_for_three_rps(self):
        device = self._get_device(
            ('a', 'b', 'c'),
            {
                'rp0': {
                    'address': {'ipv6': '2001:db8::1/64'},
                    'gateway': {'ipv6': '2001:db8::ff'},
                }
            })

        with self.assertRaisesRegex(
                SubCommandFailure,
                r"(?s)Missing ROMMON recovery information for "
                r"subconnection 'b':.*"
                r'ROMMON IPv6 address \(address.ipv6\).*'
                r'ROMMON IPv6 gateway \(gateway.ipv6\).*'
                r"Missing ROMMON recovery information for "
                r"subconnection 'c':.*"
                r'ROMMON IPv6 address \(address.ipv6\).*'
                r'ROMMON IPv6 gateway \(gateway.ipv6\)'):
            configure_rommon_tftp_ha(
                device, use_ipv6=True, image_path='test.bin')

    def test_no_rp_recovery_information(self):
        device = self._get_device(('a', 'b'), {})

        with self.assertRaisesRegex(
                SubCommandFailure,
                r"(?s)Missing ROMMON recovery information for "
                r"subconnection 'a':.*"
                r'ROMMON IPv4 address \(address.ipv4\).*'
                r'ROMMON IPv4 gateway \(gateway.ipv4\).*'
                r"Missing ROMMON recovery information for "
                r"subconnection 'b':.*"
                r'ROMMON IPv4 address \(address.ipv4\).*'
                r'ROMMON IPv4 gateway \(gateway.ipv4\)'):
            configure_rommon_tftp_ha(device, image_path='test.bin')

    def test_missing_rommon_recovery_field(self):
        device = self._get_device(
            ('a',),
            {
                'rp0': {
                    'address': {'ipv4': '5.5.5.5/16'},
                    'gateway': {},
                },
            })

        with self.assertRaisesRegex(
                SubCommandFailure,
                r"(?s)Missing ROMMON recovery information for "
                r"subconnection 'a':.*"
                r'ROMMON IPv4 gateway \(gateway.ipv4\)') as context:
            configure_rommon_tftp_ha(device, image_path='test.bin')

        self.assertNotIn('ROMMON IPv4 address', str(context.exception))

    def test_rp_entries_are_processed_by_rp_number(self):
        device = self._get_device(
            ('a', 'b', 'c'),
            {
                'rp2': {
                    'address': {'ipv4': '7.7.7.7/16'},
                    'gateway': {'ipv4': '3.3.3.3'},
                },
                'metadata': {'description': 'not an RP entry'},
                'rp0': {
                    'address': {'ipv4': '5.5.5.5/16'},
                    'gateway': {'ipv4': '1.1.1.1'},
                },
                'rp1': {
                    'address': {'ipv4': '6.6.6.6/16'},
                    'gateway': {'ipv4': '2.2.2.2'},
                },
            })

        with patch(
                'genie.libs.sdk.apis.iosxe.rommon.configure.'
                'get_image_handler') as image_handler:
            image_handler.return_value.image = []
            configure_rommon_tftp_ha(device, image_path='test.bin')

        self.assertEqual(
            [connection.execute.call_args_list[0][0][0]
             for connection in device.subconnections],
            ['IP_ADDRESS=5.5.5.5',
             'IP_ADDRESS=6.6.6.6',
             'IP_ADDRESS=7.7.7.7'])
