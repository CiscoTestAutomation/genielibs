import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.nve.verify import verify_nve_vni_members_cfg

class TestVerifyNveVniMembersCfg(unittest.TestCase):

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

    def test_verify_nve_vni_members_cfg_l2vni_static_true(self):
        exp_vni_member_cfg = {'10000': {'mcast_group': '225.1.1.1'}}
        result = verify_nve_vni_members_cfg(self.device, "1",
                                            exp_vni_member_cfg)
        expected_output = True
        self.assertEqual(result, expected_output)

    def test_verify_nve_vni_members_cfg_l2vni_ir(self):
        exp_vni_member_cfg = {'20000': {'ingress_replication': {'enabled': True}}}
        result = verify_nve_vni_members_cfg(self.device, "1",
                                            exp_vni_member_cfg)
        expected_output = True
        self.assertEqual(result, expected_output)

    def test_verify_nve_vni_members_cfg_l2vni_static_wrong_addr(self):
        exp_vni_member_cfg = {'10000': {'mcast_group': '225.1.1.2'}}
        result = verify_nve_vni_members_cfg(self.device, "1",
                                            exp_vni_member_cfg)
        expected_output = False
        self.assertEqual(result, expected_output)

    def test_verify_nve_vni_members_cfg_l2vni_wrong_rep_type(self):
        exp_vni_member_cfg = {'10000': {'ingress_replication': {'enabled': True}}}
        result = verify_nve_vni_members_cfg(self.device, "1",
                                            exp_vni_member_cfg)
        expected_output = False
        self.assertEqual(result, expected_output)

    def test_verify_nve_vni_members_cfg_l3vni(self):
        exp_vni_member_cfg = {'50000': {'vrf': 'red'}}
        result = verify_nve_vni_members_cfg(self.device, "1",
                                            exp_vni_member_cfg)
        expected_output = True
        self.assertEqual(result, expected_output)

    def test_verify_nve_vni_members_cfg_l3vni_wrong_vrf(self):
        exp_vni_member_cfg = {'50000': {'vrf': 'green'}}
        result = verify_nve_vni_members_cfg(self.device, "1",
                                            exp_vni_member_cfg)
        expected_output = False
        self.assertEqual(result, expected_output)
