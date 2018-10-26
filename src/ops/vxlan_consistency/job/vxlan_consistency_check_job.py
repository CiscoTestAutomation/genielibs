# To run the job:
# easypy vxlan_consistency_check_job.py -testbed_file <testbed_file.yaml> 
# Description: This job file shows the Genie Vxlan Consistency checker. 

import os
from ats.easypy import run

# All run() must be inside a main function
def main():
    # Find the location of the script in relation to the job file
    test_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    testscript = os.path.join('vxlan_consistency_check_script.py')

    # Execute the testscript
    run(testscript=testscript)
