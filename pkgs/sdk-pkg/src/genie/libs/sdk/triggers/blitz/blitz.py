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
                with steps.start("Verify the output of "
                                 "'{c}'".format(c=data['command']),
                                 continue_=True) as step:

                    if 'parsed' in data:
                        output = device.parse(data['command'])
                        for key in data['parsed']:
                            self.check_parsed_key(key, output, step)
                    if 'include' in data:
                        output = device.execute(data['command'])
                        for key in data['include']:
                            self.check_output(key, output, step, 'include')
                    if 'exclude' in data:
                        output = device.execute(data['command'])
                        for key in data['exclude']:
                            self.check_output(key, output, step, 'exclude')

    @aetest.setup
    def apply_configuration(self, testbed, configure=None):
        '''Apply configuration on the devices'''
        return self._configure(configure, testbed)

    @aetest.test
    def validate_configuration(self, steps, testbed, validate_configure=None):
        '''Valide'''
        return self._validate(validate_configure, testbed, steps)

    @aetest.test
    def remove_configuration(self, testbed, unconfigure=None):
        '''remove configuration on the devices'''
        return self._configure(unconfigure, testbed)

    @aetest.test
    def validate_unconfiguration(self, steps, testbed, validate_unconfigure=None):
        '''validate_unconfigure'''
        return self._validate(validate_unconfigure, testbed, steps)
