import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.aaa.configure import enable_radius_automate_tester_probe_on


class TestEnableRadiusAutomateTesterProbeOn(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          9500H_SVL_SSN_V07:
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
        self.device = self.testbed.devices['9500H_SVL_SSN_V07']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_enable_radius_automate_tester_probe_on(self):
        result = enable_radius_automate_tester_probe_on(self.device, 'serv1', 'user1', 'red')
        expected_output = None
        self.assertEqual(result, expected_output)
