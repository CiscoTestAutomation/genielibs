# Coding Guidelines

*Share-ability, Object Oriented Programming, re-usability.*

Genie promotes the idea of reusability that's why we came up with the below
guideline to get standarized shareable/reusable libraries that everyone
understand and benefit from.

# Documentation

Documentation is part of the development. All code must be commented to help the
reader. All new features and enhancements to any feature should also modify the
main documentation.

# Triggers

* A Trigger is an aetest testcase. A testcase can be divided in multiple test
sections. Using test section is very good idea! Using multiple test sections
means that your trigger can be inherited, and specific test section that needs
to be changed, modified  with every other test section remaining status quo. 
__Note:__  Every action of the trigger should be its own test section this
includes any checking (which does not equal to local verification) that should
be done before or after the trigger.

* In Triggers where device configuration must be sent to the device, using Genie
__Conf__ object as it makes it OS and Interface management agnostic.

* For checks in the Trigger, use Genie __OPS__, as it makes it OS and Interface
management agnostic. Make sure to pass attributes when calling OPS to learn
what specifically is needed to reduce run time.

* For objects that is needed to be used throughout/later - make sure to use
__self__ to pass the object.

* The Template directory contains all the base triggers - make sure to create
template for any trigger that does not have the base template and place it
under genielibs/src/sdk/triggers/template/ directory.  

# Verifications

* Verification is simple, just create a parser or an Ops object, and link it in
the verifications file.

* Make sure to evaluate [ParserGen] for your parser! It could save you hours.

[ParserGen]: https://pubhub.devnetcloud.com/media/pyats-packages/docs/parsergen/index.html

* Before writing a parser make sure to check if one already exists.

# Generic Libraries

Library APIs must be generic, with parameters that dictates its flow. 

Make sure to group the APIs into classification and create respective library file
for each classification.

Let's say you are writing a trigger called : UnconfigConfigOspf. This trigger
requires to save the configuration before removing Ospf, and then re-applying it.
We could copy paste some code to do the action, or we could use a Tftp object,
which has some functionality to copy a file to a device, and copy a
configuration from the device to a linux server. Its easy to imagine that a
lot of other people requires the same. Why don't we take this Tftp library and
share it with other script developer?

This can be done via a pypi packages, or something similar. For this to be
doable, when developing the Tftp class, we must make it independent of Genie,
and receive everything as argument. [GenieFileTransferUtilsLibs] pypi package
has been implemenetd for that purpose.

[GenieFileTransferUtilsLibs]: https://pubhub.devnetcloud.com/media/pyats-packages/docs/geniefiletransferutilslibs/index.html#

This is something to keep in mind for all triggers. Think broader than just
this trigger,  let's make it useful for everybody

# Headers

All headers must follow the following [Google Style] docstring.

[Google Style]: http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

__Header example__
```
'''Some text explaining what this module is about'''
  
class MySample(object):
    '''MySample class example
  
    Explains what the libraries class do in as much details
    it requires.
  
    If there is a __init__, it is also documented here.
    '''
     
    def my_func(self, attr1, attr2=None):
        '''1 Liner explaining what it does
  
        More in details explanation of what this function does.
        In the case of triggers, the steps should be here.
       
        Args:
            attr1 (`str`): The first parameter.
            attr2 (`str`, optional): The second parameter. Defaults to None.
                Second line of description should be indented.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
 
        Returns:
            bool: True if successful, False otherwise.
 
        Raises:
            AttributeError: The ``Raises`` section is a list of all exceptions
                that are relevant to the interface.
            ValueError: If `param2` is equal to `param1`.
  
        Example:
            Examples should be written in doctest format, and should illustrate how
            to use the function.
 
            >>>  my = MySample()
            >>> print(my.my_func(5)
            5
        '''
    # Then your code
    return attr1
```

In the case of trigger, *Example* is optional.
