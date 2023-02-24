import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.rip.configure import unconfigure_rip


class TestUnconfigureRip(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          core:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['core']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_rip(self):
        result = unconfigure_rip(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
