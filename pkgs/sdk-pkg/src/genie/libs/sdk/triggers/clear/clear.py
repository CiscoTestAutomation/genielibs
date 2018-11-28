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

        self.print_local_verifications()

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
        # Take a timestamp
        # This timestamp is used to calculate amount of time that learn_poll
        # takes
        self.pre_time = time.time()
        
        # replace the regexp when there are some
        for cmd in self.clear_cmd:
            if '(?P' in cmd:
                req = self.mapping._path_population([cmd.split()], uut)
            else:
                req = [cmd]
            for cmd in req:
              # combine command
              if isinstance(cmd, list):
                  exec_cmd = ''
                  for item in cmd:
                      exec_cmd += '%s ' % str(item)
                  cmd = exec_cmd

              # execute commands    
              log.info("Execute Clear Command '{}'".format(cmd))
              try:
                  uut.execute(cmd)
              except Exception as e:
                  self.failed("Issue while sending '{c}'".format(c=cmd),
                              from_exception=e)

    @aetest.test
    def verify_clear(self, uut, abstract, steps, timeout=None):
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
        # update the verify_ops callable with required information
        for req in self.mapping._verify_ops_dict.values():
            for item in req.get('requirements', {}):
                if not callable(item[0]):
                    continue
                ret = item[0]
                ret.keywords.update({'uut': uut, 'pre_time': self.pre_time, 'mapping': self.mapping})

        try:
            self.mapping.verify_ops(device=uut, abstract=abstract,
                                    steps=steps)
        except Exception as e:
            self.failed("The clear verification has failed", from_exception=e)


def verify_clear_callable(ops, uut, pre_time, verify_func, mapping, **kwargs):

    # If no verify attribute
    if not kwargs.get('verify_func_args', None):
        return

    # in case of inherit, introduce local var
    # for holding class glob vars
    verify_func_args = kwargs['verify_func_args'].copy()
    
    # populate r_object path
    reqs = []
    if 'r_obj' in verify_func_args:
        reqs.extend(mapping._path_population(verify_func_args['r_obj'], uut))

    # store the populate path back to self.verify_func_args as R object
    extra_args = {}
    if reqs:
        verify_func_args['r_obj'] = []
        for req in reqs:
            verify_func_args['r_obj'].append(R(req))

    # diff the pre and post time to compare the uptime
    # + 1 is fuzzy time that may diff from routers timing and script
    compare_time = int(time.time() - pre_time + 1)

    # update the mapping extra_args with variables
    for key, value in verify_func_args.items():
        if isinstance(value, str):
            # get the value from the inital ops to compare
            if value.startswith('(?P'):
                value = mapping._populate_path([[value]], ops.device, mapping.keys)
                verify_func_args[key] = value[0][0]
            else:
                if locals().get(value) or locals().get(value) == 0:
                    verify_func_args[key] = locals().get(value)
                else:
                    verify_func_args[key] = value

    # compare the attributes that may changed as expected
    if 'r_obj' in verify_func_args:
        back_up = verify_func_args['r_obj'].copy()
        for r in back_up:
            verify_func_args['r_obj'] = [r]
            verify_func(**verify_func_args)
