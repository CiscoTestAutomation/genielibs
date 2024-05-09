import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.bfd.configure import unconfigure_bfd_neighbor_on_interface


class TestUnconfigureBfdNeighborOnInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Intrepid-DUT-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            model: c9600
            type: c9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Intrepid-DUT-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_bfd_neighbor_on_interface(self):
        result = unconfigure_bfd_neighbor_on_interface(self.device, 'HundredGigE1/0/21', 'ipv6', '2013:1::20')
        expected_output = None
        self.assertEqual(result, expected_output)
