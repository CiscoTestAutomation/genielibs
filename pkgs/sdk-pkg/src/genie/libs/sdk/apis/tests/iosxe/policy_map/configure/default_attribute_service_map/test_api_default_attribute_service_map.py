from unittest import TestCase
from genie.libs.sdk.apis.iosxe.policy_map.configure import default_attribute_service_map
from unittest.mock import Mock


class TestDefaultAttributeServiceMap(TestCase):

    def test_default_attribute_service_map(self):
        self.device = Mock()
        result = default_attribute_service_map(self.device, 'BUILTIN_DEVICE_TO_TEMPLATE', 'subscriber')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['default parameter-map type subscriber attribute-to-service BUILTIN_DEVICE_TO_TEMPLATE'],)
        )
