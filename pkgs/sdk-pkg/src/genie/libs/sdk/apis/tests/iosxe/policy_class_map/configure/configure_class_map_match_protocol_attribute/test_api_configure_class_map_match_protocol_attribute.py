from unittest import TestCase
from genie.libs.sdk.apis.iosxe.policy_class_map.configure import configure_class_map_match_protocol_attribute
from unittest.mock import Mock


class TestConfigureClassMapMatchProtocolAttribute(TestCase):

    def test_configure_class_map_match_protocol_attribute(self):
        self.device = Mock()
        result = configure_class_map_match_protocol_attribute(self.device, 'match-all', 'c-attr', 'business-relevance', 'business-relevant')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['class-map match-all c-attr', 'match protocol attribute business-relevance business-relevant'],)
        )
