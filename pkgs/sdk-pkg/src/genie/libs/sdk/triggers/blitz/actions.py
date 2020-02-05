import re
import time
import logging
import copy
from pyats.utils.objects import find, R
from pyats.async_ import pcall
from pyats.aetest.steps import Steps
from genie.utils.timeout import Timeout
from genie.utils.loadattr import str_to_list

from .yangexec import run_netconf

log = logging.getLogger()


def configure(self, device, steps, command):
    with steps.start("Configuring '{device}' ".format(device=device.name)):
        device.configure(command)

def parse(self, device, steps, command, output, max_time=0,
          check_interval=0, *args, **kwargs):
    with steps.start("Verifying the output of '{c}'".format(c=command),
                     continue_=True) as step:
        # TODO - support list of output
        # Without resending the same command
        _check_parsed_key(device, output[0], command, max_time, check_interval, step)

def execute(self, device, steps, command, include=None, exclude=None,
            max_time=0, check_interval=0):
    with steps.start("Executing '{c}' on "
                     "'{device}' ".format(c=command,
                                          device=device.name)) as step:
        if include:
            _check_output(device, include, command, max_time,
                               check_interval, step, 'include')

        if exclude:
            _check_output(device, exclude, command, max_time,
                               check_interval, step, 'exclude')

        if not include and not exclude:
            device.execute(command)

def sleep(self, sleep_time, *args, **kwargs):
    log.info('Sleeping for {s} seconds'.format(s=sleep_time))
    time.sleep(sleep_time)

def api(self, device, steps, function, arguments):
    # TODO - have a returns key to verify if the return is as expected
    # Optional
    # TODO - Test that all action when they fail, it actually fail the test
    # section correctly
    with steps.start(function) as step:
        try:
            if 'device' in arguments:
                arg_device = device.testbed.devices[arguments['device']]
                arguments['device'] = arg_device
            result = getattr(device.api, function)(**arguments)
        except Exception as e:
            step.failed('Verification "{}" failed : {}'.format(function,
                                                               str(e)))
        else:
            if result:
                step.passed()
            else:
                step.failed('Failed to {}'.format(function))

def yang(self, device, steps, protocol, datastore, content, operation,
                connection=None, returns=None, *args, **kwargs):
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
        if not result:
            steps.failed('Yang action has failed')



actions = {'configure': configure,
           'parse': parse,
           'execute': execute,
           'api': api,
           'sleep': sleep,
           'yang': yang}

def _check_parsed_key(device, key, command, max_time, check_interval, step):
    keys = str_to_list(key)
    reqs = R(list(keys))

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

    with step.start("Verify that '{k}' is in the output".format(k=key)) as step:
        if max_time and check_interval:
            timeout = Timeout(max_time, check_interval)

            while timeout.iterate():
                output = device.parse(command)
                found = find([output], reqs, filter_=False, all_keys=True)
                if found:
                    break
                timeout.sleep()

            if not found:
                step.failed("Could not find '{k}'".format(k=key))
            else:
                log.info("Found {f}".format(f=found))

        else:
            output = device.parse(command)
            found = find([output], reqs, filter_=False, all_keys=True)
            if not found:
                step.failed("Could not find '{k}'".format(k=key))
            else:
                log.info("Found {f}".format(f=found))

            #_check_output(device, exclude, command, max_time,
            #                   check_interval, step, 'exclude')

def _check_output(device, strings, command, max_time, check_interval,
                  step, style):
    assert style in ['include', 'exclude']

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

    # TODO - now is sends the same show command multiple time, reduce to
    # only once
    for key in strings:
        key = str(key)
        pattern = re.compile(key)
        msg = "Verify that '{k}' is {style}'d in the "\
              "output".format(k=key, style=style)

        with step.start(msg) as step:

            if max_time and check_interval:
                timeout = Timeout(max_time, check_interval)

                while timeout.iterate():
                    output = device.execute(command)
                    m = pattern.search(output)
                    if style == 'include' and m:
                        step.passed("Found {k}".format(k=key))
                    elif style == 'exclude' and not m:
                        step.passed("Not Found {k}".format(k=key))

                    timeout.sleep()

                if style == 'include':
                    step.failed("Could not find '{k}'".format(k=key))
                else:
                    step.failed("Could find '{k}'".format(k=key))

            else:
                output = device.execute(command)
                m = pattern.search(output)
                if style == 'include':
                    if not m:
                        step.failed("Could not find '{k}'".format(k=key))
                    else:
                        log.info("Found {k}".format(k=key))
                else:
                    if m:
                        step.failed("Could find '{k}'".format(k=key))
                    else:
                        log.info("Not Found {k}".format(k=key))

def action_parallel(self, steps, testbed, data):
    # When called run all the actions
    # below the keyword parallel concurently
    pcall_payloads = []
    for action_item in data:
        for action, action_kwargs in action_item.items():
            # for future use - Enhancement needed in pyATS
            # with steps.start("Implementing action '{a}' in parallel".format(a=actions)) as step:
            steps = Steps()
            kwargs = {'steps': steps,
                      'testbed': testbed,
                      'data': [{action:action_kwargs}]}
            pcall_payloads.append(kwargs)

    pcall(self.dispatcher, ikwargs=pcall_payloads)

def device_parallel(self, steps, testbed, data):
    # When called run all the devices
    # below the keyword parallel concurently
    parallel_dict = data.pop('parallel', None)
    pcall_payloads = []
    for key, value in parallel_dict.items():
        for item in value:
            setup_dict = copy.deepcopy(data)
            setup_dict[key] = [item]
            for dev in item.keys():
                # for future use
                # with steps.start("Running devices '{d}' in parallel".format(d=dev)) as step:
                steps = Steps()
                kwargs = {'steps': steps, 'testbed': testbed, 'data': setup_dict}
                pcall_payloads.append(kwargs)
    
    pcall(self.dispatcher, ikwargs=pcall_payloads)       
