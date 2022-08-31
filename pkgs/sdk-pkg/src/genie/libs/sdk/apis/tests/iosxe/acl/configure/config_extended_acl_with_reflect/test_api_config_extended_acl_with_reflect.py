import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.acl.configure import config_extended_acl_with_reflect


class TestConfigExtendedAclWithReflect(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Cat9600-SVL_CGW:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9600
            type: c9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Cat9600-SVL_CGW']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_config_extended_acl_with_reflect(self):
        result = config_extended_acl_with_reflect(self.device, 'test2', 'reflect', 'R10000', 'tcp', 'permit', '1.1.1.1', None, None, '2.2.2.2', None, None, '80', None, 'host', '50', '120', 'timeout', '2001', 'eq', None, None)
        expected_output = None
        self.assertEqual(result, expected_output)
