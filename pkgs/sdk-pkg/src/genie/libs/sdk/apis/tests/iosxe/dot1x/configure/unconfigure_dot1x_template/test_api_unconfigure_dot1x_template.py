import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dot1x.configure import unconfigure_dot1x_template


class TestUnconfigureDot1xTemplate(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          LG-PK:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9200
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['LG-PK']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_dot1x_template(self):
        result = unconfigure_dot1x_template(self.device, 'Identity')
        expected_output = None
        self.assertEqual(result, expected_output)
