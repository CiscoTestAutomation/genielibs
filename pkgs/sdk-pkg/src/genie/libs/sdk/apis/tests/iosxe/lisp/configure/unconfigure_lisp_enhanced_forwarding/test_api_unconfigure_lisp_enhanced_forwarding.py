from unittest import TestCase
from genie.libs.sdk.apis.iosxe.lisp.configure import unconfigure_lisp_enhanced_forwarding
from unittest.mock import Mock

class TestUnconfigureLispEnhancedForwarding(TestCase):

    def test_unconfigure_lisp_enhanced_forwarding(self):
        self.device = Mock()
        unconfigure_lisp_enhanced_forwarding(self.device, '1', '2')
        self.device.configure.assert_called_with(['router lisp', 'instance-id 1', 'service ethernet', 'eid-table vlan 2', 'no enhanced-forwarding'])
