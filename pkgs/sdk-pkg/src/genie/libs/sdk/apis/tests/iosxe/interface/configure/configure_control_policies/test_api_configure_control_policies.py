import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_control_policies


class TestConfigureControlPolicies(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          VCR:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9200
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['VCR']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_control_policies(self):
        result = configure_control_policies(self.device, 'DOT1X_POLICY_RADIUS', 'session-started', 'match-all', 10, None, 'do-until-failure', 10, 'authenticate', 'dot1x', None, None, 10, None, 2, 0)
        expected_output = None
        self.assertEqual(result, expected_output)
