import logging
from types import SimpleNamespace
import unittest

from unittest.mock import Mock

from genie.abstract import Lookup
import genie.libs.clean as clean
from genie.libs.clean.stages.iosxe.cat9k.c9800.c9800_cl.stages import (
    ApplySelfSignedCert,
)

from pyats.aetest.signals import AEtestSkippedSignal
from pyats.aetest.steps import Steps
from pyats.topology.credentials import Credentials


# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class TestApplySelfSignedCert(unittest.TestCase):

    def setUp(self):
        self.cls = ApplySelfSignedCert()
        self.device = Mock(name='device')
        self.device.name = 'C9800-CL'
        self.device.credentials = {}
        self.device.testbed = None

    def test_clean_yaml_password_takes_precedence(self):
        self.device.credentials = {
            'certificate': {'password': 'device-password'},
        }

        self.cls.configure_ssc_trustpoint(
            device=self.device,
            steps=Steps(),
            password='clean-password',
        )

        call_kwargs = (
            self.device.api.execute_self_signed_certificate_command.call_args.kwargs
        )
        self.assertEqual('clean-password', call_kwargs['password'])

    def test_uses_clean_yaml_password(self):
        self.cls.configure_ssc_trustpoint(
            device=self.device,
            steps=Steps(),
            password='clean-password',
        )

        call_kwargs = (
            self.device.api.execute_self_signed_certificate_command.call_args.kwargs
        )
        self.assertEqual('clean-password', call_kwargs['password'])

    def test_falls_back_to_device_certificate_credentials(self):
        self.device.credentials = Credentials({
            'certificate': {'password': 'device-password'},
        })

        self.cls.configure_ssc_trustpoint(
            device=self.device,
            steps=Steps(),
        )

        call_kwargs = (
            self.device.api.execute_self_signed_certificate_command.call_args.kwargs
        )
        self.assertEqual('device-password', call_kwargs['password'])

    def test_skips_stage_when_password_is_unavailable(self):
        with self.assertRaisesRegex(
                AEtestSkippedSignal,
                'Password not provided in testbed certificate credentials or the clean YAML. Skipping self-signed certificate stage.'):
            self.cls.configure_ssc_trustpoint(
                device=self.device,
                steps=Steps(),
            )

        self.device.api.enable_http_server.assert_not_called()
        self.device.api.execute_self_signed_certificate_command.assert_not_called()

    def test_does_not_use_default_credentials_for_certificate(self):
        self.device.credentials = Credentials({
            'default': {'username': 'admin', 'password': 'login-password'},
        })

        with self.assertRaisesRegex(
                AEtestSkippedSignal,
                'Password not provided in testbed certificate credentials or the clean YAML. Skipping self-signed certificate stage.'):
            self.cls.configure_ssc_trustpoint(
                device=self.device,
                steps=Steps(),
            )

        self.device.api.enable_http_server.assert_not_called()
        self.device.api.execute_self_signed_certificate_command.assert_not_called()


class TestC9800CLCleanAbstraction(unittest.TestCase):

    def test_selects_submodel_stage(self):
        device = SimpleNamespace(
            os='iosxe',
            platform='cat9k',
            model='c9800',
            submodel='c9800_cl',
        )
        lookup = Lookup.from_device(device, packages={'clean': clean})

        stage = lookup.clean.stages.stages.ApplySelfSignedCert

        self.assertEqual(
            stage.__module__,
            'genie.libs.clean.stages.iosxe.cat9k.c9800.c9800_cl.stages',
        )


if __name__ == '__main__':
    unittest.main()
