--------------------------------------------------------------------------------
                                New
--------------------------------------------------------------------------------
* MAJOR infrastructure overhaul
    * Clean stages have been converted from a function into a class which provides the following benefits:
        * **Class inheritance** - Prevents duplicated code, duplicated work, and duplicated bugs due to copy and pasting existing code to make a small modification.
        * **Tests** - With class based stages, each step in the stage is it's own method. This provides the ability to mock up and test small steps of a stage to get complete code coverage. In turn better unittest means less bugs.
        * **Execute clean stages within scripts** - Due to the redesign it is possible to execute clean stages within your scripts (Highly asked for)! In the near future we will release an easy-to-use method for calling these stages (similar to device.api).
        * **100% backwards compatible** - From a user point of view, the clean yaml file and usage is still the exact same. Nothing changes from a user point of view as we do not want to break anyone.
    * Soon to come:
        * Method to easily execute clean stages within a script
        * New developer documentation