import time
import logging
from ats import aetest
from ats.utils.objects import find, R
from genie.utils.loadattr import str_to_list
from genie.harness.base import Trigger

log = logging.getLogger()


class Blitz(Trigger):
    '''Apply some configuration, validate some keys and remove configuration'''

    def check_parsed_key(self, key, output, step):
        keys = str_to_list(key)
        with step.start("Verify that '{k}' is in the "
                        "output".format(k=key)) as step:
            reqs = R(list(keys))
            found = find([output], reqs, filter_=False,
                         all_keys=True)
            if not found:
                step.failed("Could not find '{k}'"
                            .format(k=key))
            else:
                log.info("Found {f}".format(f=found))

    def check_output(self, key, output, step, style):
        msg = "Verify that '{k}' is {style}d the "\
              "output".format(k=key, style=style)
        with step.start(msg) as step:
            key = str(key)
            if style == 'include':
                if key not in output:
                    step.failed("Could not find '{k}'"
                                .format(k=key))
                else:
                    log.info("Found {k}".format(k=key))
            elif style == 'exclude':
                if key in output:
                    step.failed("Could find '{k}'"
                                .format(k=key))
                else:
                    log.info("Not Found {k}".format(k=key))
            else:
                raise Exception("{s} not supported")

    def _configure(self, data, testbed):
        if not data:
            log.info('Nothing to configure')
            return

        if 'devices' not in data:
            log.info('No devices to apply configuration on')
            return

        for dev, config in data['devices'].items():
            device = testbed.devices[dev]

            # if config is a dict, then try apply config with api
            if isinstance(config, dict):
                for c in config:
                    function = config[c].get('api')
                    if not function:
                        self.error('No API function is found, the config must be a string or a dict contatining the key "api"')

                    args = config[c].get('arguments')
                    if 'device' in args:
                        arg_device = testbed.devices[args['device']]
                        args['device'] = arg_device
                    getattr(device.api, function)(**args)

            # if not a dict then apply config directly
            else:
                device.configure(config)

        if 'sleep' in data:
            log.info('Sleeping for {s} seconds to stabilize '
                     'new configuration'.format(s=data['sleep']))
            time.sleep(data['sleep'])

    def _validate(self, data, testbed, steps):
        if not data:
            log.info('Nothing to validate')
            return

        if 'devices' not in data:
            log.info('No devices to data configuration on')
            return

        for dev, command in data['devices'].items():
            device = testbed.devices[dev]
            for i, data in sorted(command.items()):
                command = data.get('command')
                function = data.get('api')
                # if command is given, validate with parser
                if command:
                    with steps.start("Verify the output of '{c}'".format(c=command),
                                     continue_=True) as step:
                        if 'parsed' in data:
                            output = device.parse(command)
                            for key in data['parsed']:
                                self.check_parsed_key(key, output, step)
                        if 'include' in data:
                            output = device.execute(command)
                            for key in data['include']:
                                self.check_output(key, output, step, 'include')
                        if 'exclude' in data:
                            output = device.execute(command)
                            for key in data['exclude']:
                                self.check_output(key, output, step, 'exclude')

                # if no command given, validate with api function
                elif function:
                    with steps.start(function) as step:
                        try:
                            args = data.get('arguments')
                            if 'device' in args:
                                arg_device = testbed.devices[args['device']]
                                args['device'] = arg_device
                            result = getattr(device.api, function)(**args)
                        except Exception as e:
                            step.failed('Verification "{}" failed : {}'.format(function, str(e)))
                        else:
                            if result:
                                step.passed()
                            else:
                                step.failed('Failed to {}'.format(function))
                else:
                    self.error('No command or API found for verification # {}.'.format(i))

    @aetest.setup
    def apply_configuration(self, testbed, configure=None):
        '''Apply configuration on the devices'''
        return self._configure(configure, testbed)

    @aetest.test
    def validate_configuration(self, steps, testbed, validate_configure=None):
        '''Validate configuration on the devices'''
        return self._validate(validate_configure, testbed, steps)

    @aetest.test
    def remove_configuration(self, testbed, unconfigure=None):
        '''remove configuration on the devices'''
        return self._configure(unconfigure, testbed)

    @aetest.test
    def validate_unconfiguration(self, steps, testbed, validate_unconfigure=None):
        '''Validate unconfiguration on the devices'''
        return self._validate(validate_unconfigure, testbed, steps)
