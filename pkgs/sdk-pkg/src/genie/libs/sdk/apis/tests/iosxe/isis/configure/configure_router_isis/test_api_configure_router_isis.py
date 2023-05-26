import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.isis.configure import configure_router_isis


class TestConfigureRouterIsis(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-nyquist-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-nyquist-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_router_isis(self):
        result = configure_router_isis(self.device, 'test', '49.1290.0000.0011.00', 'Gi1/0/4', 'wide', 'Gi1/0/4', 'level-1')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_router_isis_1(self):
        result = configure_router_isis(self.device, 'test', None, 'Gi1/0/4', 'wide', 'Gi1/0/4', 'level-1')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_router_isis_2(self):
        result = configure_router_isis(self.device, 'test', None, None, 'wide', 'Gi1/0/4', 'level-1')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_router_isis_3(self):
        result = configure_router_isis(self.device, 'test', None, None, None, 'Gi1/0/4', 'level-1')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_router_isis_4(self):
        result = configure_router_isis(self.device, 'test', None, None, None, None, 'level-1')
        expected_output = None
        self.assertEqual(result, expected_output)
