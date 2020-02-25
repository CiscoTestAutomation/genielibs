
This example sends one raw RPC and several GET yang messages with each GET expecting a return.

To run this example on your CSR testbed with a 17.1 polaris image
=================================================================
- Edit the testbed_native_interface_oper.yaml file to match the credentials of your CSR
- Run this command in a pyATS environment (must have yang.connector installed)

    pyats run job job_native_interface_oper.py -t testbed_native_interface_oper.yaml

- You will see many missing fields and fields with bad values.  You can edit the content of data_native_interface.yaml to get passing tests.
- Edit the data_native_interface.yaml file at data:yang:content:1 with a valid NETCONF RPC for CSR to get this test to pass (the current "commit" RCP may not work)


data_native_interface.yaml data content
=======================================

data:
  variables:
    myvar: '2'

To refernce "myvar" from the test file '%{data.variables.myvar}'

data:
  yang:
    connection: yang
    protocol: netconf

To refernce "connection" from the test file '%{data.yang.connection}'
To refernce "protocol" from the test file '%{data.yang.protocol}'

and so on....


Below is an expected "return" at index 1  
----------------------------------------

- If you change "selected: false" the return field will be ignored while still keeping the data in your YAML file.

data:
  yang:
    returns:
      1:
      - id: 0
        name: name
        op: ==
        selected: true
        value: "%{ data.variables.interface_name_1 }"
        xpath: /interfaces/interface/name


Notes
=====
- This layout is just a suggestion but you may choose any layout you wish and reference the data in a way that makes sense to you.
- You can also add the data content directly to the test file without using references in an extended data file (not recommeded but good for debugging).
