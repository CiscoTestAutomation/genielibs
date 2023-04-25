import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.nve.get import get_nve_vnis

class TestGetNveVnis(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          PE1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['PE1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_nve_vnis(self):
        result = get_nve_vnis(self.device)
        expected_output = {'nve1':
                                {'50000': {'interface': 'nve1', 'vni': '50000',\
                                           'mcast': 'FF0E::501', 'vni_state': 'Up',\
                                           'mode': 'L3CP', 'vlan': '500', 'cfg': 'CLI',\
                                           'vrf': 'red'},
                                 '20000': {'interface': 'nve1', 'vni': '20000',\
                                           'mcast': 'FF0E::102', 'vni_state': 'Up',\
                                           'mode': 'L2CP', 'vlan': '200', 'cfg': 'CLI',\
                                           'vrf': 'red'}
                                 }
                           }
        self.assertEqual(result, expected_output)
