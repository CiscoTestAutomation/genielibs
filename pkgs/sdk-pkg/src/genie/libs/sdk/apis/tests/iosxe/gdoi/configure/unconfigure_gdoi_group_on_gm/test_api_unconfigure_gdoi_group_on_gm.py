import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.gdoi.configure import unconfigure_gdoi_group_on_gm


class TestUnconfigureGdoiGroupOnGm(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Router:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Router']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_gdoi_group_on_gm(self):
        result = unconfigure_gdoi_group_on_gm(self.device, 'gp_2', True)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_gdoi_group_on_gm_1(self):
        result = unconfigure_gdoi_group_on_gm(self.device, 'gp_1', False)
        expected_output = None
        self.assertEqual(result, expected_output)
