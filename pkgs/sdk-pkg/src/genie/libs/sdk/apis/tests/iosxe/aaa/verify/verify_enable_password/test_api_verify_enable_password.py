import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.aaa.verify import verify_enable_password


class TestVerifyEnablePassword(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          9300_stack:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: ng9k_stack
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9300_stack']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_enable_password(self):
        result = verify_enable_password(self.device, 'dnac1', 15)
        expected_output = True
        self.assertEqual(result, expected_output)
