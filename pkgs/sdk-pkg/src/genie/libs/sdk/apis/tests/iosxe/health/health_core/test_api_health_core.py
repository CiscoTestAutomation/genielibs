import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.health.health import health_core
from unicon.plugins.tests.mock.mock_device_iosxe import MockDeviceTcpWrapperIOSXE


class TestHealthCore(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.md = MockDeviceTcpWrapperIOSXE(
            hostname='R1',
            port=0, state='cat3k_login')
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
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )
        result = health_core(self.device)
        expected_output = {'health_data': {'num_of_cores': 1, 'corefiles': [{'filename': 'kernel.NA_CAT9K_NA_20220519205207.core.gz'}]}}
        self.assertEqual(result, expected_output)
