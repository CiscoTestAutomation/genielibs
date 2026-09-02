from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sustainability.interface.configure import (
    configure_smartpower_interface_domain_default,
)


class TestConfigureSmartpowerInterfaceDomainDefault(TestCase):

    def test_configure_smartpower_interface_domain_default(self):
        device = Mock()

        result = configure_smartpower_interface_domain_default(
            device,
            'Gi1/0/13',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            ['interface Gi1/0/13', 'default smartpower domain']
        )
