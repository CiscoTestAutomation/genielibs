from  unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.clear import clear_ip_reflexive_list


class TestClearIpReflexiveList(TestCase):

    def test_clear_ip_reflexive_list(self):
        device = Mock()

        result = clear_ip_reflexive_list(device, "REF1")
        self.assertIsNone(result)

        self.assertEqual(
            device.execute.mock_calls[0].args,
            ("clear ip reflexive-list REF1",)
        )

    def test_clear_ip_reflexive_list_1(self):
        device = Mock()

        result = clear_ip_reflexive_list(device, "*")
        self.assertIsNone(result)

        self.assertEqual(
            device.execute.mock_calls[0].args,
            ("clear ip reflexive-list *",)
        )