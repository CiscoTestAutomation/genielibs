
# Python
import logging
from inspect import unwrap
from functools import partial
from collections import OrderedDict

# pyATS
from pyats import aetest
from pyats import results
from pyats.results import Passed, Passx, Failed, Errored
from pyats.aetest import Testcase
from pyats.log.utils import banner
from pyats.aetest.base import Source
from pyats.aetest import processors
from pyats.kleenex.bases import BaseCleaner
from pyats.aetest.parameters import ParameterDict

# Genie
from genie.testbed import load
from genie.harness.utils import load_class
from genie.libs.clean.utils import pretty_schema_exception, \
    get_clean_function, load_clean_json, get_image_handler
from genie.metaparser.util.schemaengine import Schema
from genie.libs.clean.recovery import recovery_processor, block_section

# Logger
log = logging.getLogger(__name__)

NOT_A_STAGE = ['device_recovery', 'images', 'order']

GLOBAL_STAGE_REUSE_LIMIT = 3

REUSE_LIMIT_MSG = """\n
*** Terminating Genie Clean ***
\u0020
To protect against an infinite loop scenario.
\u0020
stage_reuse_limit = {limit}
{stage} ran {limit} times
"""


class CleanTestcase(Testcase):

    def __init__(self, device, global_stage_reuse_limit, *args, **kwargs):
        self.device = device
        self.global_stage_reuse_limit = global_stage_reuse_limit
        self.stages = {}
        self.device_recovery_processor = None
        self.image_handler = get_image_handler(device)
        self.history = OrderedDict()
        super().__init__(*args, **kwargs)

    def __iter__(self):
        '''Built-in function __iter__

        Generator function, yielding each testable item within this container
        in the order of appearance inside the test cases. This is the main
        mechanism that allows looping through CleanTestcase Section's child
        items.
        '''
        self.discover()
        used_uids = {}

        order = self.device.clean['order']
        while True:
            for stage in order:
                if stage not in self.stages:
                    self.failed("Stage '{}' has no configuration"
                                " in clean.yaml for device {}"
                                .format(stage, self.device.name))

                # Check if stage has hit execution limits to protect
                # against an infinite loop scenario
                count = len(used_uids.get(stage, []))
                limit = self.stages[stage]['stage_reuse_limit'] or \
                        self.global_stage_reuse_limit

                if count >= limit:
                    # Dont log this for every remaining stage
                    if not aetest.executer.goto:
                        log.error(banner(REUSE_LIMIT_MSG.format(
                            stage=stage, limit=limit)))

                    aetest.executer.goto_result = results.Blocked
                    aetest.executer.goto = [['Infinite loop scenario', str]]

                # If image handler has a method to update this section - execute it
                if self.image_handler:
                    self.image_handler.update_section(stage)

                func = self.stages[stage]['func']

                # Get a unique ID for the section
                if stage not in used_uids:
                    used_uids[stage] = []
                    func.uid = stage
                else:
                    func.uid = "{}({})".format(stage, len(used_uids[stage])+1)

                used_uids[stage].append(func.uid)

                # Setup stage function
                func.source = Source(self, objcls=func.__class__)
                func.parameters = ParameterDict()
                func.parameters['device'] = self.device

                args = self.stages[stage]['args']
                for parameter, value in args.items():
                    func.parameters[parameter] = value

                # Bind function
                section = func.__get__(self, func.__testcls__)
                self.history[section.uid] = section

                if self.device_recovery_processor:
                    processors.affix(
                        section,
                        pre=[block_section],
                        post=[self.device_recovery_processor],
                        exception=[])

                new_section = section.__testcls__(section, parent=self)
                yield new_section

                pass_order = self.stages[stage]['change_order_if_pass']
                if pass_order and new_section.result in [Passed, Passx]:
                    msg = "Due to 'change_order_if_pass' the order of clean " \
                          "is changed to:\n- " + "\n- ".join(pass_order)
                    log.warning(msg)
                    order = pass_order
                    break

                fail_order = self.stages[stage]['change_order_if_fail']
                if fail_order and new_section.result in [Failed, Errored]:
                    msg = "Due to 'change_order_if_fail' the order of clean " \
                          "is changed to:\n- " + "\n- ".join(fail_order)
                    log.warning(msg)
                    order = fail_order

                    # In this case we do not want the overall clean result to
                    # be failed. Leave the section result alone but change the
                    # parents to Passed.
                    new_section.parent.parent.result = Passed
                    new_section.parent.result = Passed
                    new_section.result = Passed
                    break

                if not new_section.result:
                    # Dont log this for every remaining stage
                    if not aetest.executer.goto:
                        log.error(banner("*** Terminating Genie Clean ***"))

                    aetest.executer.goto_result = results.Blocked
                    msg = '{} has {}'.format(new_section.uid, new_section.result)
                    aetest.executer.goto = [[msg, str]]

                # image handler updates latest image
                if self.image_handler:
                    self.image_handler.update_image_references(section)

            else:
                # Every stage in 'order' successfully ran
                # Break from while loop to finish clean
                break

    def discover(self):
        """ Discovers and loads all clean stages defined within the clean
        yaml file. During loading validate that each stage is a TestSection.
        Once loading is complete a schema validation is executed to ensure
        the data provided is valid.
        """
        clean_schema = {}
        clean_to_validate = {}

        # order is mandatory so verify schema
        clean_schema['order'] = list
        if self.device.clean.get('order'):
            clean_to_validate['order'] = self.device.clean['order']

        # device_recovery is optional so verify schema only if provided
        device_recovery_data = self.device.clean.get('device_recovery')
        if device_recovery_data:
            clean_schema['device_recovery'] = recovery_processor.schema
            clean_to_validate['device_recovery'] = device_recovery_data

            # Setup and save the device recovery processor for later
            # use in __iter__()
            self.device_recovery_processor = partial(
                recovery_processor, **self.device.clean['device_recovery'])

        # Verify schema and load each stage
        for stage in self.device.clean:
            if stage in NOT_A_STAGE:
                continue

            if self.image_handler:
                self.image_handler.update_section(stage)

            stage_data = self.device.clean[stage] or {}
            if 'source' not in stage_data:
                # Attempt to load from clean json
                clean_json = load_clean_json()
                stage_func = get_clean_function(stage, clean_json, self.device)
            else:
                # Attempt to load from the provided source
                stage_func = load_class(stage_data, self.device)

            if not hasattr(stage_func, '__testcls__'):
                raise TypeError(
                    "The function definition for stage '{}' is missing the "
                    "@aetest.test decorator".format(stage_func.__name__))

            if hasattr(stage_func, 'schema'):
                clean_schema[stage_func.__name__] = stage_func.schema
                clean_to_validate[stage_func.__name__] = stage_data

                # unwrap from schema to get the original function
                stage_func = unwrap(stage_func)

            # Save for use later in __iter__()
            self.stages[stage] = {
                'func': stage_func,
                'change_order_if_pass': stage_data.pop('change_order_if_pass', None),
                'change_order_if_fail': stage_data.pop('change_order_if_fail', None),
                'stage_reuse_limit': stage_data.pop('stage_reuse_limit', None),
                'args': stage_data
            }

        try:
            Schema(clean_schema).validate(clean_to_validate)
        except Exception as e:
            raise pretty_schema_exception(e)


class DeviceClean(BaseCleaner):

    def clean(self, device, reporter, *args, **kwargs):

        # In this section we will convert to Genie Testbed
        testbed = load(device.testbed)
        device = testbed.devices[device.name]

        global_stage_reuse_limit = getattr(
            self, 'global_stage_reuse_limit', GLOBAL_STAGE_REUSE_LIMIT)

        clean_testcase = CleanTestcase(device, global_stage_reuse_limit)
        clean_testcase.reporter = reporter.testcase(clean_testcase)
        with clean_testcase:
            # 1. Figure out what section to run
            # 2. Run them
            result = clean_testcase()

            # Disconnect the device
            try:
                device.destroy_all()
            except Exception:
                pass

            if not result:
                raise Exception("Clean {result}.".format(result=str(result)))


class PyatsDeviceClean(DeviceClean):

    def clean(self, device, reporter, *args, **kwargs):
        super().clean(device, reporter, *args, **kwargs)
