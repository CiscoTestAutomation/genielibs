import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.isis.configure import configure_isis_metric_style


class TestConfigureIsisMetricStyle(unittest.TestCase):

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

    def test_configure_isis_metric_style(self):
        result = configure_isis_metric_style(self.device, 'wide', 'level-1', 'Gi1/0/6')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_isis_metric_style_1(self):
        result = configure_isis_metric_style(self.device, 'transition', None, None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_isis_metric_style_2(self):
        result = configure_isis_metric_style(self.device, 'wide', None, 'Gi1/0/6')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_isis_metric_style_3(self):
        result = configure_isis_metric_style(self.device, 'wide', 'level-1', None)
        expected_output = None
        self.assertEqual(result, expected_output)
