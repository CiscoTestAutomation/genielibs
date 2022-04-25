import unittest

from unittest import mock

from genie.libs.clean import BaseStage
from genie.libs.clean.utils import deprecate_stage


class TestDeprecateStage(unittest.TestCase):

    @mock.patch('genie.libs.clean.utils.time')
    @mock.patch('genie.libs.clean.utils.log')
    def test_deprecation(self, log, time):

        @deprecate_stage(deprecated_in=20.1)
        class Stage(BaseStage):
            """Some docstring"""
            exec_order = ['first_step']
            def first_step(self): pass

        stage = Stage()
        stage()

        # Ensure the method was prepended to the exec_order and it was
        # added to the class.
        self.assertEqual(['deprecate_msg', 'first_step'], stage.exec_order)
        self.assertTrue(hasattr(stage, 'deprecate_msg'))

        # Ensure the docstring is updated
        self.assertEqual("Clean stage 'Stage' deprecated in v20.1.", stage.__doc__)

        # Ensure proper logging was done when stage is ran
        log.warning.assert_has_calls([
            mock.call("Clean stage 'Stage' deprecated in v20.1."),
            mock.call("\nSleeping for 15 seconds."),
        ])

        # Ensure the hardcoded sleep exists
        time.sleep.assert_called_with(15)

    @mock.patch('genie.libs.clean.utils.time')
    @mock.patch('genie.libs.clean.utils.log')
    def test_deprecation_various_arguments(self, log, time):

        @deprecate_stage(deprecated_in=20.1, removed_in=22.4)
        class Stage(BaseStage):
            """Some docstring"""
            exec_order = ['first_step']
            def first_step(self): pass

        stage = Stage()
        stage()

        # Ensure the docstring is updated
        self.assertEqual("Clean stage 'Stage' deprecated in v20.1. Scheduled to "
                         "be removed in v22.4.",
                         stage.__doc__)

        # Ensure proper logging was done when stage is ran
        log.warning.assert_has_calls([
            mock.call("Clean stage 'Stage' deprecated in v20.1. Scheduled to be "
                      "removed in v22.4."),
            mock.call("\nSleeping for 15 seconds."),
        ])

        @deprecate_stage(deprecated_in=20.1, removed_in=22.4, details="Some extra details.")
        class Stage(BaseStage):
            """Some docstring"""
            exec_order = ['first_step']
            def first_step(self): pass

        stage = Stage()
        stage()

        # Ensure the docstring is updated
        self.assertEqual("Clean stage 'Stage' deprecated in v20.1. Scheduled to "
                         "be removed in v22.4.\nSome extra details.",
                         stage.__doc__)

        # Ensure proper logging was done when stage is ran
        log.warning.assert_has_calls([
            mock.call("Clean stage 'Stage' deprecated in v20.1. Scheduled to be "
                      "removed in v22.4.\nSome extra details."),
            mock.call("\nSleeping for 15 seconds."),
        ])

        @deprecate_stage(deprecated_in=20.1, details="Some extra details.")
        class Stage(BaseStage):
            """Some docstring"""
            exec_order = ['first_step']
            def first_step(self): pass

        stage = Stage()
        stage()

        # Ensure the docstring is updated
        self.assertEqual("Clean stage 'Stage' deprecated in v20.1.\nSome extra "
                         "details.",
                         stage.__doc__)

        # Ensure proper logging was done when stage is ran
        log.warning.assert_has_calls([
            mock.call("Clean stage 'Stage' deprecated in v20.1.\nSome extra "
                      "details."),
            mock.call("\nSleeping for 15 seconds."),
        ])


