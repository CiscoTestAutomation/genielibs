'''
Device class for devices with common TGN OS (ixia/spirent/agilent)
'''

# Genie Devices
import genie.libs.conf.device
import genie.libs.conf.device.cisco


class Device(genie.libs.conf.device.cisco.Device):
    '''Device class for devices with common TGN OS (ixia/spirent/agilent)'''

    '''__init__ instantiates a single connection instance.'''
    def __init__(self,
                 tgn_skip_configuration = False, 
                 tgn_enable = False,
                 tgn_traffic_convergence_threshold = 60.0, 
                 tgn_reference_rate_threshold =  100.0, 
                 tgn_first_sample_threshold = 15.0,
                 tgn_disable_traffic_post_execution =  False,
                 tgn_traffic_loss_recovery_threshold = 5.0,
                 tgn_traffic_loss_tolerance_percentage = 15.0,
                 tgn_enable_traffic_loss_check = True,
                 tgn_config_post_device_config = True,
                 tgn_profile_snapshot_threshold = 1200.0,
                 tgn_routing_threshold = 120.0,
                 tgn_port_list = '',
                 tgn_arp_wait_time=60.0,
                 tgntcl_enable_arp = False,
                 tgntcl_learn_after_n_samples = 1,
                 tgntcl_stream_sample_rate_percentage = 10.0,
                 tgntcl_wait_multiplier = 1, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.tgn_skip_configuration = tgn_skip_configuration
        self.tgn_enable = tgn_enable
        self.tgn_traffic_convergence_threshold = tgn_traffic_convergence_threshold
        self.tgn_reference_rate_threshold =  tgn_reference_rate_threshold
        self.tgn_first_sample_threshold = tgn_first_sample_threshold
        self.tgn_disable_traffic_post_execution =  tgn_disable_traffic_post_execution
        self.tgn_traffic_loss_recovery_threshold = tgn_traffic_loss_recovery_threshold
        self.tgn_traffic_loss_tolerance_percentage = tgn_traffic_loss_tolerance_percentage
        self.tgn_enable_traffic_loss_check = tgn_enable_traffic_loss_check
        self.tgn_config_post_device_config = tgn_config_post_device_config
        self.tgn_profile_snapshot_threshold = tgn_profile_snapshot_threshold
        self.tgn_routing_threshold = tgn_routing_threshold
        self.tgn_port_list = tgn_port_list
        self.tgn_arp_wait_time = tgn_arp_wait_time
        self.tgntcl_enable_arp = tgntcl_enable_arp
        self.tgntcl_learn_after_n_samples = tgntcl_learn_after_n_samples
        self.tgntcl_stream_sample_rate_percentage = tgntcl_stream_sample_rate_percentage
        self.tgntcl_wait_multiplier = tgntcl_wait_multiplier