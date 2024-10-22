import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_ppp_multilink


class TestUnconfigurePppMultilink(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          nanook_pkumarmu_rr:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: router
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['nanook_pkumarmu_rr']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_ppp_multilink(self):
        result = unconfigure_ppp_multilink(self.device, 'Dialer10')
        expected_output = None
        self.assertEqual(result, expected_output)
