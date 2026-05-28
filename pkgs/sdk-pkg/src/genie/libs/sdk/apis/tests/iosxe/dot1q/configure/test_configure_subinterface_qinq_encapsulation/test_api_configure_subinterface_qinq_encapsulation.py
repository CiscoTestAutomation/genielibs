from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dot1q.configure import (
    configure_subinterface_qinq_encapsulation,
    unconfigure_subinterface_qinq_encapsulation,
)


class TestConfigureSubinterfaceQinqEncapsulation(TestCase):

    def test_configure_subinterface_qinq_encapsulation(self):
        self.device = Mock()
        interface = 'GigabitEthernet1/0'
        qinq = '100'

        configure_subinterface_qinq_encapsulation(
            self.device, interface=interface, qinq=qinq
        )

        expected_cmds = [
            f"interface {interface}.{qinq}",
            f"encapsulation dot1q {qinq} second {qinq}"
        ]
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (expected_cmds,)
        )

    def test_unconfigure_subinterface_qinq_encapsulation(self):
        self.device = Mock()
        interface = 'GigabitEthernet1/0'
        qinq = '100'

        unconfigure_subinterface_qinq_encapsulation(
            self.device, interface=interface, qinq=qinq
        )

        expected_cmds = [
            f"interface {interface}.{qinq}",
            f"no encapsulation dot1q {qinq} second {qinq}"
        ]
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (expected_cmds,)
        )
