import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_cts_manual


class TestUnconfigureCtsManual(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          9500H_SVL_W0607:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9500H_SVL_W0607']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_cts_manual(self):
        result = unconfigure_cts_manual(self.device, 'HundredGigE1/0/23')
        expected_output = None
        self.assertEqual(result, expected_output)
