########################################################
# To run the job:
# easypy path/to/my/job/file/myjob.py \
#        -testbed_file path/to/my/yaml/file/myyaml.yaml
########################################################
from genie.harness.main import gRun

# testbed_file: testbed_native_test.yaml


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
native_nexus_get = [
    'native_get'
]
native_iosxe_get = [
    'native_iosxe_get'
]
native_nexus_capabilities = [
    'native_nxos_capabilities'
]
native_iosxe_capabilities = [
    'native_iosxe_capabilities'
]
native_nexus_set = [
    'native_set'
]
native_nexus_telemetry = [
    'native_telemetry',
]
native_iosxe_telemetry = [
    'native_iosxe_telemetry',
]
postconfig = []

test_profile = preconfig
test_profile += native_nexus_set
#test_profile += native_nexus_get
#test_profile += native_iosxe_get
#test_profile += native_nexus_capabilities
#test_profile += native_iosxe_capabilities
#test_profile += native_nexus_telemetry
#test_profile += native_iosxe_telemetry
test_profile += postconfig

#test_profile = ['test_no_value']

main(test_profile, "native_test.yaml")
