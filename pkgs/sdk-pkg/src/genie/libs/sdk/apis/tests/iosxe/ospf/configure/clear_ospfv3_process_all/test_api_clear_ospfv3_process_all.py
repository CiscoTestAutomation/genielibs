from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import clear_ospfv3_process_all


class TestClearOspfv3ProcessAll(TestCase):

    def test_clear_ospfv3_process_all(self):
        device = Mock()
        result = clear_ospfv3_process_all(device)
        self.assertEqual(result, None)
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('clear ospfv3 process',)
        )