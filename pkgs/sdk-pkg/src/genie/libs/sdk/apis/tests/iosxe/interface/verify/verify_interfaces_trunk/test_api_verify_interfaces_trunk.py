import os
from pyats.topology import loader
from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.verify import \
    verify_interfaces_trunk


class TestVerifyInterfacesTrunk(TestCase):
    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          DNAC-4:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir
                    {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: router
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['DNAC-4']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_interfaces_trunk(self):
        result = verify_interfaces_trunk(
            self.device,
            interface='GigabitEthernet0/1/0',
            mode='off',
            encapsulation='dot1q',
            status='no_trunking',
            native_vlan='1',
            vlans_allowed_on_trunk='100',
            vlans_allowed_active_in_mgmt_domain='100',
            vlans_in_stp_forwarding_not_pruned='100',
            max_time=20,
            interval=2
        )
        self.assertTrue(result)
    def test_verify_interfaces_trunk(self):
        result = verify_interfaces_trunk(
            self.device,
            interface='GigabitEthernet0/1/0',
            mode='off',
            encapsulation='dot1q',
            status='no_trunking',
            native_vlan='1',
            vlans_allowed_on_trunk='100',
            vlans_allowed_active_in_mgmt_domain='1000',
            vlans_in_stp_forwarding_not_pruned='100',
            max_time=1,
            interval=1
        )
        self.assertFalse(result)
    def test_verify_interfaces_trunk(self):
        result = verify_interfaces_trunk(
            self.device,
            interface='GigabitEthernet0/1/0',
            mode='off',
            encapsulation='dot1q',
            status='trunking',
            native_vlan='1',
            vlans_allowed_on_trunk='100',
            vlans_allowed_active_in_mgmt_domain='100',
            vlans_in_stp_forwarding_not_pruned='100',
            max_time=1,
            interval=1
        )
        self.assertFalse(result)
