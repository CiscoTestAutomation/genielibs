import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.acl.configure import config_extended_acl


class TestConfigExtendedAcl(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          LG-PK:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['LG-PK']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_config_extended_acl(self):
        result = config_extended_acl(self.device, 'IN29', 'permit', 'ip', None, None, None, None, None, None, None, 0, None, 10)
        expected_output = None
        self.assertEqual(result, expected_output)
