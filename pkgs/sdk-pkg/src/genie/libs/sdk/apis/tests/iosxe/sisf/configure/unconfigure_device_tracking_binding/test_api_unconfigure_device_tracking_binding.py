import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.sisf.configure import unconfigure_device_tracking_binding


class TestUnconfigureDeviceTrackingBinding(unittest.TestCase):

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

    def test_unconfigure_device_tracking_binding(self):
        result = unconfigure_device_tracking_binding(device=self.device, vlan=10, address='10.10.10.10', interface='te1/0/1', mac='dead.beef.1000', tracking='default')
        expected_output = None
        self.assertEqual(result, expected_output)
