########################################################
# To run the job:
# easypy path/to/my/job/file/myjob.py \
#        -testbed_file path/to/my/yaml/file/myyaml.yaml
########################################################
from genie.harness.main import gRun

# testbed_file: testbed_native_interface_oper.yaml


def main(*args, **kwargs):
    # cleanup section calls this also so make sure we have args.
    if not args:
        return

    trigger_uids, trigger_datafile = args

    gRun(trigger_uids=trigger_uids,
         trigger_datafile=trigger_datafile,
         mapping_datafile="mapping_datafile.yaml",
         subsection_datafile="subsection_datafile.yaml")


preconfig = []
native_interface_00001_interfaces_interface = [
    'native_interface_00001_interfaces_interface_state',
]
native_interface_00010_interfaces_interface_statistics = [
    'native_interface_00010_interfaces_interface_statistics_state',
]
native_interface_00030_interfaces_interface_diffserv_info = [
    'native_interface_00030_interfaces_interface_diffserv_info_state',
]
native_interface_00031_diffserv_target_classifier_stats = [
    'native_interface_00031_diffserv_target_classifier_stats_state',
]
native_interface_00032_classifier_entry_stats = [
    'native_interface_00032_classifier_entry_stats_state',
]
native_interface_00035_meter_stats = [
    'native_interface_00035_meter_stats_state',
]
native_interface_00040_queuing_stats = [
    'native_interface_00040_queuing_stats_state',
]
native_interface_00046_queuing_stats_wred_stats = [
    'native_interface_00046_queuing_stats_wred_stats_state',
]
native_interface_00058_queuing_stats_cac_stats = [
    'native_interface_00058_queuing_stats_cac_stats_state',
]
native_interface_00060_subclass_list = [
    'native_interface_00060_subclass_list_state',
]
native_interface_00061_subclass_list_cos_counters = [
    'native_interface_00061_subclass_list_cos_counters_state',
]
native_interface_00068_subclass_list_cos_default = [
    'native_interface_00068_subclass_list_cos_default_state',
]
native_interface_00074_subclass_list_dscp_counters = [
    'native_interface_00074_subclass_list_dscp_counters_state',
]
native_interface_00081_subclass_list_dscp_default = [
    'native_interface_00081_subclass_list_dscp_default_state',
]
native_interface_00087_subclass_list_discard_class_counters = [
    'native_interface_00087_subclass_list_discard_class_counters_state',
]
native_interface_00094_subclass_list_disc_class_default = [
    'native_interface_00094_subclass_list_disc_class_default_state',
]
native_interface_00100_subclass_list_precedence_counters = [
    'native_interface_00100_subclass_list_precedence_counters_state',
]
native_interface_00107_subclass_list_prec_default = [
    'native_interface_00107_subclass_list_prec_default_state',
]
native_interface_00113_subclass_list_mpls_exp_counters = [
    'native_interface_00113_subclass_list_mpls_exp_counters_state',
]
native_interface_00120_subclass_list_mpls_exp_default = [
    'native_interface_00120_subclass_list_mpls_exp_default_state',
]
native_interface_00126_subclass_list_dei_counters = [
    'native_interface_00126_subclass_list_dei_counters_state',
]
native_interface_00133_subclass_list_dei_counts_default = [
    'native_interface_00133_subclass_list_dei_counts_default_state',
]
native_interface_00139_subclass_list_clp_counters = [
    'native_interface_00139_subclass_list_clp_counters_state',
]
native_interface_00146_subclass_list_clp_default = [
    'native_interface_00146_subclass_list_clp_default_state',
]
native_interface_00152_marking_stats_marking_dscp_stats_val = [
    'native_interface_00152_marking_stats_marking_dscp_stats_val_state',
]
native_interface_00154_marking_dscp_tunnel_stats_val = [
    'native_interface_00154_marking_dscp_tunnel_stats_val_state',
]
native_interface_00156_marking_stats_marking_cos_stats_val = [
    'native_interface_00156_marking_stats_marking_cos_stats_val_state',
]
native_interface_00158_marking_cos_inner_stats_val = [
    'native_interface_00158_marking_cos_inner_stats_val_state',
]
native_interface_00160_marking_discard_class_stats_val = [
    'native_interface_00160_marking_discard_class_stats_val_state',
]
native_interface_00162_marking_qos_grp_stats_val = [
    'native_interface_00162_marking_qos_grp_stats_val_state',
]
native_interface_00164_marking_stats_marking_prec_stats_val = [
    'native_interface_00164_marking_stats_marking_prec_stats_val_state',
]
native_interface_00166_marking_prec_tunnel_stats_val = [
    'native_interface_00166_marking_prec_tunnel_stats_val_state',
]
native_interface_00168_marking_mpls_exp_imp_stats_val = [
    'native_interface_00168_marking_mpls_exp_imp_stats_val_state',
]
native_interface_00170_marking_mpls_exp_top_stats_val = [
    'native_interface_00170_marking_mpls_exp_top_stats_val_state',
]
native_interface_00172_marking_fr_de_stats_val = [
    'native_interface_00172_marking_fr_de_stats_val_state',
]
native_interface_00174_marking_fr_fecn_becn_stats_val = [
    'native_interface_00174_marking_fr_fecn_becn_stats_val_state',
]
native_interface_00176_marking_atm_clp_stats_val = [
    'native_interface_00176_marking_atm_clp_stats_val_state',
]
native_interface_00178_marking_vlan_inner_stats_val = [
    'native_interface_00178_marking_vlan_inner_stats_val_state',
]
native_interface_00180_marking_stats_marking_dei_stats_val = [
    'native_interface_00180_marking_stats_marking_dei_stats_val_state',
]
native_interface_00182_marking_dei_imp_stats_val = [
    'native_interface_00182_marking_dei_imp_stats_val_state',
]
native_interface_00184_marking_srp_priority_stats_val = [
    'native_interface_00184_marking_srp_priority_stats_val_state',
]
native_interface_00186_marking_wlan_user_priority_stats_val = [
    'native_interface_00186_marking_wlan_user_priority_stats_val_state',
]
native_interface_00188_diffserv_info_priority_oper_list = [
    'native_interface_00188_diffserv_info_priority_oper_list_state',
]
native_interface_00189_agg_priority_stats = [
    'native_interface_00189_agg_priority_stats_state',
]
native_interface_00197_qlimit_default_thresh = [
    'native_interface_00197_qlimit_default_thresh_state',
]
native_interface_00203_qlimit_cos_thresh_list = [
    'native_interface_00203_qlimit_cos_thresh_list_state',
]
native_interface_00210_qlimit_disc_class_thresh_list = [
    'native_interface_00210_qlimit_disc_class_thresh_list_state',
]
native_interface_00217_qlimit_qos_grp_thresh_list = [
    'native_interface_00217_qlimit_qos_grp_thresh_list_state',
]
native_interface_00224_qlimit_mpls_exp_thresh_list = [
    'native_interface_00224_qlimit_mpls_exp_thresh_list_state',
]
native_interface_00231_qlimit_dscp_thresh_list = [
    'native_interface_00231_qlimit_dscp_thresh_list_state',
]
native_interface_00245_interfaces_interface_v4_protocol_stats = [
    'native_interface_00245_interfaces_interface_v4_protocol_stats_state',
]
native_interface_00257_interfaces_interface_v6_protocol_stats = [
    'native_interface_00257_interfaces_interface_v6_protocol_stats_state',
]
native_interface_00271_interface_lag_aggregate_state = [
    'native_interface_00271_interface_lag_aggregate_state_state',
]
native_interface_00278_interfaces_interface_ether_state = [
    'native_interface_00278_interfaces_interface_ether_state_state',
]
native_interface_00283_interfaces_interface_ether_stats = [
    'native_interface_00283_interfaces_interface_ether_stats_state',
]
native_interface_00293_interface_ether_stats_dot3_counters = [
    'native_interface_00293_interface_ether_stats_dot3_counters_state',
]
native_interface_00294_dot3_counters_dot3_error_counters_v2 = [
    'native_interface_00294_dot3_counters_dot3_error_counters_v2_state',
]
native_interface_00316_interfaces_interface_serial_state = [
    'native_interface_00316_interfaces_interface_serial_state_state',
]
native_interface_00321_interfaces_interface_serial_stats = [
    'native_interface_00321_interfaces_interface_serial_stats_state',
]
native_interface_00323_interfaces_interface_syncserial_state = [
    'native_interface_00323_interfaces_interface_syncserial_state_state',
]
native_interface_00335_syncserial_state_dce_mode_state = [
    'native_interface_00335_syncserial_state_dce_mode_state_state',
]
native_interface_00338_syncserial_state_dte_mode_state = [
    'native_interface_00338_syncserial_state_dte_mode_state_state',
]
postconfig = []

test_profile = preconfig
test_profile += native_interface_00001_interfaces_interface
test_profile += native_interface_00010_interfaces_interface_statistics
test_profile += native_interface_00030_interfaces_interface_diffserv_info
test_profile += native_interface_00031_diffserv_target_classifier_stats
test_profile += native_interface_00032_classifier_entry_stats
test_profile += native_interface_00035_meter_stats
test_profile += native_interface_00040_queuing_stats
test_profile += native_interface_00046_queuing_stats_wred_stats
test_profile += native_interface_00058_queuing_stats_cac_stats
test_profile += native_interface_00060_subclass_list
test_profile += native_interface_00061_subclass_list_cos_counters
test_profile += native_interface_00068_subclass_list_cos_default
test_profile += native_interface_00074_subclass_list_dscp_counters
test_profile += native_interface_00081_subclass_list_dscp_default
test_profile += native_interface_00087_subclass_list_discard_class_counters
test_profile += native_interface_00094_subclass_list_disc_class_default
test_profile += native_interface_00100_subclass_list_precedence_counters
test_profile += native_interface_00107_subclass_list_prec_default
test_profile += native_interface_00113_subclass_list_mpls_exp_counters
test_profile += native_interface_00120_subclass_list_mpls_exp_default
test_profile += native_interface_00126_subclass_list_dei_counters
test_profile += native_interface_00133_subclass_list_dei_counts_default
test_profile += native_interface_00139_subclass_list_clp_counters
test_profile += native_interface_00146_subclass_list_clp_default
test_profile += native_interface_00152_marking_stats_marking_dscp_stats_val
test_profile += native_interface_00154_marking_dscp_tunnel_stats_val
test_profile += native_interface_00156_marking_stats_marking_cos_stats_val
test_profile += native_interface_00158_marking_cos_inner_stats_val
test_profile += native_interface_00160_marking_discard_class_stats_val
test_profile += native_interface_00162_marking_qos_grp_stats_val
test_profile += native_interface_00164_marking_stats_marking_prec_stats_val
test_profile += native_interface_00166_marking_prec_tunnel_stats_val
test_profile += native_interface_00168_marking_mpls_exp_imp_stats_val
test_profile += native_interface_00170_marking_mpls_exp_top_stats_val
test_profile += native_interface_00172_marking_fr_de_stats_val
test_profile += native_interface_00174_marking_fr_fecn_becn_stats_val
test_profile += native_interface_00176_marking_atm_clp_stats_val
test_profile += native_interface_00178_marking_vlan_inner_stats_val
test_profile += native_interface_00180_marking_stats_marking_dei_stats_val
test_profile += native_interface_00182_marking_dei_imp_stats_val
test_profile += native_interface_00184_marking_srp_priority_stats_val
test_profile += native_interface_00186_marking_wlan_user_priority_stats_val
test_profile += native_interface_00188_diffserv_info_priority_oper_list
test_profile += native_interface_00189_agg_priority_stats
test_profile += native_interface_00197_qlimit_default_thresh
test_profile += native_interface_00203_qlimit_cos_thresh_list
test_profile += native_interface_00210_qlimit_disc_class_thresh_list
test_profile += native_interface_00217_qlimit_qos_grp_thresh_list
test_profile += native_interface_00224_qlimit_mpls_exp_thresh_list
test_profile += native_interface_00231_qlimit_dscp_thresh_list
test_profile += native_interface_00245_interfaces_interface_v4_protocol_stats
test_profile += native_interface_00257_interfaces_interface_v6_protocol_stats
test_profile += native_interface_00271_interface_lag_aggregate_state
test_profile += native_interface_00278_interfaces_interface_ether_state
test_profile += native_interface_00283_interfaces_interface_ether_stats
test_profile += native_interface_00293_interface_ether_stats_dot3_counters
test_profile += native_interface_00294_dot3_counters_dot3_error_counters_v2
test_profile += native_interface_00316_interfaces_interface_serial_state
test_profile += native_interface_00321_interfaces_interface_serial_stats
test_profile += native_interface_00323_interfaces_interface_syncserial_state
test_profile += native_interface_00335_syncserial_state_dce_mode_state
test_profile += native_interface_00338_syncserial_state_dte_mode_state
test_profile += postconfig


main(test_profile, "native_interface.yaml")
