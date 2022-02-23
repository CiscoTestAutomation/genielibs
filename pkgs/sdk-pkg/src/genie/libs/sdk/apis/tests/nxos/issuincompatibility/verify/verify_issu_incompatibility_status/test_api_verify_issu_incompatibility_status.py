import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.nxos.issuincompatibility.verify import verify_issu_incompatibility_status


class TestVerifyIssuIncompatibilityStatus(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          GX_uut2_26:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os nxos --mock_data_dir mock_data --state connect
                protocol: unknown
            os: nxos
            platform: Nexus 9000
            type: Nexus 9000
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['GX_uut2_26']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_issu_incompatibility_status(self):
        result = verify_issu_incompatibility_status(self.device, 'nxos64-cs.10.2.2.39.F.bin', 100, 5)
        expected_output = True
        self.assertEqual(result, expected_output)
