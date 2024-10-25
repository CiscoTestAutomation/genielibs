import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_service_policy_type_queueing_on_interface


class TestConfigureServicePolicyTypeQueueingOnInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Raitt:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Raitt']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_service_policy_type_queueing_on_interface(self):
        result = configure_service_policy_type_queueing_on_interface(self.device, 'GigabitEthernet1/0/10', 'output', '3p1q')
        expected_output = None
        self.assertEqual(result, expected_output)
