'''
Connection Implementation for Common TGN devices
'''

# Python
import os
import logging
import time

# ATS
try:
    from pyats import tcl
except Exception:
    pass
from pyats.log.utils import banner
from pyats.connections import BaseConnection

# Genie Exceptions
from genie.harness.exceptions import GenieTgnError

# Logger
log = logging.getLogger(__name__)


class GenieTgn(BaseConnection):


    def __init__(self, *args, **kwargs):
        '''__init__ instantiates a single connection instance.'''

        # instantiate BaseConnection
        super().__init__(*args, **kwargs)

        # Default
        self._is_connected = False

        # Check for env(ENA_TESTS)
        if 'ENA_TESTS' in os.environ and os.path.isdir(os.environ['ENA_TESTS']):
            psat_tgn = os.path.join(os.environ['ENA_TESTS'], 'psat/psat_tgn.tcl')
            psat_lib = os.path.join(os.environ['ENA_TESTS'], 'psat/psat_lib.tcl')
        else:
            raise Exception("env(ENA_TESTS) not set or its path does not exist")

        # Check for required env vars
        required_env_vars = ['AUTOTEST', 'ATS_EASY', 'IXIA_HOME', 'IXIA_VERSION',
                             'IXIA_HLTAPI_LIBRARY', 'XBU_SHARED', 'TCLLIBPATH',
                             'TCL_PKG_PREFER_LATEST']
        for env_var in required_env_vars:
            if env_var not in os.environ:
                raise Exception("env({}) has not been set".format(env_var))

        # Required TCL Packages
        tcl.q.package('require', 'cAAs')
        tcl.q.package('require', 'psat-ng')
        tcl.q.package('require', 'enaTgnUtils')
        tcl.eval('namespace import -force ::enaTgnUtils::*')

        # Source PSAT lib files
        try:
            tcl.q.source(psat_tgn)
            tcl.q.source(psat_lib)
        except:
            raise Exception("Unable to source PSAT files required for TGN")

        # Get arguments from TGN testbed YAML file
        try:
            address = self.connection_info['address']
            controller = self.connection_info['controller']
            handle = self.connection_info['handle']
            tgn_type = self.connection_info['tgn_type']
        except KeyError as e:
            raise Exception('Argument not provided in TGN YAML file') from e

        # TGN configuration file
        if self.device.tgn_skip_configuration:
            self.config = ""
            session_up = True
        else:
            try:
                self.config = kwargs['config']
                session_up = False
            except:
                raise Exception("Configuration file not provided for '{d}'".format(d=self.device.name))

        # TGN port list
        if not self.device.tgn_port_list:
            try:
                port_list = self.connection_info['port_list']
            except KeyError as e:
                raise Exception("Aborting: Mandatory argument `port_list` not "
                                "found in TGN YAML file or from Genie job file "
                                "arguments.") from e
        else:
            port_list = str(self.device.tgn_port_list)

        # Genie TGN arguments
        # --------------------
        tgn_enable = int(self.device.tgn_enable) # useTGN
        tgntcl_enable_arp = int(self.device.tgntcl_enable_arp) # TGNEnableARP
        tgn_traffic_convergence_threshold = self.device.tgn_traffic_convergence_threshold # TGNWaitConvergence
        tgn_reference_rate_threshold = self.device.tgn_reference_rate_threshold # TGNMinWaitForReferenceRate
        tgn_first_sample_threshold = self.device.tgn_first_sample_threshold * 1000 # TGNWaitBeforeFirstSample
        tgntcl_learn_after_n_samples = self.device.tgntcl_learn_after_n_samples # TGNLearnExcessAfterNSamples
        tgn_disable_traffic_post_execution = int(self.device.tgn_disable_traffic_post_execution) # TGNStopTraffic
        tgn_traffic_loss_recovery_threshold = self.device.tgn_traffic_loss_recovery_threshold * 1000 # TGNWaitTimeNoTrafficMs
        tgn_traffic_loss_tolerance_percentage = self.device.tgn_traffic_loss_tolerance_percentage # trafficLossPercentageTolerance
        tgn_enable_traffic_loss_check = int(self.device.tgn_enable_traffic_loss_check) # checkTrafficLoss
        tgntcl_stream_sample_rate_percentage = self.device.tgntcl_stream_sample_rate_percentage # TGNThreshold
        tgntcl_wait_multiplier = self.device.tgntcl_wait_multiplier # TGNWaitMultiplier
        tgn_config_post_device_config = int(self.device.tgn_config_post_device_config) # loadTGNAfterRouterConfig
        tgn_profile_snapshot_threshold = int(self.device.tgn_profile_snapshot_threshold) # TGNWaitForRefRateMinutes
        tgn_routing_threshold = self.device.tgn_routing_threshold # waitAfterTGNRouting
        self.tgn_arp_wait_time = int(self.device.tgn_arp_wait_time)

        # Set user configured values
        # --------------------------
        tcl.q.set('test_params(useTGN)', tgn_enable)
        tcl.q.set('test_params(TGNEnableARP)', tgntcl_enable_arp)
        tcl.q.set('test_params(loadTGNAfterRouterConfig)', tgn_config_post_device_config)
        tcl.q.set('test_params(waitAfterTGNRouting)', tgn_routing_threshold)
        tcl.q.set('test_params(TGNWaitConvergence)', tgn_traffic_convergence_threshold)
        tcl.q.set('test_params(TGNWaitTimeNoTrafficMs)', tgn_traffic_loss_recovery_threshold)
        tcl.q.set('test_params(TGNWaitForRefRateMinutes)', tgn_profile_snapshot_threshold)
        tcl.q.set('test_params(TGNWaitBeforeFirstSample)', tgn_first_sample_threshold)
        tcl.q.set('test_params(TGNMinWaitForReferenceRate)', tgn_reference_rate_threshold)
        tcl.q.set('test_params(TGNThreshold)', tgntcl_stream_sample_rate_percentage)
        tcl.q.set('test_params(checkTrafficLoss)', tgn_enable_traffic_loss_check)
        tcl.q.set('test_params(trafficLossPercentageTolerance)', tgn_traffic_loss_tolerance_percentage)
        tcl.q.set('test_params(TGNStopTraffic)', tgn_disable_traffic_post_execution)
        tcl.q.set('test_params(TGNLearnExcessAfterNSamples)', tgntcl_learn_after_n_samples)
        tcl.q.set('test_params(TGNWaitMultiplier)', tgntcl_wait_multiplier)

        # Set default values
        # ------------------
        tcl.q.set('test_params(TGNWaitInterval)', 1)
        tcl.q.set('test_params(TGNReportWorstStreams)', 0)
        tcl.q.set('test_params(TGNFeaturePatternMatch)', '{}')
        tcl.q.set('test_params(TGNretries)', 10)
        tcl.q.set('test_params(TGNarpTimeout)', 0)
        tcl.q.set('test_params(TGNarpInterval)', 0)
        tcl.q.set('test_params(TGNfIndex)', 0)
        tcl.q.set('test_params(TGNiIndex)', 1)
        tcl.q.set('test_params(TGNeIndex)', 2)
        tcl.q.set('test_params(TGNtIndex)', 3)
        tcl.q.set('test_params(TGNStatisticsSet)', '')
        tcl.q.set('test_params(TGNPortStatisticsSet)', '')

        # Build TGN_KEY structure for TCL procs
        # -------------------------------------
        tcl.q.keylset('test_params(TGN_KEY)', 'Session1.Address', address)
        tcl.q.keylset('test_params(TGN_KEY)', 'Session1.Controller', controller)
        tcl.q.keylset('test_params(TGN_KEY)', 'Session1.Handle', handle)
        tcl.q.keylset('test_params(TGN_KEY)', 'Session1.portList', port_list)
        tcl.q.keylset('test_params(TGN_KEY)', 'Session1.Type', tgn_type)
        tcl.q.keylset('test_params(TGN_KEY)', 'Session1.SessionFile', self.config)
        tcl.q.keylset('test_params(TGN_KEY)', 'Session1.SessionAlreadyUp', session_up)
        tcl.q.keylset('test_params(TGN_KEY)', 'Session1.SessionLabel', tgn_type)


    @property
    def connected(self):
        '''Check if device is connected'''
        return self._is_connected

    def connect(self):
        '''Connect to TGN device'''

        # Already connected do nothing
        if self.connected:
            return

        # Connect to TGN & load configuration
        # expect1.1> LoadTGN
        result = tcl.eval('LoadTGN')

        # Check connected & config loaded
        if result == '1':
            self._is_connected = True
            log.info("Connected successfully to device '{}'".format(self.device.name))
        else:
            self._is_connected = False
            raise GenieTgnError("Unable to connect to device '{}'".format(self.device.name))


    def learn_traffic_streams(self):

        # Learn traffic
        # expect1.1> LearnTGN
        result = tcl.eval('LearnTGN')

        # Process result
        if result == '1':
            log.info("Successfully learned traffic streams on device '{}'".format(self.device.name))
        else:
            raise GenieTgnError("Unable to learn traffic streams on device '{}'".format(self.device.name))


    def start_routing(self):

        # Start routing
        # expect1.1> TGNRouting
        result = tcl.eval('TGNRouting')

        # Process result
        if result == '1':
            log.info("Successfully started routing on device '{}'".format(self.device.name))
        else:
            raise GenieTgnError("Failed to start routing on device '{}'".format(self.device.name))


    def initialize_tgn_ArpNdPim(self):

        # Send arp on interface
        # expect1.1> TGNSendArpOnInterface
        self.send_arp_on_interface()

        # Sleep for wait_time seconds
        log.info('Sleeping for {} seconds after sending ARP on interfaces'.\
                    format(self.tgn_arp_wait_time))
        time.sleep(self.tgn_arp_wait_time)

        # Initialize TGN
        # expect1.1> initializeTGN
        result = tcl.eval('initializeTGN')

        # Process result
        if result == '1':
            log.info("Successfully initialized TGN device '{}'".format(self.device.name))
        else:
            raise GenieTgnError("Unable to initialize TGN device '{}'".format(self.device.name))


    def start_traffic(self):

        # Start traffic
        # expect1.1> TGNTraffic
        result = tcl.eval('TGNTraffic')

        # Process result
        if result == '1':
            log.info("Successfully started traffic on device '{}'".format(self.device.name))
        else:
            raise GenieTgnError("Failed to start traffic on device '{}'".format(self.device.name))


    def stop_traffic(self):

        # Stop traffic
        # expect1.1> TGNTraffic -stop
        result = tcl.eval('TGNTraffic -stop')

        # Process result
        if result == '1':
            log.info("Successfully stopped traffic on device '{}'".format(self.device.name))
        else:
            raise GenieTgnError("Unable to stop traffic on device '{}'".format(self.device.name))


    def get_current_packet_rate(self, first_sample=False):

        # Get the current packet rate
        # expect1.1> TGNGetCurrentPacketRate -array test_params
        result = tcl.eval('TGNGetCurrentPacketRate -array test_params')

        # Process result
        if result == '1':
            log.info("Successfully got current packet rate on device '{}'".format(self.device.name))

            # If this was the first sample of rates, save the timestamp
            if first_sample:
                fs_timestamp = tcl.eval('clock seconds')
                tcl.q.set('test_params(TGN,FirstRateSampleTimeStamp)', fs_timestamp)
        else:
            raise GenieTgnError("Unable to get current packet rate on device '{}'".format(self.device.name))


    def get_reference_packet_rate(self):

        # Get the referecne packet rate
        # expect1.1> TGNGetReferencePacketRate -maxMinutes $test_params(TGNWaitForRefRateMinutes)
        result = tcl.eval('TGNGetReferencePacketRate -maxMinutes $test_params(TGNWaitForRefRateMinutes)')

        # Process result
        if result == '1':
            log.info("Successfully got reference packet rate on device '{}'".format(self.device.name))
        else:
            raise GenieTgnError("Unable to get reference packet rate on device '{}'".format(self.device.name))


    def check_traffic_loss(self):

        # Connect to TGN & load configuration
        # expect1.1> TGNCheckTrafficLossPercent
        result = tcl.eval('TGNCheckTrafficLossPercent')

        # Process result
        if result == '1':
            log.info("Successfully checked traffic loss on device '{}'".format(self.device.name))
        else:
            raise GenieTgnError("Unable to check traffic loss on device '{}'".format(self.device.name))


    def calculate_absolute_outage(self, max_outage_ms=5):

        # Convert from seconds to milliseconds for PSAT TGN
        max_outage_ms = (max_outage_ms * 1000)

        # Calculate traffic outage
        # expect1.1> TGNCalculateAbsoluteOutage -maxOutageMs $maxOutageInMs
        result = tcl.eval('TGNCalculateAbsoluteOutage -maxOutageMs {}'.\
                          format(max_outage_ms))

        # Process result
        if result != '1':
            raise GenieTgnError("Traffic failure observed on device '{}'".\
                                format(self.device.name))


    def poll_traffic_until_traffic_resumes(self, timeout=60, delay_check_traffic=10):

        # 'timeout' value in seconds [default 60 seconds]
        # 'delay' value in seconds [default 10 seconds]

        # Convert from seconds to milliseconds for PSAT TGN
        delay_check_traffic = delay_check_traffic * 1000

        # expect1.1> TGNPollUntilTrafficResumes -timeout $maxOutageTime -delayCheckTraffic $delayCheckTraffic
        result = tcl.eval('TGNPollUntilTrafficResumes -timeout {timeout}'
                          ' -delayCheckTraffic {delay}'.\
                          format(timeout=timeout, delay=delay_check_traffic))

        # Process result
        if result != '1':
            raise GenieTgnError("Traffic failure observed on device '{}'".\
                                format(self.device.name))


    def clear_stats(self):

        # Clear TGN statistics
        # expect1.1> TGNClearAllStats
        result = tcl.eval('TGNClearAllStats')

        # Process result
        if result == '1':
            log.info("Successfully cleared statistics on device '{}'".format(self.device.name))
        else:
            raise GenieTgnError("Unable to clear statistics device on '{}'".format(self.device.name))


    def send_arp_on_interface(self):

        # Send ARP on interface
        # expect1.1> TGNSendArpOnInterface
        result = tcl.eval('::psat-ng::TGNSendArpOnInterface')

        # Process result
        if result == '1':
            log.info("Successfully sent ARP on interface on TGN device '{}'".format(self.device.name))
        else:
            raise GenieTgnError("Unable to send ARP on interface on TGN device '{}'".format(self.device.name))
