########################################################
# To run the job:
# pyats run job  path/to/my/job/file/myjob.py \
#        -testbed_file path/to/my/yaml/file/myyaml.yaml
########################################################
from genie.harness.main import gRun


def main():
    trigger_uids = [
        'native_oper_interface_statistics_get',
        'openconfig_gnmi_fan_statistics_subscribe',
        'native_netconf_cpu_statistics_subscribe',
        'nexus_openconfig_gnmi_fan_statistics_subscribe',
        'nexus_netconf_interface_state_subscribe',
    ]

    gRun(trigger_uids=trigger_uids,
         trigger_datafile="test_trigger.yaml",
         mapping_datafile="mapping.yaml",
         subsection_datafile="subsection.yaml")


if __name__ == '__main__':
    main()
