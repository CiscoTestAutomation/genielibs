import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ospf.configure import unconfigure_ipv6_ospf_bfd


class TestUnconfigureIpv6OspfBfd(unittest.TestCase):

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
            type: C9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Intrepid-DUT-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_ipv6_ospf_bfd(self):
        result = unconfigure_ipv6_ospf_bfd(device=self.device, interface='HundredGigE1/0/21')
        expected_output = None
        self.assertEqual(result, expected_output)
