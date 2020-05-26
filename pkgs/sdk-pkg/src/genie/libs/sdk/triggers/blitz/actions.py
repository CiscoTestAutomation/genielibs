import re
import time
import logging

from genie.libs import sdk
from genie.harness.standalone import run_genie_sdk

from pyats.async_ import pcall
from pyats.log.utils import banner
from pyats.aetest.steps import Steps
from pyats.results import TestResult, Passed, Failed, Skipped, Passx, Aborted, Errored

from .markup import save_variable
from .yangexec import run_netconf, run_gnmi, notify_wait
from .actions_helper import configure_handler, api_handler, learn_handler, parse_handler, execute_handler


log = logging.getLogger()


def configure(self, device, steps, command, reply=None, continue_=True):

    # default output set to none in case of an exception
    output = None
    with steps.start("Configuring '{device}'".\
                    format(device=device.name), continue_=continue_) as step:

        output = configure_handler(self, step, device, command, reply)

    notify_wait(steps, device)

    return output

def parse(self, device, steps, command, include=None,
          exclude=None,  max_time=None, check_interval=None, continue_=True, *args, **kwargs):

    # action parse
    output = {}
    with steps.start("Parsing '{c}' on '{d}'".\
                    format(c=command, d=device.name), continue_=continue_) as step:

        output = parse_handler(self, step, device, command, include, exclude,
                              max_time, check_interval, continue_)

    notify_wait(steps, device)

    return output

def execute(self, device, steps, command, include=None, exclude=None,
            max_time=None, check_interval=None, reply=None, continue_=True):

    # action execute
    with steps.start("Executing '{c}' on '{d}'".\
                    format(c=command, d=device.name), continue_=continue_) as step:

        output = execute_handler(self, step, device, command, include, exclude,
                                max_time, check_interval, continue_, reply=reply)

    notify_wait(steps, device)

    return output

def api(self, device, steps, function, arguments=None, include=None,
        exclude=None, max_time=None, check_interval=None, continue_=True):

    # action api
    output = None
    with steps.start("Calling API '{f}' on '{d}'".\
                    format(f=function, d=device.name), continue_=continue_) as step:

        output = api_handler(self, step, device, function, include, exclude,
                            max_time, check_interval, continue_, function, arguments=arguments)

    notify_wait(steps, device)

    return output

def learn(self, device, steps, feature, include=None, exclude=None,
          max_time=None, check_interval=None, continue_=True):

    # action learn
    with steps.start("Learning '{f}' on '{d}'".\
                    format(f=feature, d=device.name), continue_=continue_) as step:

        output = learn_handler(self, step, device, feature, include, exclude, 
                              max_time, check_interval, continue_=continue_)

    return output

def sleep(self, steps, sleep_time, continue_=True, *args, **kwargs):
    log.info('Sleeping for {s} seconds'.format(s=sleep_time))
    time.sleep(float(sleep_time))
    
def yang(self, device, steps, protocol, datastore, content, operation,
         continue_=True, connection=None, returns=None, *args, **kwargs):
    if connection:
        device = getattr(device, connection)
        # Verify that we are connected
        # TODO
        # I think all our connection implementation (unicon, rest, yang)
        # should have an isconnected which does an action on the device, example show
        # clock for cli, to verify.  Right now, we dont havet his, we have
        # connected but we all know its of no use.
    if returns is None:
        returns = {}
    if protocol == 'netconf':
        result = run_netconf(operation=operation, device=device, steps=steps,
                             datastore=datastore, rpc_data=content,
                             returns=returns, **kwargs)
    elif protocol == 'gnmi':
        result = run_gnmi(operation=operation, device=device, steps=steps,
                          datastore=datastore, rpc_data=content,
                          returns=returns, **kwargs)
    if not result:
        steps.failed('Yang action has failed')
    
    if operation != 'subscribe':
        notify_wait(steps, device)

    return result

def configure_replace(self, device, steps, config, continue_=True, iteration=2, interval=30):
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

def save_config_snapshot(self, device, steps, continue_=True):
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

def restore_config_snapshot(self, device, steps, continue_=True, delete_snapshot=True):

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

def bash_console(self, device, steps, commands, continue_=True, **kwargs):

    ret_dict = {}
    with device.bash_console(**kwargs) as bash:
        for command in commands:
            output = bash.execute(command, **kwargs)
            ret_dict.update({command:output})
    
    return ret_dict

def genie_sdk(self, steps, continue_=True, **kwargs):
    sdks = list(kwargs.keys())
    run_genie_sdk(self, steps, sdks, parameters=kwargs)

def print(self, steps, continue_=True, *args, **kwargs):

    if 'steps' in kwargs:
        kwargs.pop('steps')
    
    for key, value in kwargs.items():
        if value.get('type') == 'banner':

            print_value = 'printing message: {k}\n{v}'.format(k=key,v=banner(value['value']))
        else:
            print_value = 'The value of {k}: {v}'.format(k=key,v=value['value'])

        log.info(print_value)

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
           'run_genie_sdk': genie_sdk,
           'bash_console': bash_console}

def action_parallel(self, steps, testbed, section, data):
    # When called run all the actions
    # below the keyword parallel concurently
    pcall_payloads = []
    with steps.start('Executing actions in parallel', continue_=True) as steps:

        for action_item in data:
            for action, action_kwargs in action_item.items():
                # for future use - Enhancement needed in pyATS
                # with steps.start("Implementing action '{a}' in parallel".format(a=actions)) as step:
                # on parallel it is not possible to set continue to False and benefit from that feature
                step = Steps()
                kwargs = {'steps': step, 'testbed': testbed, 'section': section, 'data': [{action:action_kwargs}]}
                pcall_payloads.append(kwargs)
        pcall_returns = pcall(self.dispatcher, ikwargs=pcall_payloads)

        # Each action return is a dictionary containing the action name, possible saved_variable
        # Action results, and device name that action is being implemented on
        # These value would be lost when the child processor that executes the action end the process.
        # It is being implemented this way in order to add these values to the main processor.
        for each_return in pcall_returns:

            if each_return.get('saved_vars'):
                for saved_var_name, saved_var_data in each_return.get('saved_vars').items():

                    if each_return.get('filters'):
                        log.info('Applied filter: {} to the action {} output'.format(each_return['filters'], action))

                    save_variable(self, saved_var_data, saved_var_name)
        
            if each_return['device']:
                msg = 'Executed action {action} on {device} in parallel'.format(
                    action=each_return['action'], device=each_return['device'])
            else:
                msg = 'Executed action {action} in parallel'.format(
                    action=each_return['action'])
 
            with steps.start(msg, continue_=True, description=each_return['description']) as report_step:

                log.info('Check above for detailed action report')
                getattr(report_step, str(each_return['step_result']))()
    
