import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.sisf.configure import remove_device_tracking_policy


class TestRemoveDeviceTrackingPolicy(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          sisf-c9500-21-8-26-2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: ios
            type: ios
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['sisf-c9500-21-8-26-2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_remove_device_tracking_policy(self):
        result = remove_device_tracking_policy(device=self.device, client_policy_name='pol1', server_policy_name='pol2')
        expected_output = None
        self.assertEqual(result, expected_output)
