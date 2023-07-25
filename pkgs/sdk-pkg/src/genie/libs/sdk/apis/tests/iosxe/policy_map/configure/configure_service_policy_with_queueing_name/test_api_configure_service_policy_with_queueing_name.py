import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.policy_map.configure import configure_service_policy_with_queueing_name


class TestConfigureServicePolicyWithQueueingName(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Startrek-SVL:
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
        self.device = self.testbed.devices['Startrek-SVL']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_service_policy_with_queueing_name(self):
        result = configure_service_policy_with_queueing_name(self.device, 'FourHundredGigE1/0/17', 'queue', 'llq')
        expected_output = 'interface FourHundredGigE1/0/17\r\ninterface FourHundredGigE1/0/17\r\nservice-policy type queue output llq\r\nservice-policy type queue output llq\r\n'
        self.assertEqual(result, expected_output)
