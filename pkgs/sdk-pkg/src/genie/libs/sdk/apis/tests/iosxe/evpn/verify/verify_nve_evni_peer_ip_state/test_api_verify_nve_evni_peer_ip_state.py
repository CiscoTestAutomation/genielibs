import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.evpn.verify import verify_nve_evni_peer_ip_state


class TestVerifyNveEvniPeerIpState(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          CL1-c9300:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['CL1-c9300']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_nve_evni_peer_ip_state(self):
        result = verify_nve_evni_peer_ip_state(self.device, '20.0.101.2', '2000101', '2000101', 'UP', 60, 10)
        expected_output = True
        self.assertEqual(result, expected_output)
