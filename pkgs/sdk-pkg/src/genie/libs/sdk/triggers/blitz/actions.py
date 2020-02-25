import re
import time
import logging
import copy
import operator
from pyats.utils.objects import find, R
from pyats.async_ import pcall
from pyats.aetest.steps import Steps
from genie.utils.timeout import Timeout
from genie.utils.loadattr import str_to_list
from genie.libs import sdk
from genie.harness.standalone import run_genie_sdk

from .markup import get_variable
from .markup import save_variable
from pyats.results import TestResult, Passed, Failed, Skipped, Passx, Aborted, Errored
from unicon.eal.dialogs import Statement, Dialog

from .yangexec import run_netconf, run_gnmi

log = logging.getLogger()

def configure(self, device, steps, command, reply=None):
    with steps.start("Configuring '{device}' ".format(device=device.name), continue_=True) as step:
        try :
            if reply:
                output = device.configure(command, reply=_prompt_handler(reply))    
            
            output = device.configure(command)
        except Exception as e:
            output = None
            step.failed('Configure failed ==> {}'.format(str(e)))

    return output, steps.__result__

def parse(self, device, steps, command, include=None,
          exclude=None,  max_time=None, check_interval=None, *args, **kwargs):

    return _find_key_actions(self, device, steps, command, include, exclude,
                             max_time, check_interval, 'parse')

def execute(self, device, steps, command, include=None, exclude=None,
            max_time=None, check_interval=None, reply=None):

    return _find_key_actions(self, device, steps, command, include, exclude,
                             max_time, check_interval, 'execute', reply)    

def sleep(self, steps, sleep_time, *args, **kwargs):
    with steps.start('Sleeping for {s} seconds'.format(s=sleep_time), continue_=True):
        time.sleep(float(sleep_time))

    return None, steps.__result__

def api(self, device, steps, function, arguments, output=None):
    with steps.start("Executing API function ==> {} on {}".format(function, device), continue_=True) as step:
        try:
            if 'device' in arguments:
                arg_device = device.testbed.devices[arguments['device']]
                arguments['device'] = arg_device
            result = getattr(device, function)(**arguments) if device.os == 'ixianative'\
                 else getattr(device.api, function)(**arguments)
        except Exception as e:
            result = None
            if not function in dir(device.api):
                step.failed(str(e))
            else:
                step.failed("Verification of the input '{}' failed : {}".format(function,str(e)))
        else:
            if result:
                kwargs = {'result': result, 'step': step}
                if output:
                    kwargs.update({'value': output.get('value')})
                    kwargs.update({'operation': output.get('operation', '==')})

                _check_value_result (**kwargs)
            else:
                step.passed('The API ==> {} completed its job'.format(function))  

    return result, steps.__result__
       
def yang(self, device, steps, protocol, datastore, content, operation,
         connection=None, returns=None, *args, **kwargs):
    with steps.start('yang action', continue_=True) as step:
        if connection:
            device = getattr(device, connection)
            # Verify that we are connected
            # TODO
            # I think all our connection implementation (unicon, rest, yang)
            # should have a which does an action on the device, example show
            # clock for cli, to verify.  Right now, we dont havet his, we have
            # connected but we all know its of no use.

        if returns is None:
            returns = {}
        if protocol == 'netconf':
            result = run_netconf(operation=operation, device=device, steps=steps,
                                 datastore=datastore, rpc_data=content,
                                 returns=returns)
        elif protocol == 'gnmi':
            result = run_gnmi(operation=operation, device=device, steps=steps,
                              datastore=datastore, rpc_data=content,
                              returns=returns)
            if not result:
                step.failed('Yang action has failed')

    return result, steps.__result__

def learn(self, device, steps, feature, ops, include=None, exclude=None,
          max_time=None, check_interval=None):

    return _find_key_actions(self, device=device, steps=steps, command=feature,
                             include=include, exclude=exclude, max_time=max_time,
                             check_interval=check_interval, action='learn' , ops=ops)

def configure_replace(self, device, steps, config, iteration=2, interval=30):
    with steps.start('restore action', continue_=True):
        restore = sdk.libs.abstracted_libs.restore.Restore(device=device)

        # lib.to_url is normally saved via restore.save_configuration()
        # but since we only want the os abstraction and we are providing
        # a config - Just set the to_url equal to the config path provided
        restore.lib.to_url = config

        restore.restore_configuration(
            device=device,
            abstract=None,
            method='config_replace',
            iteration=iteration,
            interval=interval,
            delete_after_restore=False,
        )

    return None, steps.__result__

def save_config_snapshot(self, device, steps):
    with steps.start('save_config action', continue_=True):
        # setup restore object for device
        if not hasattr(self, 'restore'):
            self.restore = {}
        if device not in self.restore:
            self.restore[device] = sdk.libs.abstracted_libs.restore.Restore(device=device)

        # Get default directory
        save_dir = getattr(self.parent, 'default_file_system')
        if not save_dir:
            self.parent.default_file_system = {}

        # learn default directory
        if device.name not in save_dir:
            self.parent.default_file_system.update({
                device.name: self.restore[device].abstract.sdk.libs.abstracted_libs.\
                    subsection.get_default_dir(device=device)})

        self.restore[device].save_configuration(
            device=device,
            abstract=None,
            method='config_replace',
            default_dir=self.parent.default_file_system
        )

        # To keep track of snapshots (whether they are deleted or not)
        self.restore[device].snapshot_deleted = False

    return None, steps.__result__

def restore_config_snapshot(self, device, steps, delete_snapshot=True):
    with steps.start('restore_config action', continue_=True):
        if not hasattr(self, 'restore') or device not in self.restore:
            steps.errored("Must use action 'save_config_snapshot' first.\n\n")

        # If the snapshot file was deleted - error
        if self.restore[device].snapshot_deleted:
            steps.errored("If you want to restore with the same snapshot "
                          "multiple times then you must pass 'delete_snapshot=False' "
                          "to previous uses of this action. Otherwise the "
                          "snapshot will be deleted on the first usage.")

        try:
            self.restore[device].restore_configuration(
                device=device,
                abstract=None,
                method='config_replace',
                delete_after_restore=delete_snapshot
            )
        except Exception as e:
            steps.failed(str(e))

        # To keep track of snapshots (whether they are deleted or not)
        if delete_snapshot:
            self.restore[device].snapshot_deleted = True

    return None, steps.__result__

def genie_sdk(self, steps, **kwargs):
    with steps.start('run_genie_sdk action', continue_=True):
        sdks = list(kwargs.keys())
        run_genie_sdk(self, steps, sdks, parameters=kwargs)

    return None, steps.__result__

def print(self, steps, *args, **kwargs):
    with steps.start('Print action', continue_=True):
        if 'steps' in kwargs:
            kwargs.pop('steps')

        for key, value in kwargs.items():
            log.info('The value of {k}: {v}'.format(k=key,v=value))

    return None, steps.__result__

actions = {'configure': configure,
           'parse': parse,
           'execute': execute,
           'api': api,
           'tgn': api,
           'sleep': sleep,
           'yang': yang,
           'learn': learn,
           'print': print,
           'configure_replace': configure_replace,
           'save_config_snapshot': save_config_snapshot,
           'restore_config_snapshot': restore_config_snapshot,
           'run_genie_sdk': genie_sdk}

def _check_value_result(result, step, value=None, operation=None, style=None):
    # Checking the inclusion or exclusion and verifies result values
    # With regards to different operations for actions ('api','parse', 'learn')
    if result and not value:
        step.passed("Found ==> '{}' as the output".format(result))

    try :
        dict_of_ops = {'==': operator.eq, '>=':operator.ge,
        '>': operator.gt, '<=':operator.le, '<':operator.le,
        '!=':operator.ne}
        result = float(result)
        value = float(value)
    except:
        # If not a float/int, the only valid operations are == and !=
        if type(result) == type(value):
            dict_of_ops =  {'==': operator.eq, '!=':operator.ne}
            if isinstance(result, str) and isinstance(value, str):
                # If string allow to check if the return value contains any specific term
                dict_of_ops.update({'contains': operator.contains})
        else:
            step.errored('{} and {} are not of the same type'.format(result, value))

    if not operation in dict_of_ops.keys():
        step.errored('The operation should be from the following list ==> {}.'.format(dict_of_ops))

    if dict_of_ops[operation](result, value):
        msg = "The keyword ==> {} was not found in output".format(value) if style == 'excluded'\
            else "The included value ==> ({}) and expected value ==> ({}) are functioning as expected"\
                .format(result, value)

        step.passed(msg)
    msg = "The keyword ==> {} was found in output".format(value) if style == 'excluded'\
        else "The expected result is not met. The value is ==> ({}). The expected value ==> ({}). The operation is ({})"\
            .format(result, value, operation)

    step.failed(msg)


def _execute_validation(result, step, style, key):
    # Validating execute results
    if style == "included" and result:
        step.passed("Found '{k}' in the output".format(k=key))
    elif style =='excluded' and not result:
        step.passed("Did not find '{k}' in the output".format(k=key))
    elif style == "included" and not result:
        log.info("Could not find ==> '{k}' in the output".format(k=key))
    else:
        log.info("Found ==> '{k}' in the output".format(k=key))

def _get_timeout_from_ratios(device, max_time, check_interval):

    max_time_ratio = device.custom.get('max_time_ratio', None)
    if max_time and max_time_ratio:
        try:
            max_time = int(max_time * float(max_time_ratio))
        except ValueError:
            log.error('The max_time_ratio ({m}) value is not of type float'.format(m=max_time_ratio))

    check_interval_ratio = device.custom.get('check_interval_ratio', None)
    if check_interval and check_interval_ratio:
        try:
            check_interval = int(check_interval * float(check_interval_ratio))
        except ValueError:
            log.error('The check_interval_ratio ({c}) value is not of type float'.format(c=check_interval_ratio))
    return max_time, check_interval

def action_parallel(self, steps, testbed, data):
    # When called run all the actions
    # below the keyword parallel concurently
    pcall_payloads = []
    with steps.start('Executing actions in parallel', continue_=True) as steps:

        for action_item in data:
            for action, action_kwargs in action_item.items():
                # for future use - Enhancement needed in pyATS
                # with steps.start("Implementing action '{a}' in parallel".format(a=actions)) as step:
                step = Steps()
                kwargs = {'steps': step, 'testbed': testbed, 'data': [{action:action_kwargs}]}
                pcall_payloads.append(kwargs)
        pcall_returns = pcall(self.dispatcher, ikwargs=pcall_payloads)
        # Each action return is a dictionary containing the action name, possible saved_variable
        # Action results, and device name that action is being implemented on
        # These value would be lost when the child processor that executes the action end the process.
        # It is being implemented this way in order to add these values to the main processor.  
        for each_return in pcall_returns:

            if each_return.get('saved_var'):
                saved_var_data = each_return['saved_var'][0]
                saved_var_name = each_return['saved_var'][1]
                save_variable(self, saved_var_data, saved_var_name)

            with steps.start('Executed {} on {} in parallel'.format(each_return['action'], each_return['device']),continue_=True) as report_step:
                 getattr(report_step, str(each_return['step_result']))()

def _prompt_handler(reply):
    dialog_list = []
    for statement in reply:
        dialog_list.append(Statement(**statement))
    
    return Dialog(dialog_list)

def _find_key_actions(self, device, steps, command,  include, 
            exclude, max_time, check_interval, action, reply=None, ops=None):

    # Inclusion, exclusion process.
    keys = []
    if include:
        for item in include:
            keys.append((item, 'included'))
    if exclude:
        for item in exclude:
            keys.append((item, 'excluded'))

    max_time, check_interval = _get_timeout_from_ratios(
        device=device, max_time=max_time, check_interval=check_interval)

    with steps.start("Executing '{c}' on '{device}'"
                     .format(c=command, device=device.name)) as step:
        

        output =  getattr(device, action)(command, reply= _prompt_handler(reply)) if reply else \
            getattr(device, action)(command)

        if action == 'learn':
            output = getattr(output, ops) if hasattr(output, ops) else {}

        for key, style in keys:
            pattern = re.compile(str(key)) if action == 'execute' else \
                R(list(str_to_list(key['key']+'[(.*)]')))

            with step.start("Verify that '{key}' is {style} in the output"
                            .format(key= key if action == 'execute' else key['key'] , style=style), continue_=True) as substep:

                # for each key to verify, start with the previous output
                send_cmd = False
                timeout = Timeout(max_time, check_interval)
                while True:
                    if send_cmd:
                        output = getattr(device, action)(command)
                    else:
                        log.info("Using previous output to verify")

                    # set flag to send command on next iteration in case we are polling
                    send_cmd = True
                    if action == 'execute':
                        found = pattern.search(output)
                        _execute_validation(found, substep, style, key)
                    else:
                        try:
                            found = find([output], pattern, filter_=False, all_keys=True)[0][0]
                        except Exception as e:
                            substep.errored('The keywords are not inputed appropriately {}'\
                                .format(str(e)))
                        else:
                            value = key.get('value')
                            operation = key.get('operation', '==') if style == 'included' \
                                else '!='

                        _check_value_result(found, substep, value, operation, style)

                    timeout.sleep()
                    if not timeout.iterate():
                        break

                # failing logic
                if style == "included":
                    substep.failed("Could not find '{k}' in the output".format(k=key))
                elif style == "excluded":
                    substep.failed("Found '{k}' in the output".format(k=key))
    return output, steps.__result__
