import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.health.health import health_core
from unicon.plugins.tests.mock.mock_device_iosxe import MockDeviceTcpWrapperIOSXE


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
                    'bootflash:/core/kernel.NA_CAT9K_NA_20220519205207.core.gz'
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
                5,
                'corefiles': [{
                    'filename':
                    'flash-1:/core/CAT3K_CAA-1-UNIVERSALK9_20150104-042336-UTC.core.gz'
                }, {
                    'filename':
                    'flash-2:/core/CAT3K_CAA-2-UNIVERSALK9_20150104-042336-UTC.core.gz'
                }, {
                    'filename':
                    'flash-2:/core/CAT3K_CAA-UNIVERSALK9-042336-UTC.core.gz.coregen.dbg'
                }, {
                    'filename':
                    'flash-3:/core/CAT3K_CAA-3-UNIVERSALK9_20150104-042336-UTC.core.gz'
                }, {
                    'filename':
                    'flash-3:/core/CAT3K_CAA-UNIVERSALK9-042336-UTC.core.gz.coregen.dbg'
                }]
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
                    'bootflash:/core/UNIVERSALK9_20150104-042336-UTC.core.gz'
                }, {
                    'filename':
                    'stby-bootflash:/core/UNIVERSALK9_20150105-042336-UTC.core.gz'
                }]
            }
        }
        self.assertEqual(result, expected_output)

    @classmethod
    def tearDownClass(cls):
        cls.md.stop()
