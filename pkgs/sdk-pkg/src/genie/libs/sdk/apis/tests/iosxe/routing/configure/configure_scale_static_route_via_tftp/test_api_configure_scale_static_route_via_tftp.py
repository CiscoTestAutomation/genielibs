import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.configure import configure_scale_static_route_via_tftp


class TestConfigureScaleStaticRouteViaTftp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Organ:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: router
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Organ']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_scale_static_route_via_tftp(self):
        result = configure_scale_static_route_via_tftp(self.device, {'myftpserver': {'custom': {'scale_config_path': '/auto/tftp-sjc-users4/siwwu/'},
                 'dynamic': True,
                 'protocol': 'ftp'}}, 3, '201.0.0.1', '0.0.1.0', '255.255.255.255', '12.0.0.2', '0.0.1.0', None, False, False)
        expected_output = ('\n'
 '         ip route 201.0.0.1 255.255.255.255 12.0.0.2 \n'
 '        \n'
 '         ip route 201.0.1.1 255.255.255.255 12.0.1.2 \n'
 '        \n'
 '         ip route 201.0.2.1 255.255.255.255 12.0.2.2 \n'
 '        ')
        self.assertEqual(result, expected_output)
