import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.qos.configure import config_qos_rewrite_dscp


class TestConfigQosRewriteDscp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Switch:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_config_qos_rewrite_dscp(self):
        result = config_qos_rewrite_dscp(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
