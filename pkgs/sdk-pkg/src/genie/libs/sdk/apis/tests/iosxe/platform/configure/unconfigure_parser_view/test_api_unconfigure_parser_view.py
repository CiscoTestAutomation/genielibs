import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_parser_view


class TestUnconfigureParserView(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          c8kv-dev-7:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: C8000v
            type: C8000v
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['c8kv-dev-7']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_parser_view(self):
        result = unconfigure_parser_view(self.device, 'pv1')
        expected_output = None
        self.assertEqual(result, expected_output)
