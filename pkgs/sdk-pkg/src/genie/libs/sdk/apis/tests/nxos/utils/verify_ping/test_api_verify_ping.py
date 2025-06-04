import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.nxos.utils import verify_ping


class TestVerifyPing(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          R3_nx:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os nxos --mock_data_dir mock_data --state connect
                protocol: unknown
            os: nxos
            platform: n9kv
            type: NX-OSv 9000
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R3_nx']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_ping(self):
        result = verify_ping(self.device, '1.1.1.8')
        expected_output = True
        self.assertEqual(result, expected_output)
