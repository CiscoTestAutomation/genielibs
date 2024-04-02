import unittest
from unittest.mock import patch, call
from unittest.mock import Mock, ANY

from pyats.topology import loader
from genie.libs.sdk.apis.execute import (
    execute_power_cycle_device,
    execute_power_on_device,
    execute_power_off_device,
)


class TestExecutePowerCyclerApis(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        testbed = """
devices:
  FW-9800-7:
    connections:
      defaults:
        class: unicon.Unicon
      a:
        command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
        protocol: unknown
    peripherals:
      power_cycler:
        - type: raritan-px2
          connection_type: snmp
          read_community: public
          write_community: private
          host: 127.0.0.1
          outlets: [11]
    os: iosxe
    platform: c9800
    type: c9800
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices["FW-9800-7"]

    def test_execute_power_cycle_device(self):
        with patch(
            "genie.libs.sdk.powercycler.snmp_client.SNMPClient.snmp_set"
        ) as set_mock, patch("time.sleep"):
            execute_power_cycle_device(self.device)
            expected_calls = [
                call(oid="1.3.6.1.4.1.13742.6.4.1.2.1.2.1.11", value=0, type="Integer"),
                call(oid="1.3.6.1.4.1.13742.6.4.1.2.1.2.1.11", value=1, type="Integer"),
            ]
            self.assertEqual(set_mock.call_args_list, expected_calls)

    def test_execute_power_on_device(self):
        with patch(
            "genie.libs.sdk.powercycler.snmp_client.SNMPClient.snmp_set"
        ) as set_mock, patch("time.sleep"):
            execute_power_on_device(self.device)
            expected_calls = [
                call(oid="1.3.6.1.4.1.13742.6.4.1.2.1.2.1.11", value=1, type="Integer"),
            ]
            self.assertEqual(set_mock.call_args_list, expected_calls)

    def test_execute_power_off_device(self):
        with patch(
            "genie.libs.sdk.powercycler.snmp_client.SNMPClient.snmp_set"
        ) as set_mock, patch("time.sleep"):
            execute_power_off_device(self.device)
            expected_calls = [
                call(oid="1.3.6.1.4.1.13742.6.4.1.2.1.2.1.11", value=0, type="Integer"),
            ]
            self.assertEqual(set_mock.call_args_list, expected_calls)


class TestExecutePowerCyclerApis_2(unittest.TestCase):
    """
    To test the raritan-px2 powercycler snmpv3 implementation
    """
    @classmethod
    def setUpClass(self):
        testbed = """
devices:
  FW-9800-7:
    connections:
      defaults:
        class: unicon.Unicon
      a:
        command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
        protocol: unknown
    peripherals:
      power_cycler:
          - type: raritan-px2
            connection_type: snmpv3
            host: vmtb-pdu1
            outlets: [15]
            username: test
            auth_key: test
            auth_protocol: md5
            priv_key: test
            priv_protocol: aes128
            security_level: authpriv
    os: iosxe
    platform: c9800
    type: c9800
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices["FW-9800-7"]

    def test_execute_power_cycle_device(self):
        with patch(
            "genie.libs.sdk.powercycler.snmp_client.SNMPv3Client.snmp_set"
        ) as set_mock, patch("time.sleep"):
            execute_power_cycle_device(self.device)
            expected_calls = [
                call(oid="1.3.6.1.4.1.13742.6.4.1.2.1.2.1.15", value=0, type="Integer"),
                call(oid="1.3.6.1.4.1.13742.6.4.1.2.1.2.1.15", value=1, type="Integer"),
            ]
            self.assertEqual(set_mock.call_args_list, expected_calls)

    def test_execute_power_on_device(self):
        with patch(
            "genie.libs.sdk.powercycler.snmp_client.SNMPv3Client.snmp_set"
        ) as set_mock, patch("time.sleep"):
            execute_power_on_device(self.device)
            expected_calls = [
                call(oid="1.3.6.1.4.1.13742.6.4.1.2.1.2.1.15", value=1, type="Integer"),
            ]
            self.assertEqual(set_mock.call_args_list, expected_calls)

    def test_execute_power_off_device(self):
        with patch(
            "genie.libs.sdk.powercycler.snmp_client.SNMPv3Client.snmp_set"
        ) as set_mock, patch("time.sleep"):
            execute_power_off_device(self.device)
            expected_calls = [
                call(oid="1.3.6.1.4.1.13742.6.4.1.2.1.2.1.15", value=0, type="Integer"),
            ]
            self.assertEqual(set_mock.call_args_list, expected_calls)


class TestExecutePowerCyclerApis_3(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        testbed = """
devices:
  FW-9800-7:
    connections:
      defaults:
        class: unicon.Unicon
      a:
        command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
        protocol: unknown
    peripherals:
      power_cycler:
          - type: generic-cli
            host: localhost
            connection_type: ssh
            outlets: [6]
            commands:
                power_on: "power outlets {outlet} on"
                power_off: "power outlets {outlet} off"

    os: iosxe
    platform: c9800
    type: c9800

  localhost:
      os: linux
      connections:
          a:
              ip: localhost
              protocol: ssh
      credentials:
         default:
             username: test
             password: test

        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices["FW-9800-7"]
        self.server = self.testbed.devices["localhost"]


    def test_execute_power_on_device(self):
        with patch("time.sleep"):
            self.server.connect = Mock()
            self.server.execute = Mock()
            execute_power_on_device(self.device)
            expected_calls = [
                call('power outlets 6 on', reply=ANY),
            ]
            self.assertEqual(self.server.execute.call_args_list, expected_calls)


    def test_execute_power_off_device(self):
        with patch("time.sleep"):
            self.server.connect = Mock()
            self.server.execute = Mock()
            execute_power_off_device(self.device)
            expected_calls = [
                call('power outlets 6 off', reply=ANY),
            ]
            self.assertEqual(self.server.execute.call_args_list, expected_calls)


class TestExecutePowerCyclerApis_4(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        testbed = """
devices:
  FW-9800-7:
    connections:
      defaults:
        class: unicon.Unicon
      a:
        command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
        protocol: unknown
    peripherals:
      power_cycler:
          - type: generic-cli
            host: localhost
            connection_type: ssh
            commands:
                power_on: "power-tool %{self} on"
                power_off: "power-tool %{self} off"

    os: iosxe
    platform: c9800
    type: c9800

  localhost:
      os: linux
      connections:
          a:
              ip: localhost
              protocol: ssh
      credentials:
         default:
             username: test
             password: test

        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices["FW-9800-7"]
        self.server = self.testbed.devices["localhost"]


    def test_execute_power_on_device(self):
        with patch("time.sleep"):
            self.server.connect = Mock()
            self.server.execute = Mock()
            execute_power_on_device(self.device)
            expected_calls = [
                call('power-tool FW-9800-7 on'),
            ]
            self.assertEqual(self.server.execute.call_args_list, expected_calls)

    def test_execute_power_off_device(self):
        with patch("time.sleep"):
            self.server.connect = Mock()
            self.server.execute = Mock()
            execute_power_off_device(self.device)
            expected_calls = [
                call('power-tool FW-9800-7 off'),
            ]
            self.assertEqual(self.server.execute.call_args_list, expected_calls)


class TestExecutePowerCyclerApis_5(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        testbed = """
devices:
  FW-9800-7:
    connections:
      defaults:
        class: unicon.Unicon
      a:
        command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
        protocol: unknown
    peripherals:
      power_cycler:
          - type: Raritan
            host: localhost
            connection_type: telnet
            outlets: [7]

    os: iosxe
    platform: c9800
    type: c9800

  localhost:
      os: linux
      connections:
          a:
              ip: localhost
              protocol: telnet
      credentials:
         default:
             username: test
             password: test

        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices["FW-9800-7"]
        self.server = self.testbed.devices["localhost"]


    def test_execute_power_on_device(self):
        with patch("time.sleep"):
            self.server.connect = Mock()
            self.server.execute = Mock()
            execute_power_on_device(self.device)
            expected_calls = [
                call('power outlets 7 on', reply=ANY),
            ]
            self.assertEqual(self.server.execute.call_args_list, expected_calls)


    def test_execute_power_off_device(self):
        with patch("time.sleep"):
            self.server.connect = Mock()
            self.server.execute = Mock()
            execute_power_off_device(self.device)
            expected_calls = [
                call('power outlets 7 off', reply=ANY),
            ]
            self.assertEqual(self.server.execute.call_args_list, expected_calls)


class TestExecutePowerCyclerApis__6(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        testbed = """
devices:
  FW-9800-7:
    connections:
      defaults:
        class: unicon.Unicon
      a:
        command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
        protocol: unknown
    peripherals:
      power_cycler:
        - type: raritan-px2
          connection_type: snmp
          read_community: public
          write_community: private
          host: 127.0.0.1
          outlets: [11]
          proxy: proxy
    os: iosxe
    platform: c9800
    type: c9800
  proxy:
      os: linux
      connections:
          a:
              command: mock_device_cli --os linux --mock_data_dir mock_data --state connect
              protocol: telnet
      credentials:
         default:
             username: test
             password: test
testbed:
  servers:
    proxy:
      address: 10.1.1.1
      credentials:
        default:
          password: test
          username: test
        enable:
          password: ''
      path: /
      protocol: scp
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices["FW-9800-7"]

    def test_execute_power_cycle_device(self):
        with patch(
            "genie.libs.sdk.powercycler.snmp_client.SNMPClient.snmp_set"
        ) as set_mock, patch("time.sleep"):
            with patch(
            "genie.libs.sdk.apis.utils.get_remote_ip"
        ) as set_mock_1, patch("time.sleep"):
                self.device.api.execute_power_cycle_device()
                expected_calls = [
                    call(oid='1.3.6.1.4.1.13742.6.4.1.2.1.2.1.11', value=0, type='Integer'),
                    call(oid='1.3.6.1.4.1.13742.6.4.1.2.1.2.1.11', value=1, type='Integer')
                ]
                self.assertEqual(set_mock.call_args_list, expected_calls)
