import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.configure import configure_system_jumbomtu


class TestConfigureSystemJumbomtu(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          CE1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat6k
            type: cat6500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['CE1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_system_jumbomtu(self):
        result = configure_system_jumbomtu(self.device, 1900)
        expected_output = None
        self.assertEqual(result, expected_output)
