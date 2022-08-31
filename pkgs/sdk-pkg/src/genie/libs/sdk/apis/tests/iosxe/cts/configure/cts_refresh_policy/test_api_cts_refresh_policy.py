import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cts.configure import cts_refresh_policy


class TestCtsRefreshPolicy(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          CTS-AUTO-C9500:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['CTS-AUTO-C9500']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_cts_refresh_policy(self):
        result = cts_refresh_policy(self.device, False, None, False, None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_cts_refresh_policy_1(self):
        result = cts_refresh_policy(self.device, True, None, False, None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_cts_refresh_policy_2(self):
        result = cts_refresh_policy(self.device, True, 'peer1', False, None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_cts_refresh_policy_3(self):
        result = cts_refresh_policy(self.device, False, None, True, 'unknown')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_cts_refresh_policy_4(self):
        result = cts_refresh_policy(self.device, False, None, True, 'default')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_cts_refresh_policy_5(self):
        result = cts_refresh_policy(self.device, False, None, True, '10')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_cts_refresh_policy_6(self):
        result = cts_refresh_policy(self.device, False, None, True, 'x10y')
        expected_output = None
        self.assertEqual(result, expected_output)
