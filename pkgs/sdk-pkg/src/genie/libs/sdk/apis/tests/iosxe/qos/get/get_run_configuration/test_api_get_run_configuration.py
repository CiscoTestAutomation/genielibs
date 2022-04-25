import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.qos.get import get_run_configuration


class TestGetRunConfiguration(unittest.TestCase):

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

    def test_get_run_configuration(self):
        result = get_run_configuration(self.device, 'qos')
        expected_output = None
        self.assertEqual(result, expected_output)
