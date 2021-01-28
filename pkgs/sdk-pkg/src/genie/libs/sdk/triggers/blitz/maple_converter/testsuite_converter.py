import os
import logging
import ruamel.yaml

from ats.easypy import runtime

#genie
from genie.utils import Dq
from genie.testbed import load
from genie.harness.main import gRun

from .maple_converter import Converter

log = logging.getLogger(__name__)



class Testsuite_Converter(object):
    def __init__(self, testsuite_file):
        self.testsuite_file = testsuite_file

    def grun_kwargs_generator(self):

        kwargs = {}
        clean_files = []
        skip_testcases = []
        run_testcases = []
        # all the possible keys in a maple testsuite
        ts_keywords = {'testcase_control': None,
                       'teststep_control': None,
                       'tims_testplan_folder': None,
                       'tims_result_folder': None,
                       'testbed_file': None,
                       'testcase_file': None}

        # Going through the testsuite and yielding testbed, testcase_name,
        # the equivalent of trigger_uids etc. to the above generator
        with open(self.testsuite_file, 'r') as tempfile:
            testsuite_string = tempfile.read()

        testsuite_dict = ruamel.yaml.safe_load(testsuite_string)
        for each_testcase, testcase_arguments in testsuite_dict['tasks'].items():

            runtime.args.clean_files = None
            for key, value in testcase_arguments.items():

                # Getting all the values of the job file
                if key in ts_keywords.keys():

                    ts_keywords[key] = value
                elif key == 'run':

                    run_testcases = value.split(',')
                elif key == 'skip':

                    skip_testcases = value.split(',')
                elif key == 'clean_file':

                    clean_files.append(value)
                    runtime.args.clean_files = clean_files
                    runtime.args.invoke_clean = True
                    runtime.args.check_all_devices_up = True

            kwargs = self.updating_grun_kwargs(kwargs,
                                               ts_keywords,
                                               run_testcases,
                                               skip_testcases)
            yield kwargs


    def updating_grun_kwargs(self,
                             grun_kwargs,
                             ts_keywords,
                             run_testcases,
                             skip_testcases):

        try:
            # Calling the converter
            converter = Converter(ts_keywords['testcase_file'],
                                  testbed=ts_keywords['testbed_file'],
                                  testcase_control=ts_keywords['testcase_control'],
                                  teststep_control=ts_keywords['teststep_control'],
                                  tims_testplan_folder=ts_keywords['tims_testplan_folder'])

            trigger_uids = converter.convert()

        except Exception as e:
            raise Exception(
                            'Unable to translate maple script due to the following error:{}'.format(str(e)))

        # update if skip or run key is specified in testsuite
        if run_testcases or skip_testcases:
            trigger_uids = self._update_trigger_uids(trigger_uids,
                                                     run_testcases=run_testcases,
                                                     skip_testcases=skip_testcases)
        # Arguments of the gRun in JOB file
        grun_kwargs.update({'subsection_datafile': self._subsection_datafile_creator(),
                            'trigger_datafile': converter.blitz_file,
                            'testbed': converter.testbed_file,
                            'trigger_uids': trigger_uids,
                            'tims_folder': ts_keywords['tims_result_folder'],
                            'mapping_datafile': self._mapping_datafile_creator(
                                                            testbed=ts_keywords['testbed_file'])})

        return grun_kwargs

    def _subsection_datafile_creator(self):

        # Generating subsection datafile
        subsection_dict = {'setup': {
                                'sections':{
                                    'connect':{
                                        'method': 'genie.harness.commons.connect'
                                        }
                                },
                                'order':['connect']
                            },
                            'cleanup': {
                                'sections': {},
                                'order': []
                            }
                        }

        additionals_dir = self._get_dir_for_additional_datafile()

        with open(additionals_dir+ '/subsection_datafile.yaml', 'w') as subsection_file_dumped:
            subsection_file_dumped.write(ruamel.yaml.round_trip_dump(subsection_dict))

        return additionals_dir+ '/subsection_datafile.yaml'

    def _mapping_datafile_creator(self, testbed):

        # Generating mapping datafile
        mapping_dict = {}
        mapping_dict.setdefault('devices', {})

        testbed = load(testbed)

        for dev, dev_args in testbed.devices.items():

            # if ha device mapping datafile with [a, b]
            if 'a' in dev_args.connections and \
               'b' in dev_args.connections:

                mapping_dict['devices'].update({dev: {'mapping': {'cli': ['a', 'b']}}})

            # for single connection devices just a
            elif 'a' in dev_args.connections:
                mapping_dict['devices'].update({dev: {'mapping': {'cli': 'a'}}})

            # for devices with cli connection,
            # we pick the first connection in the list of connection
            # Usually these cases should have only one connection in the testbed
            else:
                connections = Dq(dev_args.connections).\
                              not_contains('default.*', regex=True).\
                              reconstruct()

                connection = list(connections.keys())[0]
                mapping_dict['devices'].update({dev: {'mapping': {'cli': connection}}})

        additionals_dir = self._get_dir_for_additional_datafile()

        with open(additionals_dir+ '/mapping_datafile.yaml', 'w') as mapping_file_dumped:
            mapping_file_dumped.write(ruamel.yaml.round_trip_dump(mapping_dict))

        return additionals_dir+ '/mapping_datafile.yaml'

    def _get_dir_for_additional_datafile(self):

        # just create a new directory to store subsection and mapping datafile inside
        testsuite_dir_name = os.path.dirname(os.path.abspath(self.testsuite_file))
        additionals_dir = testsuite_dir_name+ '/additional_datafiles'

        # If folder doesn't exist, then create it.
        if not os.path.isdir(additionals_dir):
            os.makedirs(additionals_dir)

        return additionals_dir

    def _update_trigger_uids(self, trigger_uids, run_testcases=None, skip_testcases=None):

        # when run is set, testcases in the list of run should run
        if run_testcases:
            return [rt.strip() for rt in run_testcases if rt.strip()]
        # when skip is set, testcases in the list of skip should not run
        if skip_testcases:
            return [tc for tc in trigger_uids if tc in skip_testcases]
