import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.eigrp.configure import unconfigure_eigrp_named_router


class TestUnconfigureEigrpNamedRouter(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          kparames_csr10:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat8k
            model: c8000v
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['kparames_csr10']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_eigrp_named_router(self):
        result = unconfigure_eigrp_named_router(self.device, 'named-eigrp')
        expected_output = None
        self.assertEqual(result, expected_output)
