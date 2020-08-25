import logging

# pyATS
from pyats.results import Passed, Passx
from pyats.aetest.steps import Steps

# Genie
from genie.utils import Dq
from genie.libs.sdk.triggers.blitz.blitz import Blitz
from genie.libs.parser.utils.common import format_output

log = logging.getLogger(__name__)


class Health(Blitz):
    def _check_processor_tag(self, data, data_dict='', processor_flag=''):
        """
        check `processor` keys in all action in section.
        sectionA:
          actionA:
            processor: pre
          actionB:
            processor: post
        above is not allowed. in the same section, `processor` should be 
        same among actions
        """
        if not data_dict:
            data_dict = {}
        for item in data:
            data_dict.update(item)
            for api_data in item.values():
                if 'processor' in api_data:
                    if processor_flag:
                        if processor_flag != api_data['processor']:
                            raise Exception(
                                "'processor' value is not same among actions")
                    else:
                        processor_flag = api_data['processor']
                else:
                    processor_flag = 'both'
        return data_dict, processor_flag

    def _check_all_devices_connected(self, testbed, data_dict_dq):
        # assumed all the targeted devices are connected.
        # each device will be checked. if one of devices is not connected,
        # change to False
        for dev in data_dict_dq.get_values('device'):
            # check if device object, or not
            if hasattr(dev, 'name'):
                dev = dev.name
            # check if device exists in testbed and if connected
            if dev in testbed.devices and not testbed.devices[
                    dev].is_connected():
                return False
        return True

    def _pre_post_processors(self,
                             testbed,
                             section,
                             data,
                             name,
                             devices_connected,
                             processor_flag,
                             processors,
                             processor_type,
                             pre_processor_result=Passed):
        # processor start message
        # import remote_pdb; remote_pdb.set_trace()
        log.debug('{type}-processor {name} started'.format(
            name=name, type=processor_type.capitalize()))
        pre_processor_run = True

        # check `processor` to control
        if processor_flag in processors:
            # if any device is not connected, processor will be skipped
            if devices_connected:
                # instantiate Steps() to reset step number
                steps = Steps()
                result = self.dispatcher(steps, testbed, section, data, name)

                log.debug('Blitz section return:\n{result}'.format(
                    result=format_output(result)))
                # check section result
                log.debug('section result: {section_result}'.format(
                    section_result=section.result.name))
                log.debug('steps result: {steps_result}'.format(
                    steps_result=steps.result.name))

                if processor_type == 'pre' and steps.result != Passed and steps.result != Passx:
                    log.info(
                        "Pre-processor pyATS Health {name} was failed, but continue section and Post-processor"
                        .format(name=name))
                    # save pre-processor result
                    pre_processor_result = steps.result
                    return pre_processor_run, pre_processor_result
                elif processor_type == 'post':
                    # refrect result to section
                    getattr(
                        section,
                        str(steps.result + steps.result +
                            self.pre_processor_result))()
                    return pre_processor_run, pre_processor_result

            else:
                if processor_type == 'pre':
                    pre_processor_run = False
                    # processor is skipped. but call passed to move forward     for this case
                    log.info(
                        "Pre-processor pyATS Health '{name}' is skipped  because devices are not connected."
                        .format(name=name))
                    return pre_processor_run, pre_processor_result
                elif processor_type == 'post':
                    # for the case only pre-processors runs
                    if section.result == pre_processor_result:
                        log.info(
                            'Only Pre-processor runs. Section result and Pre-processor result are different. Reflecting Post-processor result to Section.'
                        )
                        getattr(section,
                                str(section.result + pre_processor_result))()
                    log.info(
                        "Post-processor pyATS Health '{name}' was skipped because devices are not connected."
                        .format(name=name))
                    return pre_processor_run, pre_processor_result
        else:
            log.info('Skipped because {name} is not {type}-processor'.format(
                name=name, type=processor_type.capitalize()))
            return pre_processor_run, pre_processor_result

        return pre_processor_run, pre_processor_result

    def health_dispatcher(self,
                          steps,
                          section,
                          data,
                          testbed,
                          name='',
                          **kwargs):
        # pre-context processor

        # `data` contains all the items under a section in Blitz yaml
        #
        # example of `data`:
        # [
        #   {
        #     'parallel': [
        #       {
        #         'api': {
        #           'device': 'uut',
        #           'function': 'get_platform_cpu_load',
        #           'arguments': {
        #             'command': 'show processes cpu',
        #             'processes': ['BGP I/O']
        #           },
        #           'save': [
        #             {
        #               'variable_name': 'cpu'
        #             }
        #           ]
        #         }
        #       },
        #       {
        #         'api': {
        #           'device': 'uut',
        #           (snip)
        #
        # `data` is List, so store the `data` as dict to `data_dict` for Dq
        # check `processor` and return the value in processor_flag
        data_dict, processor_flag = self._check_processor_tag(data=data)
        log.debug('processor_flag: {flag}'.format(flag=processor_flag))

        # check if all devices are connected
        data_dict_dq = Dq(data_dict)
        devices_connected = self._check_all_devices_connected(
            testbed, data_dict_dq)

        # execute pre-processor and received result in self.pre_processor_result
        self.pre_processor_run, self.pre_processor_result = self._pre_post_processors(
            testbed,
            section,
            data,
            name,
            devices_connected,
            processor_flag,
            processors=['pre', 'both'],
            processor_type='pre')

        try:
            yield
        except Exception as e:
            # for case section gets Exception
            section.errored(e)

        # post-context processor

        # check `post_after_pre` and if pre-processor is executed
        if (data_dict_dq.get_values('processor', 0) == 'post_after_pre'
                and not self.pre_processor_run):
            log.info(
                "Post-processor pyATS Health '{name}' was skipped because required Pre-processor was not executed."
                .format(name=name))
        else:
            # check if all devices are connected
            data_dict_dq = Dq(data_dict)
            devices_connected = self._check_all_devices_connected(
                testbed, data_dict_dq)

            # execute post-processor
            self._pre_post_processors(
                testbed,
                section,
                data,
                name,
                devices_connected,
                processor_flag,
                processors=['post', 'post_after_pre', 'both'],
                processor_type='post',
                pre_processor_result=self.pre_processor_result)
