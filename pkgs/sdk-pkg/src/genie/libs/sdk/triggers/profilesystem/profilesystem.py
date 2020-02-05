'''Common implementation for profilesystem triggers'''

# import python
import logging

# import pyats
from pyats import aetest

# Genie
from genie.harness.base import Trigger
from genie.utils.profile import Profile, summarize_comparison

log = logging.getLogger(__name__)


class TriggerProfileSystem(Trigger):
    '''Trigger class for ProfileSystem action'''

    @aetest.test
    def learn(self, testbed):
        '''Learn features passed in the trigger datafile

        Args:
            testbed (`obj`): testbed object.

        Returns:
            None

        Raises:
            pyATS Results
        '''

        self.location = self.parameters['location'] \
            if 'location' in self.parameters else None
        self.golden_file = self.parameters['golden_file'] \
            if 'golden_file' in self.parameters else  None
        self.features = self.parameters['features'] \
            if 'features' in self.parameters else  None

        if not self.features:
            self.errored("No features to be learnt were passed in the trigger "
                "datafile")

        try:
            self.learnt_output_1 = Profile.learn_features(
                            features=self.features,
                            testbed=testbed,
                            file=self.golden_file,
                            location=self.location,
                            pts_name=self.__uid__)
        except KeyError:
            self.errored("No features to be learnt were passed in the trigger "
                "datafile")
        except Exception as e:
            self.failed("Learning features '{f}' failed".format(
                f=self.features), from_exception=e)

        if self.golden_file:
            compare_result = Profile.compare(
                compare1=self.learnt_output_1,
                compare2=self.golden_file,
                pts_data=self.parent.pts_data)

            summarize_comparison(summarized_dict=compare_result)

            for feature in self.features:
                if compare_result[feature]['failed']:
                    self.failed('PTS Comparison failed')

            self.passed("Successfully compared learnt features '{f}' with "
                "'{g}'".format(f=self.features, g=self.golden_file))
        else:
            self.passed("Successfully learnt features '{f}'".format(
                    f=self.features))