import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.sisf.verify import verify_empty_device_tracking_policies


class TestVerifyEmptyDeviceTrackingPolicies(unittest.TestCase):

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

    def test_verify_empty_device_tracking_policies(self):
        result = verify_empty_device_tracking_policies(device=self.device, max_time=1, check_interval=1)
        expected_output = True
        self.assertEqual(result, expected_output)
