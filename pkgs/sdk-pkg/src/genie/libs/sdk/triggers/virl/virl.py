'''Common implementation for VIRL triggers'''
# python import
import logging
import time

# pyats import
from pyats import aetest

# Genie
from genie.utils.timeout import Timeout
from genie.harness.base import Trigger
from genie.libs.sdk.apis.virl.std.utils import (launch_simulation,
                                                stop_simulation)
from genie.libs.sdk.apis.virl.std.get import get_simulations
from genie.libs.sdk.apis.virl.std.verify import (verify_simulation,
                                                 verify_node_state)

log = logging.getLogger(__name__)


class TriggerStopStartSimulation(Trigger):
    '''Trigger class to start/stop simulation'''

    @aetest.setup
    def get_simulations(self, uut):
        ''' Get simulations

            Args:
                 uut (`obj`): Device object

            Returns:
                 None

            Raises:
                 pyATS Results
        '''

        log.info("Getting list of simulations.")
        try:
            self.sim_list = get_simulations(uut)
            log.info("Successfully got the list of simulations: {}".format(self.sim_list))
        except Exception as e:
            raise Exception("Unable to get list of simulations.")

    @aetest.test
    def stop_simulation(self, uut, simulation_name):
        ''' Stop simulations

            Args:
                 uut (`obj`): Device object
                 simulation_name (`str`): simulation name

            Returns:
                 None

            Raises:
                 pyATS Results
        '''

        log.info("stopping simulation {}".format(simulation_name))
        try:
            result = stop_simulation(uut, simulation_name)
            if 'instead of the expected status code' not in str(result):
                log.info("Successfully stopped simulation {}".format(simulation_name))
            elif '404' in str(result):
                log.info("Simulation {} is not running. No need to stop.".format(simulation_name))
            else:
                self.failed("Failed to stop simulation {}".format(simulation_name))
            
        except Exception as e:
            self.failed("Unable to stop simulation {}: {}".format(simulation_name, e))

        # make sure the simulation is stopped
        log.info("Checking if the simulation {} is stopped".format(simulation_name))
        try:
            result = verify_simulation(uut, simulation_name, exist = False)
            if 'instead of the expected status code' not in str(result):
                log.info("Successfully verified simulation {} doesn't exist.".format(simulation_name))
            else:
                self.failed("Failed to verify if simulation {} is stopped".format(simulation_name))
            
        except Exception as e:
            self.failed("Unable to verify simulation {}: {}".format(simulation_name, e))
            
    @aetest.test
    def launch_simulation(self, uut, simulation_name, virl_file):
        ''' Launch simulation

            Args:
                 uut (`obj`): Device object
                 simulation_name (`str`): simulation name

            Returns:
                 None

            Raises:
                 pyATS Results
        '''

        log.info("Opening virl file: {}.".format(virl_file))
        try:
            with open(virl_file) as f:
                virl_data = f.read()
        except Exception as e:
            self.failed("Failed to open virl file {}: {}".format(virl_file, e))
        
        log.info("Launching simulation {}".format(simulation_name))
        try:
            result = launch_simulation(uut, simulation_name, virl_data)
            if 'instead of the expected status code' not in str(result):
                log.info("Successfully launched simulation {}".format(simulation_name))
            else:
                self.failed("Failed to launch simulation {}".format(simulation_name))
            
        except Exception as e:
            self.failed("Unable to launch simulation {}: {}".format(simulation_name, e))

        # Verify if all nodes are ACTIVE
        log.info("Getting list of all nodes on simulation {}".format(simulation_name))
        try:
            result = verify_node_state(uut, simulation_name)
            if 'instead of the expected status code' not in str(result):
                log.info("Successfully verified all nodes are ACTIVE on simulation {}".format(simulation_name))
            else:
                self.failed("Failed to verified all nodes are ACTIVE on simulation {}".format(simulation_name))
        except Exception as e:
            self.failed("Unable to verify all nodes are ACTIVE on simulation {}: {}".format(simulation_name, e))
            
        

            
