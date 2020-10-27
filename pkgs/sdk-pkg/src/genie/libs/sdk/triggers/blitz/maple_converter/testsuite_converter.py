import os
import ruamel.yaml

#genie
from genie.utils import Dq
from genie.testbed import load
from genie.harness.main import gRun
from genie.libs.sdk.triggers.blitz.maple_converter.maple_converter import Converter



class Testsuite_Converter(object):
    def __init__(self, testsuite_file):
        self.testsuite_file = testsuite_file

    def grun_kwargs_generator(self):

        kwargs = {}
        run_testcases = []
        # Control values for section action 
        # in blitz --> continue: False
        testcase_control = None
        teststep_control = None

        # Going through the testsuite and yielding testbed, testcase_name, the equivalent of trigger_uids etc. to the above generator
        with open(self.testsuite_file, 'r') as tempfile:
            testsuite_string = tempfile.read()

        testsuite_dict = ruamel.yaml.safe_load(testsuite_string)
        for each_testcase, testcase_arguments in testsuite_dict['tasks'].items():
            for key, value in testcase_arguments.items():

                # Getting all the values of the job file
                if key == 'testbed_file':
                    testbed = value
                elif key == 'testcase_file':
                    testcase = value
                elif key == 'run':
                    run_testcases = value.split(',')
                elif key == 'testcase_control':
                    testcase_control = value
                elif key =='teststep_control':
                    teststep_control = value

            try:
                # Calling the converter 
                converter = Converter(testcase, testbed=testbed, 
                                     testcase_control=testcase_control, teststep_control=teststep_control)
                trigger_uids = converter.convert()

            except Exception as e:
                raise Exception('Testbed {} or testcase {} or both are not valid. {}'.format(testbed, testcase, str(e)))

            if run_testcases:
                trigger_uids = run_testcases

            # Arguments of the gRun in JOB file
            kwargs.update({'subsection_datafile': self.subsection_datafile_creator(),
                           'mapping_datafile': self.mapping_datafile_creator(testbed),
                           'trigger_datafile': converter.blitz_file,
                           'testbed': converter.testbed_file,
                           'trigger_uids': trigger_uids})
            yield kwargs

    def subsection_datafile_creator(self):

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

    def mapping_datafile_creator(self, testbed):

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
