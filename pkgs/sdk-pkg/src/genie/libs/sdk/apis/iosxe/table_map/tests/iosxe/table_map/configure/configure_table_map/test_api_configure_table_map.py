import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.table_map.configure import configure_table_map


class TestConfigureTableMap(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Startek:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Startek']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_table_map(self):
        result = configure_table_map(device=self.device, table_map_name='table_cos', from_val=['2', '5'], to_val=['5', '2'], default_val='copy')
        expected_output = None
        self.assertEqual(result, expected_output)
