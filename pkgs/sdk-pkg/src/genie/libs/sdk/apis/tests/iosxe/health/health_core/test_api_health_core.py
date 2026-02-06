import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.health.health import health_core
from unicon.plugins.tests.mock.mock_device_iosxe import MockDeviceTcpWrapperIOSXE
from unittest.mock import MagicMock, patch, Mock

class TestHealthCore(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.md = MockDeviceTcpWrapperIOSXE(hostname='R1',
                                           port=0,
                                           state='cat3k_login')
        cls.md.start()

        cls.testbed = """
        devices:
          R1:
            os: iosxe
            type: router
            tacacs:
                username: cisco
            passwords:
                tacacs: cisco
            connections:
              defaults:
                class: unicon.Unicon
              a:
                protocol: telnet
                ip: 127.0.0.1
                port: {}
        """.format(cls.md.ports[0])

    @classmethod
    def tearDownClass(cls):
        cls.md.stop()

    def test_health_core(self):
        self.testbed = loader.load(self.testbed)
        self.device = self.testbed.devices['R1']
        self.device.connect(learn_hostname=True,
                            init_config_commands=[],
                            init_exec_commands=[])
        result = health_core(self.device)
        expected_output = {
            'health_data': {
                'num_of_cores':
                1,
                'corefiles': [{
                    'filename':
                    'kernel.NA_CAT9K_NA_20220519205207.core.gz'
                }]
            }
        }
        self.assertEqual(result, expected_output)


class TestHealthCoreStack(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.md = MockDeviceTcpWrapperIOSXE(hostname='Router',
                                           port=0,
                                           state='stack_enable' +
                                           ',stack_enable' * 2,
                                           stack=True)
        cls.md.start()
        cls.testbed = '''
            devices:
              Router:
                type: router
                os: iosxe
                chassis_type: stack
                connections:
                  defaults:
                    class: 'unicon.Unicon'
                    connections: [p1, p2, p3]
                  p1:
                    protocol: telnet
                    ip: 127.0.0.1
                    port: {}
                  p2:
                    protocol: telnet
                    ip: 127.0.0.1
                    port: {}
                  p3:
                    protocol: telnet
                    ip: 127.0.0.1
                    port: {}
            '''.format(cls.md.ports[0], cls.md.ports[1], cls.md.ports[2])

    def test_health_core_stack(self):

        self.testbed = loader.load(self.testbed)
        self.device = self.testbed.devices['Router']
        self.device.connect()
        result = health_core(self.device)
        expected_output = {
            'health_data': {
                'num_of_cores':
                4,
                'corefiles': [{
                    'filename':
                    'CAT3K_CAA-1-UNIVERSALK9_20150104-042336-UTC.core.gz'
                }, {
                    'filename':
                    'CAT3K_CAA-2-UNIVERSALK9_20150104-042336-UTC.core.gz'
                }, {
                    'filename':
                    'CAT3K_CAA-UNIVERSALK9-042336-UTC.core.gz.coregen.dbg'
                }, {
                    'filename':
                    'CAT3K_CAA-3-UNIVERSALK9_20150104-042336-UTC.core.gz'
                }],
            }
        }
        self.assertEqual(result, expected_output)

    @classmethod
    def tearDownClass(cls):
        cls.md.stop()


class TestHealthCoreHA(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.md = MockDeviceTcpWrapperIOSXE(hostname='R1',
                                           port=0,
                                           state='asr_login,asr_exec_standby')
        cls.md.start()

        cls.testbed = """
        devices:
          R1:
            os: iosxe
            type: router
            tacacs:
                username: cisco
            passwords:
                tacacs: cisco
            connections:
              defaults:
                class: unicon.Unicon
              a:
                protocol: telnet
                ip: 127.0.0.1
                port: {}
              b:
                protocol: telnet
                ip: 127.0.0.1
                port: {}
        """.format(cls.md.ports[0], cls.md.ports[1])

    def test_health_core_HA(self):

        self.testbed = loader.load(self.testbed)
        self.device = self.testbed.devices['R1']
        self.device.connect()
        result = health_core(self.device)
        expected_output = {
            'health_data': {
                'num_of_cores':
                2,
                'corefiles': [{
                    'filename':
                    'UNIVERSALK9_20150104-042336-UTC.core.gz'
                }, {
                    'filename':
                    'UNIVERSALK9_20150105-042336-UTC.core.gz'
                }],
            }
        }
        self.assertEqual(result, expected_output)

    @classmethod
    def tearDownClass(cls):
        cls.md.stop()

class TestHealthCoreNewFiles(unittest.TestCase):

    @patch('genie.libs.sdk.apis.iosxe.health.health.runtime')
    @patch('genie.libs.sdk.apis.iosxe.health.health.log')
    def test_health_core_new_files_detection(self, mock_log, mock_runtime):
        self.device = Mock()
        self.device.parse = MagicMock()
        self.device.name = 'R1'
        self.device.hostname = 'R1'
        self.device.os = 'iosxe'
        self.device.type = 'router'
        self.device.platform = 'iosxe'
        self.device.is_connected = True

        self.device.is_ha = False

        self.device.cli = MagicMock()
        self.device.cli.is_connected = True
        self.device.filesystems = {'bootflash:/': {}}

        self.device.api = MagicMock()
        self.device.api.get_core_directories.return_value = ['bootflash:/core/']
        mock_runtime.health_data = {}
        mock_runtime.synchro.dict.return_value = {}
        mock_runtime.directory = "/tmp"

        mock_runtime.health_data = {}
        mock_runtime.synchro.dict.return_value = {}
        mock_runtime.directory = "/tmp"

        base_dir = 'bootflash:/core/'

        known_filename = 'existing_core_1.core.gz'
        known_core_full_path = known_filename

        mock_runtime.health_data.setdefault(self.device.name, {'core': {'corefiles': []}})
        mock_runtime.health_data[self.device.name]['core']['corefiles'].append(
            {'filename': known_core_full_path}
        )

        new_filename = 'new_core_2.core.gz'
        mock_parsed_output = MagicMock()
        mock_parsed_output.q.get_values.return_value = [known_filename, new_filename]
        self.device.parse = MagicMock(return_value=mock_parsed_output)

        mock_log.info.reset_mock()

        result = health_core(self.device, default_dir=[base_dir])

        expected_result = {
            'health_data': {
                'num_of_cores': 1,
                'corefiles': [{
                    'filename': 'new_core_2.core.gz'
                }],
            }
        }
        self.assertEqual(result, expected_result)

        self.assertEqual(
            mock_runtime.health_data[self.device.name]['core']['corefiles'],
            [{'filename': known_core_full_path}, {'filename': new_filename}]
        )
