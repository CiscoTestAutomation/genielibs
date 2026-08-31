import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import configure_scale_vrf_via_tftp


class TestConfigureScaleVrfViaTftp(unittest.TestCase):

    def test_configure_scale_vrf_via_tftp(self):
        device = Mock()
        server = {
            'myftpserver': {
                'address': None,
                'custom': {
                    'scale_config_path': '/auto/tftp-sjc-users4/siwwu/',
                },
                'dynamic': True,
                'path': '/',
                'protocol': 'ftp',
                'subnet': '171.70.0.0/16',
            }
        }

        result = configure_scale_vrf_via_tftp(
            device,
            server,
            1,
            1,
            5,
            False,
            False,
        )
        template = (
            '\n'
            '            vrf definition {vrf}\n'
            '                rd {vrf}:{vrf}\n'
            '                !\n'
            '                address-family ipv4\n'
            '                exit-address-family\n'
            '                !\n'
            '                address-family ipv6\n'
            '                exit-address-family\n'
            '            !\n'
            '            '
        )
        expected_config = ''.join(
            template.format(vrf=vrf) for vrf in range(1, 6)
        )

        self.assertEqual(result, expected_config)
        device.configure.assert_not_called()
