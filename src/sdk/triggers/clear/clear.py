'''Common implementation for clear triggers'''

# python import
import time
import logging

# ats import
from ats import aetest
from ats.utils.objects import R

# Genie Libs import
from genie.libs.sdk.triggers.template.clear import TriggerClear

log = logging.getLogger(__name__)


class TriggerClear(TriggerClear):
    '''Trigger class for Clear action'''

    @aetest.setup
    def verify_prerequisite(self, uut, abstract, steps, timeout):
        '''Learn Ops object and verify the requirements.

           If the requirements are not satisfied, then skip to the next
           testcase.

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object
               timeout (`timeout obj`): Timeout Object

           Returns:
               None

           Raises:
                pyATS Results
        '''
        self.timeout = timeout

        try:
            self.pre_snap = self.mapping.learn_ops(device=uut,
                                                   abstract=abstract,
                                                   steps=steps,
                                                   timeout=timeout)
        except Exception as e:
            self.errored("Section failed due to: '{e}'".format(e=e))

        for stp in steps.details:
            if stp.result.name == 'skipped':
                self.skipped('Cannot learn the feature', goto=['next_tc'])

    @aetest.test
    def clear(self, uut):
        '''Actual clear action by using cli

           Args:
               uut (`obj`): Device object

           Returns:
               None

           Raises:
               Failed: When cli command could not be sent correctly to the
                       device
        '''
        log.info("Execute Clear Command '{}'".format(self.clear_cmd))
        for cmd in self.clear_cmd:
            if '(?P' in cmd:
                req = self.mapping._path_population([cmd.split()], uut)
            else:
                req = [cmd]
            for cmd in req:
              # combine command
              if isinstance(cmd, list):
                  cmd = ' '.join(cmd)
              try:
                  uut.execute(cmd)
              except Exception as e:
                  self.failed("Issue while sending '{c}'".format(c=cmd),
                              from_exception=e)

    @aetest.test
    def verify_clear(self, uut, abstract, steps, timeout_recovery=None):
        '''Compares the snapshot from save_snapshot and this section,
           then verifies the clear action if needed

           Args:
               uut (`obj`): Device object

           Returns:
               None

           Raises:
               Failed: When state of the device did not revert to what it was
                       before clear command
               Errored: When looking for particular mapping_extra_args which
                        does not exists
        '''
        # Take a timestamp
        # This timestamp is used to calculate amount of time that learn_poll
        # takes
        pre_time = time.time()

        try:
            self.ops_obj = self.mapping.verify_with_initial(\
                                                   device=uut,
                                                   abstract=abstract,
                                                   steps=steps,
                                                   verify_find=self._verify,
                                                   uut = uut,
                                                   pre_time=pre_time,
                                                   timeout_recovery=timeout_recovery)
        except Exception as e:
            self.failed("The clear verification has failed", from_exception=e)

    def _verify(self, ops, pre_time, uut, **kwargs):

        # See if it can be verified
        self.mapping._verify_same(ops=ops, **kwargs)

        # At the moment only support one for ops_obj but could be enhanced
        self.ops_obj = ops

        # If no verify attribute
        if not hasattr(self, 'verify'):
            return

        # in case of inherit, introduce local var
        # for holding class glob vars
        loc_args = self.verify_func_args.copy()
        
        # populate r_object path
        reqs = []
        if 'r_obj' in loc_args:
            for r in loc_args['r_obj']:
                reqs.extend(self.mapping._path_population(r.args, uut))

        # store the populate path back to self.verify_func_args as R object
        if reqs:
            loc_args['r_obj'] = []
            for req in reqs:
                loc_args['r_obj'].append(R(req))

        # diff the pre and post time to compare the uptime
        self.compare_time = int(time.time() - pre_time)

        # update the mapping extra_args with variables
        try:
            for key, value in self.mapping_extra_args.items():
                loc_args[key] = getattr(self, value)
        except Exception as e:
            self.errored('Failed to get key {k} value {v}'.
                         format(k=key, v=value), from_exception=e)

        # compare the attributes that may changed as expected
        if 'r_obj' in loc_args:
            back_up = loc_args['r_obj'].copy()
            for r in back_up:
                loc_args['r_obj'] = [r]
                self.verify(**loc_args)
