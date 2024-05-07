
import unittest
import functools
import importlib

from unittest import mock
from functools import partial

from genie.libs.clean.clean import StageSection, BaseStage, CleanTestcase, REUSE_LIMIT_MSG
from genie.libs.clean.stages.image_handler import BaseImageHandler
from genie.conf.base import Device
from genie.abstract.package import AbstractTree

from pyats.log.utils import banner
from pyats import results


class TestStageSection(unittest.TestCase):

    def test_representation(self):
        stage_name = 'banana'

        section = StageSection(function=self, uid=stage_name)

        self.assertEqual(stage_name, section.uid)
        self.assertEqual(f'stage {stage_name}', str(section))


class TestBaseStage(unittest.TestCase):

    class SomeStage(BaseStage):
        def func2(self): pass

        def func1(self): pass

    stage = SomeStage()

    def test_exec_order_attribute_exists(self):
        self.assertTrue(hasattr(self.stage, 'exec_order'))

    def test_exec_order(self):
        self.stage.exec_order = ['func1', 'func2']

        stage_iter = iter(self.stage)

        self.assertEqual(self.stage.func1, next(stage_iter))
        self.assertEqual(self.stage.func2, next(stage_iter))

    def test_exec_order_not_defined(self):
        self.stage.exec_order = []

        expected_msg = r"^The class variable 'exec_order' from .*SomeStage.* is " \
                       r"empty or not defined.$"

        with self.assertRaisesRegex(AttributeError, expected_msg):
            iter(self.stage)

    def test_exec_order_contains_undefined_method(self):
        self.stage.exec_order = ['func1', 'this doesnt exist', 'func2']

        expected_msg = r"^The class variable 'exec_order' from .*SomeStage.* " \
                       r"contains undefined methods: .*this doesnt exist.*$"

        with self.assertRaisesRegex(AttributeError, expected_msg):
            iter(self.stage)

    @mock.patch.multiple(
        stage, func1=mock.DEFAULT, func2=mock.DEFAULT,
        apply_parameters=lambda func, args: partial(func, **args))
    def test_running_stage_methods_called(self, func1, func2):

        self.stage.exec_order = ['func1', 'func2']

        # run the stage
        self.stage()

        # make sure the methods defined in exec_order were called
        func1.assert_called()
        func2.assert_called()

        self.stage(test=123)
        func1.assert_called_with(test=123)


source_json = {
        "SomeStage": {
            "folders": {
                "iosxe": {
                    "package": "genie.libs.clean",
                    "module_name": "stages.stages",
                    "uid": "SomeStage",
                    "tokens": {
                        "os": "iosxe"
                    }
                }
            }
        },
        "SomeOtherStage": {
            "folders": {
                "iosxe": {
                    "package": "genie.libs.clean",
                    "module_name": "stages.stages",
                    "uid": "SomeOtherStage",
                    "tokens": {
                        "os": "iosxe"
                    }
                }
            }
        },
        "token_order": ["os"],
        "tokens": {
            "os": ["iosxe"]
        }
    }

def clean_json():
    # mock load_clean_json function to return a new abstract matrix each test
    return AbstractTree.from_json(source_json)

class TestCleanTestcase(unittest.TestCase):
    class SomeStage(BaseStage):
        schema = {}

    class SomeOtherStage(BaseStage):
        schema = {}

    def setUp(self):
        self.device = Device(
            name='TestDevice', os='iosxe',
            custom={'abstraction': {'order': ['os']}})

        self.global_stage_reuse_limit = 3

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_discover(self):

        self.device.clean = {
            'SomeStage': {},
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        clean_testcase.discover()

        self.assertEqual(self.SomeStage, clean_testcase.stages['SomeStage']['func'])

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_discover_with_image_handler(self):

        self.device.clean = {
            'images': ['image.bin'],
            'SomeStage': {},
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        self.assertTrue(isinstance(clean_testcase.image_handler, BaseImageHandler))

        clean_testcase.image_handler.update_section = mock.Mock()

        clean_testcase.discover()

        clean_testcase.image_handler.update_section.assert_called_with('SomeStage')

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_discover_custom_stage_source(self):
        self.device.clean = {
            'SomeStage': {
                'source': {
                    'pkg': 'genie.libs.clean',
                    'class': 'stages.stages.SomeStage'
                }
            },
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        clean_testcase.discover()

        self.assertEqual(self.SomeStage, clean_testcase.stages['SomeStage']['func'])

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_discover_invalid_stage_schema(self):
        self.device.clean = {
            'SomeStage': {'Not in schema': None},
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        expected_msg = r"Not in schema:       <<<"

        with self.assertRaisesRegex(ValueError, expected_msg):
            clean_testcase.discover()

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    def test_discover_stage_doesnt_exist_in_json(self):

        self.device.clean = {
            'ThisStageDoesntExist': {},
            'order': ['ThisStageDoesntExist']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        expected_msg = r"The clean stage 'ThisStageDoesntExist' does not exist " \
                       r"in the json file"

        with self.assertRaisesRegex(Exception, expected_msg):
            clean_testcase.discover()

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    def test_discover_stage_doesnt_exist(self):

        self.device.clean = {
            'SomeStage': {},
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        expected_msg = r"The clean stage 'SomeStage' does not exist under the " \
                       r"following abstraction tokens: \{.*\}"

        with self.assertRaisesRegex(Exception, expected_msg):
            clean_testcase.discover()

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_discover_device_recovery_not_in_yaml(self):
        self.device.clean = {
            'SomeStage': {},
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        self.assertEqual(None, clean_testcase.device_recovery_processor)

        clean_testcase.discover()

        self.assertEqual(None, clean_testcase.device_recovery_processor)

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_discover_device_recovery_in_yaml(self):

        self.device.clean = {
            'device_recovery': {
                'golden_image': [
                    'golden.bin'
                ]
            },
            'order': []
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        self.assertEqual(None, clean_testcase.device_recovery_processor)

        clean_testcase.discover()

        self.assertIsInstance(clean_testcase.device_recovery_processor,
                              functools.partial)

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_iter(self):
        self.device.clean = {
            'SomeStage': {},
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        iterator = iter(clean_testcase)

        self.assertEqual('stage SomeStage', str(next(iterator)))

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_iter_unique_stage_uids(self):
        self.device.clean = {
            'SomeStage': {},
            'SomeStage__2': {},
            'order': ['SomeStage', 'SomeStage__2', 'SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        iterator = iter(clean_testcase)

        self.assertEqual('stage SomeStage', str(next(iterator)))
        self.assertEqual('stage SomeStage(2)', str(next(iterator)))
        self.assertEqual('stage SomeStage(3)', str(next(iterator)))

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_iter_device_recovery_processor(self):

        self.device.clean = {
            'SomeStage': {},
            'device_recovery': {
                'golden_image': [
                    'golden.bin'
                ]
            },
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        iterator = iter(clean_testcase)
        stage = next(iterator)

        self.assertEqual(clean_testcase.device_recovery_processor,
                         stage.function.__processors__.post[0])


    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_iter_with_image_handler(self):
        self.device.clean = {
            'images': ['image.bin'],
            'SomeStage': {},
            'SomeStage__2': {},
            'order': ['SomeStage', 'SomeStage__2']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        clean_testcase.image_handler.update_section = mock.Mock()
        iterator = iter(clean_testcase)

        self.assertEqual('stage SomeStage', str(next(iterator)))
        clean_testcase.image_handler.update_section.assert_called_with('SomeStage', update_history=True)

        self.assertEqual('stage SomeStage(2)', str(next(iterator)))
        clean_testcase.image_handler.update_section.assert_called_with('SomeStage__2', update_history=True)

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_iter_stage_in_order_but_not_declared(self):
        self.device.clean = {
            'order': ['SomeStage', 'SomeStage__2']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        iterator = iter(clean_testcase)

        expected_msg = r"Stage 'SomeStage' has no configuration in clean.yaml " \
                       r"for device TestDevice"

        with self.assertRaisesRegex(Exception, expected_msg):
            next(iterator)

    @mock.patch('genie.libs.clean.clean.log')
    @mock.patch('genie.libs.clean.clean.aetest')
    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_iter_infinite_loop_scenario(self, mocked_aetest, mocked_log):
        self.device.clean = {
            'SomeStage': {
                'change_order_if_pass': [
                    'SomeStage'
                ]
            },
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        mocked_aetest.executer.goto = None

        iterator = iter(clean_testcase)

        for _ in range(self.global_stage_reuse_limit + 1):
            next(iterator)

        mocked_log.error.assert_called_with(
            banner(REUSE_LIMIT_MSG.format(
                stage='SomeStage', limit=self.global_stage_reuse_limit))
        )

        self.assertEqual(results.Blocked, mocked_aetest.executer.goto_result)
        self.assertEqual([['Infinite loop scenario', str]], mocked_aetest.executer.goto)

    @mock.patch('genie.libs.clean.clean.log')
    @mock.patch('genie.libs.clean.clean.aetest')
    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_iter_failed_stage(self, mocked_aetest, mocked_log):
        self.device.clean = {
            'SomeStage': {
                'change_order_if_pass': [
                    'SomeStage'
                ]
            },
            'order': ['SomeStage', 'SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        mocked_aetest.executer.goto = None

        iterator = iter(clean_testcase)

        stage = next(iterator)
        stage.result = results.Failed

        next(iterator)

        mocked_log.error.assert_called_with(
            banner("*** Terminating Genie Clean ***")
        )

        self.assertEqual(results.Blocked, mocked_aetest.executer.goto_result)
        self.assertEqual([['SomeStage has failed', str]], mocked_aetest.executer.goto)

    @mock.patch('genie.libs.clean.clean.log')
    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    @mock.patch('genie.libs.clean.stages.stages.SomeOtherStage', SomeOtherStage, create=True)
    def test_iter_change_order_if_pass(self, mocked_log):
        self.device.clean = {
            'SomeOtherStage': {},
            'SomeStage': {
                'change_order_if_pass': [
                    'SomeOtherStage'
                ]
            },
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        iterator = iter(clean_testcase)

        stage = next(iterator)
        stage.result = results.Passed

        stage = next(iterator)

        mocked_log.warning.assert_called_with(
            "Due to 'change_order_if_pass' the order of clean is changed "
            "to:\n- SomeOtherStage"
        )

        self.assertEqual('SomeOtherStage', stage.uid)

    @mock.patch('genie.libs.clean.clean.log')
    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    @mock.patch('genie.libs.clean.stages.stages.SomeOtherStage', SomeOtherStage, create=True)
    def test_iter_change_order_if_fail(self, mocked_log):
        self.device.clean = {
            'SomeOtherStage': {},
            'SomeStage': {
                'change_order_if_fail': [
                    'SomeOtherStage'
                ]
            },
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit,
            parent=mock.Mock(__result__=None))

        iterator = iter(clean_testcase)

        stage = next(iterator)
        stage.result = results.Failed

        stage = next(iterator)

        mocked_log.warning.assert_called_with(
            "Due to 'change_order_if_fail' the order of clean is changed "
            "to:\n- SomeOtherStage"
        )

        self.assertEqual('SomeOtherStage', stage.uid)

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(return_value=clean_json()))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_discover_image_handler_image_override_false(self):
        self.device.clean = {
            'images': ['/my/image.bin'],
            'SomeStage': {},
            'order': ['SomeStage'],
            'image_management': {
                'override_stage_images': False
            },
        }
        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        clean_testcase.discover()

        self.assertEqual(clean_testcase.image_handler.override_stage_images, False)

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(return_value=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_discover_image_handler_image_override_true(self):
        self.device.clean = {
            'images': ['/my/image.bin'],
            'SomeStage': {
                'source': {
                    'pkg': 'genie.libs.clean',
                    'class': 'stages.stages.SomeStage'
                }
            },
            'order': ['SomeStage'],
            'image_management': {
                'override_stage_images': True
            },
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        clean_testcase.discover()

        self.assertEqual(clean_testcase.image_handler.override_stage_images, True)

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(return_value=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_discover_image_handler_image_override_default(self):
        self.device.clean = {
            'images': ['/my/image.bin'],
            'SomeStage': {
                'source': {
                    'pkg': 'genie.libs.clean',
                    'class': 'stages.stages.SomeStage'
                }
            },
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        clean_testcase.discover()

        self.assertEqual(clean_testcase.image_handler.override_stage_images, True)
