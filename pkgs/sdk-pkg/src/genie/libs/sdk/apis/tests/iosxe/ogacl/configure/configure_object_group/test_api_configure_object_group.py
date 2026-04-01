from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ogacl.configure import configure_object_group

class TestConfigureObjectGroup(TestCase):

    def test_configure_object_group(self):
        device = Mock()
        result = configure_object_group(
            device,
            'network',
            'HOSTA',
            'None',
            'None',
            'None',
            'host',
            '1.1.1.1',
            '1.1.1.1'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'object-group network HOSTA',
                'host 1.1.1.1'
            ],)
        )