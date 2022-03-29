import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.utils import fp_switchover


class TestFpSwitchover(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          PE3:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: router
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['PE3']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_fp_switchover(self):
        result = fp_switchover(self.device, 420)
        expected_output = True
        self.assertEqual(result, expected_output)
