import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.rep.configure import unconfigure_rep_segment


class TestUnconfigureRepSegment(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          IE-II-03-AgN1_2008_PB:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['IE-II-03-AgN1_2008_PB']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_rep_segment(self):
        result = unconfigure_rep_segment(self.device, ['Gi1/0/10', 'Gi1/0/11'], '1', '25', True, False)
        expected_output = None
        self.assertEqual(result, expected_output)
