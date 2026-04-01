from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospf_redistributed_static


class TestConfigureOspfRedistributedStatic(TestCase):

    def test_configure_ospf_redistributed_static(self):
        device = Mock()
        result = configure_ospf_redistributed_static(
            device,
            1
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['router ospf 1', 'redistribute static'],)
        )