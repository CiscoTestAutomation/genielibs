import unittest
import threading
from types import SimpleNamespace
from unittest.mock import patch, call
from unittest.mock import Mock, ANY

from pyats.topology import loader
from genie.libs.sdk.apis.execute import (
    execute_power_cycle_device,
    execute_power_on_device,
    execute_power_off_device,
    change_power_cycler_state,
    _change_power_cycler_config_state,
)
from genie.libs.sdk.apis.utils import get_power_cyclers


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


class TestExecutePowerCyclerApisMultiplePowerCyclers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
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
        - type: raritan-px2
          connection_type: snmp
          read_community: public
          write_community: private
          host: 127.0.0.2
          outlets: [12]
    os: iosxe
    platform: c9800
    type: c9800
        """
        cls.testbed = loader.load(testbed)
        cls.device = cls.testbed.devices["FW-9800-7"]
        if not hasattr(cls.device, 'api'):
            cls.device.api = SimpleNamespace(
                change_power_cycler_state=(
                    lambda powercycler, state, outlets:
                    change_power_cycler_state(
                        cls.device, powercycler, state, outlets)),
                execute_power_off_device=(
                    lambda: execute_power_off_device(cls.device)),
                execute_power_on_device=(
                    lambda: execute_power_on_device(cls.device)))

    @staticmethod
    def _threaded_pcall(target, ikwargs=(), **kwargs):
        results = [None] * len(ikwargs)
        errors = [None] * len(ikwargs)

        def run(index, call_kwargs):
            try:
                results[index] = target(**call_kwargs)
            except Exception as e:
                errors[index] = e

        threads = [
            threading.Thread(target=run, args=(index, call_kwargs))
            for index, call_kwargs in enumerate(ikwargs)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        for error in errors:
            if error:
                raise error
        return tuple(results)

    def test_execute_power_cycle_device_groups_parallel_off_delay_and_on(self):
        expected_off_oids = [
            "1.3.6.1.4.1.13742.6.4.1.2.1.2.1.11",
            "1.3.6.1.4.1.13742.6.4.1.2.1.2.1.12",
        ]
        expected_on_oids = list(expected_off_oids)
        started = {0: [], 1: []}
        all_started = {0: threading.Event(), 1: threading.Event()}
        events = []
        lock = threading.Lock()

        def snmp_set_side_effect(oid, value, type="Integer"):
            with lock:
                started[value].append(oid)
                events.append(value)
                if len(started[value]) == 2:
                    all_started[value].set()

            if not all_started[value].wait(2):
                raise AssertionError(
                    "powercycler state change was serialized")
            return []

        def sleep_side_effect(delay):
            with lock:
                events.append("sleep")

        with patch(
            "genie.libs.sdk.powercycler.snmp_client.SNMPClient.snmp_set",
            side_effect=snmp_set_side_effect
        ), patch("time.sleep", side_effect=sleep_side_effect), patch(
            "genie.libs.sdk.apis.execute.pcall",
            side_effect=self._threaded_pcall
        ) as pcall_mock:
            execute_power_cycle_device(self.device, delay=7)

        self.assertCountEqual(started[0], expected_off_oids)
        self.assertCountEqual(started[1], expected_on_oids)
        self.assertEqual(pcall_mock.call_count, 2)
        self.assertEqual(events.count("sleep"), 1)
        sleep_index = events.index("sleep")
        self.assertTrue(all(event == 0 for event in events[:sleep_index]))
        self.assertTrue(all(event == 1 for event in events[sleep_index + 1:]))

    def test_execute_power_off_device_reports_each_failing_powercycler(self):
        called = []
        lock = threading.Lock()

        def snmp_set_side_effect(oid, value, type="Integer"):
            with lock:
                called.append((oid, value))
            if oid.endswith(".11"):
                raise RuntimeError("first PDU failed")
            raise RuntimeError("second PDU failed")

        with patch(
            "genie.libs.sdk.powercycler.snmp_client.SNMPClient.snmp_set",
            side_effect=snmp_set_side_effect
        ), patch(
            "genie.libs.sdk.apis.execute.pcall",
            side_effect=self._threaded_pcall
        ):
            with self.assertRaises(Exception) as cm:
                execute_power_off_device(self.device)

        message = str(cm.exception)
        self.assertIn("Failed to powercycle device off", message)
        self.assertIn("host='127.0.0.1'", message)
        self.assertIn("outlets=[11]", message)
        self.assertIn("first PDU failed", message)
        self.assertIn("host='127.0.0.2'", message)
        self.assertIn("outlets=[12]", message)
        self.assertIn("second PDU failed", message)
        self.assertCountEqual(
            called,
            [
                ("1.3.6.1.4.1.13742.6.4.1.2.1.2.1.11", 0),
                ("1.3.6.1.4.1.13742.6.4.1.2.1.2.1.12", 0),
            ])

    def test_multiple_powercyclers_are_constructed_inside_pcall(self):
        device = SimpleNamespace(
            name='FW-9800-7',
            testbed=SimpleNamespace(),
            peripherals={
                'power_cycler': [
                    {
                        'type': 'generic-cli',
                        'connection_type': 'ssh',
                        'host': 'pdu-1',
                        'outlets': [1],
                    },
                    {
                        'type': 'generic-cli',
                        'connection_type': 'ssh',
                        'host': 'pdu-2',
                        'outlets': [2],
                    },
                ],
            },
        )
        created = []
        calls = []

        class FakePowerCycler:
            def __init__(self, **kwargs):
                self.host = kwargs['host']
                self.type = kwargs['type']
                self.proxy_dev = None
                created.append(self)

            def off(self, *outlets):
                calls.append((self.host, outlets))

            def disconnect(self):
                pass

        def fake_pcall(target, ikwargs=(), **kwargs):
            self.assertEqual(created, [])
            self.assertNotIn('timeout', kwargs)
            return tuple(target(**call_kwargs) for call_kwargs in ikwargs)

        with patch(
            "genie.libs.sdk.apis.execute.PowerCycler",
            side_effect=lambda **kwargs: FakePowerCycler(**kwargs)
        ), patch(
            "genie.libs.sdk.apis.execute.pcall",
            side_effect=fake_pcall
        ) as pcall_mock:
            execute_power_off_device(device)

        self.assertEqual(pcall_mock.call_count, 1)
        self.assertEqual(len(created), 2)
        self.assertEqual(len({id(powercycler) for powercycler in created}), 2)
        self.assertEqual(calls, [('pdu-1', (1,)), ('pdu-2', (2,))])

    def test_execute_power_off_device_reports_timed_out_powercycler(self):
        disconnected = []

        class FakePowerCycler:
            def __init__(self, **kwargs):
                self.host = kwargs['host']
                self.type = kwargs['type']
                self.proxy_dev = None

            def off(self, *outlets):
                import time
                time.sleep(10)

            def disconnect(self):
                disconnected.append(self.host)

        def fake_pcall(target, ikwargs=(), **kwargs):
            self.assertNotIn('timeout', kwargs)
            return tuple(target(**call_kwargs) for call_kwargs in ikwargs)

        with patch(
            "genie.libs.sdk.apis.execute.pcall",
            side_effect=fake_pcall
        ), patch(
            "genie.libs.sdk.apis.execute."
            "POWER_CYCLER_STATE_CHANGE_TIMEOUT",
            0.1
        ), patch(
            "genie.libs.sdk.apis.execute.PowerCycler",
            side_effect=lambda **kwargs: FakePowerCycler(**kwargs)
        ):
            with self.assertRaises(Exception) as cm:
                execute_power_off_device(self.device)

        message = str(cm.exception)
        self.assertIn("Failed to powercycle device off", message)
        self.assertIn("host='127.0.0.1'", message)
        self.assertIn("outlets=[11]", message)
        self.assertIn("host='127.0.0.2'", message)
        self.assertIn("outlets=[12]", message)
        self.assertIn("timed out after 0.1 seconds", message)
        self.assertCountEqual(disconnected, ['127.0.0.1', '127.0.0.2'])

    def test_timed_out_powercycler_init_runs_proxy_cleanup(self):
        disconnected = []

        class ProxyDevice:
            connected = True

            def disconnect(self):
                disconnected.append('proxy')

        class PowerCycler:
            __module__ = 'genie.libs.sdk.powercycler.base'

            def __new__(cls, **kwargs):
                return object.__new__(cls)

            def __init__(self, **kwargs):
                self.host = kwargs['host']
                self.type = kwargs['type']
                self.proxy_dev = ProxyDevice()
                self.socat_pid = 123
                import time
                time.sleep(10)

            def disconnect(self):
                disconnected.append('powercycler')

        power_cycler = {
            'type': 'raritan-px2',
            'connection_type': 'snmp',
            'host': '127.0.0.1',
        }

        with patch(
            "genie.libs.sdk.apis.execute.PowerCycler",
            PowerCycler
        ):
            error = _change_power_cycler_config_state(
                'FW-9800-7', power_cycler, [11], 'off', timeout=0.1)

        self.assertIn("host='127.0.0.1'", error)
        self.assertIn("timed out after 0.1 seconds", error)
        self.assertEqual(disconnected, ['powercycler', 'proxy'])


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


class TestSNMPv3PowerCyclerCredentials(unittest.TestCase):
    def test_uses_powercycler_credentials(self):
        testbed = """
devices:
  FW-9800-7:
    connections:
      defaults:
        class: unicon.Unicon
      a:
        command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
        protocol: unknown
    credentials:
      default:
        username: device-user
        password: device-password
    peripherals:
      power_cycler:
          - type: raritan-px2
            connection_type: snmpv3
            host: vmtb-pdu1
            outlets: [15]
            credentials:
              default:
                username: pdu-user
                password: pdu-password
            auth_protocol: md5
            priv_protocol: aes128
            security_level: authpriv
    os: iosxe
    platform: c9800
    type: c9800
        """
        device = loader.load(testbed).devices["FW-9800-7"]

        powercycler, _ = get_power_cyclers(device)[0]

        self.assertEqual(powercycler.auth.userName, "pdu-user")
        self.assertEqual(powercycler.auth.authentication_key, "pdu-password")
        self.assertEqual(powercycler.auth.privacy_key, "pdu-password")

    def test_uses_powercycler_fields_with_case_insensitive_options(self):
        testbed = """
devices:
  FW-9800-7:
    connections:
      defaults:
        class: unicon.Unicon
      a:
        command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
        protocol: unknown
    credentials:
      default:
        username: device-user
        password: device-password
    peripherals:
      power_cycler:
          - type: raritan-px2
            connection_type: snmpv3
            host: vmtb-pdu1
            outlets: [15]
            username: pdu-user
            auth_key: pdu-password
            auth_protocol: MD5
            security_level: authNoPriv
    os: iosxe
    platform: c9800
    type: c9800
        """
        device = loader.load(testbed).devices["FW-9800-7"]

        powercycler, _ = get_power_cyclers(device)[0]

        self.assertEqual(powercycler.auth.userName, "pdu-user")
        self.assertEqual(powercycler.auth.authentication_key, "pdu-password")
        self.assertFalse(powercycler.auth.privacy_key)

    def test_does_not_fall_back_to_device_default_credentials(self):
        testbed = """
devices:
  FW-9800-7:
    connections:
      defaults:
        class: unicon.Unicon
      a:
        command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
        protocol: unknown
    credentials:
      default:
        username: device-user
        password: device-password
    peripherals:
      power_cycler:
          - type: raritan-px2
            connection_type: snmpv3
            host: vmtb-pdu1
            outlets: [15]
    os: iosxe
    platform: c9800
    type: c9800
        """
        device = loader.load(testbed).devices["FW-9800-7"]

        with self.assertRaisesRegex(ValueError, "SNMPv3 powercycler requires a username"):
            get_power_cyclers(device)

    def test_snmpv3_requires_username(self):
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
    os: iosxe
    platform: c9800
    type: c9800
        """
        device = loader.load(testbed).devices["FW-9800-7"]

        with self.assertRaisesRegex(ValueError, "SNMPv3 powercycler requires a username"):
            get_power_cyclers(device)

    def test_invalid_security_level_fails(self):
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
            username: pdu-user
            security_level: authPrvi
    os: iosxe
    platform: c9800
    type: c9800
        """
        device = loader.load(testbed).devices["FW-9800-7"]

        with self.assertRaisesRegex(ValueError, "Invalid SNMPv3 security_level"):
            get_power_cyclers(device)

    def test_non_string_security_level_fails(self):
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
            username: pdu-user
            security_level: 3
    os: iosxe
    platform: c9800
    type: c9800
        """
        device = loader.load(testbed).devices["FW-9800-7"]

        with self.assertRaisesRegex(ValueError, "security_level must be a string"):
            get_power_cyclers(device)

    def test_invalid_auth_protocol_fails(self):
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
            username: pdu-user
            auth_key: pdu-password
            auth_protocol: bad
            security_level: authnopriv
    os: iosxe
    platform: c9800
    type: c9800
        """
        device = loader.load(testbed).devices["FW-9800-7"]

        with self.assertRaisesRegex(ValueError, "Invalid SNMPv3 authentication protocol"):
            get_power_cyclers(device)

    def test_non_string_auth_protocol_fails(self):
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
            username: pdu-user
            auth_key: pdu-password
            auth_protocol: 3
            security_level: authnopriv
    os: iosxe
    platform: c9800
    type: c9800
        """
        device = loader.load(testbed).devices["FW-9800-7"]

        with self.assertRaisesRegex(ValueError, "authentication protocol must be a string"):
            get_power_cyclers(device)

    def test_invalid_priv_protocol_fails(self):
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
            username: pdu-user
            auth_key: pdu-password
            auth_protocol: md5
            priv_key: pdu-password
            priv_protocol: bad
            security_level: authpriv
    os: iosxe
    platform: c9800
    type: c9800
        """
        device = loader.load(testbed).devices["FW-9800-7"]

        with self.assertRaisesRegex(ValueError, "Invalid SNMPv3 privacy protocol"):
            get_power_cyclers(device)

    def test_non_string_priv_protocol_fails(self):
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
            username: pdu-user
            auth_key: pdu-password
            auth_protocol: md5
            priv_key: pdu-password
            priv_protocol: 3
            security_level: authpriv
    os: iosxe
    platform: c9800
    type: c9800
        """
        device = loader.load(testbed).devices["FW-9800-7"]

        with self.assertRaisesRegex(ValueError, "privacy protocol must be a string"):
            get_power_cyclers(device)


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



class TestExecutePowerCyclerApisProxmox(unittest.TestCase):
    """
    To test the Proxmox powercycler ssh implementation
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
              - type: proxmox
                connection_type: ssh
                host: localhost
                outlets: [101]
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
            self.server.execute = Mock(return_value="")

            execute_power_on_device(self.device)

            expected_calls = [
                call('qm start 101'),
            ]
            self.assertEqual(self.server.execute.call_args_list, expected_calls)


    def test_execute_power_off_device(self):
        with patch("time.sleep"):
            self.server.connect = Mock()
            self.server.execute = Mock(return_value="")

            execute_power_off_device(self.device)

            expected_calls = [
                call('qm stop 101'),
            ]
            self.assertEqual(self.server.execute.call_args_list, expected_calls)
    
    def test_execute_power_on_device_vm_not_exist(self):
        with patch("time.sleep"):
            self.server.connect = Mock()
            self.server.execute = Mock(return_value="Configuration file 'nodes/cisco/qemu-server/101.conf' does not exist")

            with self.assertRaises(Exception) as cm:
                execute_power_on_device(self.device)

            self.assertIn("does not exist", str(cm.exception))
            self.assertIn("Failed to powercycle device on", str(cm.exception))
