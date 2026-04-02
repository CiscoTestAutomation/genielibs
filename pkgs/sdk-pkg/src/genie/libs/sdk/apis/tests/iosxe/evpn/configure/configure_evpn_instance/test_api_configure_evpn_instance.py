import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.evpn.configure import configure_evpn_instance


def _flatten_cmds(cmds):
    """Recursively flatten a list of CLI commands that may include sub-lists."""
    flat = []
    for item in cmds:
        if isinstance(item, (list, tuple)):
            flat.extend(_flatten_cmds(item))
        else:
            flat.append(item)
    return flat


class TestConfigureEvpnInstance(TestCase):

    def test_configure_evpn_instance(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_evpn_instance(
            device,
            10,
            'vlan-based',
            'vxlan',
            'ingress'
        )
        self.assertEqual(result, None)

        device.configure.assert_called_once()

        sent_commands = device.configure.mock_calls[0].args[0]
        flat_commands = _flatten_cmds(sent_commands)

        self.assertIn('l2vpn evpn instance 10 vlan-based', flat_commands)
        self.assertIn('l2vpn evpn instance 10', flat_commands)
        self.assertIn('encapsulation vxlan', flat_commands)
        self.assertIn('replication ingress', flat_commands)


if __name__ == '__main__':
    unittest.main()