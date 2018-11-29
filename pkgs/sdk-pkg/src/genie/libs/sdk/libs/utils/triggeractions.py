'''This is file contains validation functions for
   trigger actions, it could be used in all platforms'''

# Python
import logging
import time

# import ats
from ats.utils.objects import find, R

log = logging.getLogger(__name__)


class CompareUptime(object):

    @classmethod
    def compare_uptime(cls, ops, threshold_time, r_obj, relation='<'):
        ''' Compare the uptime from the Ops object to an expected_time

            Args:
              Mandatory:
                ops (`obj`) : Learnt ops object.
                threshold_time (`int`) : Uptime vallue want to compare.
                r_obj (`list`) : List of ats.utils.objects.R objects which
                                 contains the keys structure of desired
                                 information for find function.
              Optional:
                relation (`str`) : Relation between the uptime and
                                   threshold_time.
                                   support '<' '>' '<=' '>='

            Returns:
                None

            Raises:
                Exception : uptime is not reset as expected
                Error: control_index does not have valid value when
                       extra_control_r is defined

            Example:
                >>> compare_uptime(bgp = <bgp_ops_obj>, threshold_time = 20,
                      relation = '<', attr='info',
                      r_obj=R(['instance',
                        '(.*)', 'vrf', '(.*)','neighbor', '(.*)',
                        'up_time', '(.*)'])))
        '''
        # find required info from ops obj
        uptime_ret = find([ops], *r_obj, filter_=False)

        # Compare uptime
        for items in uptime_ret:
            # get uptime from find result
            uptime = items[0]

            log.info('Check - {n}: {t} {r} {tt}s'
                     .format(n=items[1][1:], t=uptime, r=relation,
                            tt=threshold_time))

            if 'never' in uptime:
                raise Exception('Fail - {n}: {t} is not {r} {tt}s'
                                .format(n=items[1][1:], t=uptime, r=relation,
                                        tt=threshold_time))

            if uptime and ':' in uptime:
                t = uptime.split(':')
                time = int(t[0]) * 3600 + int(t[1]) * 60 + int(t[2])
            elif uptime and 'd' in uptime:
                t = uptime.split('d')
                try:
                    time = int(t[0]) * 3600 * 24
                except:
                    raise Exception('Fail - {n}: {t}s is not {r} {tt}s'
                                    .format(n=items[1][1:], t=uptime, r=relation,
                                            tt=threshold_time))                   
            elif uptime:
                try:
                    time = float(uptime)
                except:
                    raise Exception('Fail - {n}: {t}s is not {r} {tt}s'
                                    .format(n=items[1][1:], t=uptime, r=relation,
                                            tt=threshold_time))
            else:
                raise Exception('Cannot get uptime for neighbor {}'
                                .format(nei))

            result = {'>': time > threshold_time,
                      '<': time < threshold_time,
                      '==': time == threshold_time,
                      '<=': time <= threshold_time,
                      '>=': time >= threshold_time}[relation]
            if not result:
                raise Exception('Fail - {n}: {t}s is not {r} {tt}s'
                                .format(n=items[1][1:],
                  r=relation, t=uptime, tt=threshold_time))


class CheckFeatureStatus(object):
    '''Trigger class for DisableEnable action'''

    @classmethod
    def check_feature_status(cls, device, expect, feature_name, abstract,
                             attempt=3, sleep=5):
        ''' Check if the feature is disabled/enabled

            Args:
                device (`obj`): Device Object.
                abstract (`obj`): Abstract Lookup Object.
                expect (`str`): Feature status.
                                Only accept 'disabled' and 'enabled'
                feature_name (`str`): Feature namne.
                sleep_time (`int`): The sleep time.
                attempt (`int`): Attempt numbers when learn the feature.

            Returns:
                None

            Raises:
                AssertionError: 'expect' is not 'disabled' or 'enabled'
                                Or the status is not same as expect value 
                SyntaxError: Cannot parse show feature output

            Example:
                >>> check_feature_status(device=uut, expect='disabled',
                                         feature_name='bgp',abstract=abstract)
        '''
        assert expect in ['disabled', 'enabled']

        for i in range(attempt):
                try:
                    ret = abstract.parser.show_feature.ShowFeature(device=device)
                    ret = ret.parse()
                except Exception as e:
                    raise SyntaxError("Cannot parse command 'show "
                                      "feature'") from e

                ret = find([ret], R(['feature', feature_name, 'instance',
                                     '(.*)', 'state', expect]), filter_=False)
                if ret:
                    break
                time.sleep(sleep)
        else:
            raise AssertionError('{n} is failed to {s}'
                                 .format(n=feature_name, s=expect))


class Configure(object):
    '''Config functions for doing specific configurations'''

    @classmethod
    def conf_configure(self, device, conf,
                       conf_structure, unconfig=False, _first=True):
        '''Configure device via conf object'''

        # Build the conf object
        if _first:
            # In case of interface conf, we can't add it as a feature to
            # the device.
            if 'interface' not in conf.__class__.__name__.lower():
                device.add_feature(conf)

        self._set_conf_attribute(conf, conf_structure)

        if _first:
            if unconfig:
                # Could be done in the above for loop, but I believe it would
                # be a waste of time for most scenario. So only build it if
                # unconfig.
                # I think this should always be sent.
                attributes = self._build_attribute(conf_structure)
                conf.build_unconfig(attributes=attributes)
            else:
                conf.build_config()

    @classmethod
    def _set_conf_attribute(self, conf, conf_structure, return_attr=False):
        returned_attr = None
        for structure in conf_structure:
            if len(structure) == 2:
                # Then its value
                try:
                    setattr(conf, structure[0], structure[1])
                except AttributeError:
                    getattr(conf, structure[0])[structure[1]]
                    if return_attr:
                        return getattr(conf, structure[0])[structure[1]]
                except ValueError as e:
                    if 'int' in str(e):
                        setattr(conf, structure[0], int(structure[1]))
            else:
                item = structure[0]
                try:
                    c_item = getattr(conf, structure[0])
                except (AttributeError, TypeError):
                    c_item = conf[structure[0]]
                returned_attr=self._set_conf_attribute(c_item,
                                         conf_structure=[structure[1:]],
                                         return_attr=return_attr)
        if return_attr:
            return returned_attr

    @classmethod
    def _build_attribute(self, structures):
        attributes = {}
        for structure in structures:
            level = attributes
            for item in structure[:-1]:
                if item not in level:
                    level[item] = {}
                level = level[item]
            # Set last item
            level[structure[-1]] = None

        # attributes should be None when nothing in structures
        # this is conf object standard
        return None if not attributes else attributes


class CompareCounters(object):

    @classmethod
    def compare_counter(cls, ops, threshold_counter, r_obj, relation='<'):
        ''' Compare the counters from the Ops object to an threshold_counter

            Args:
              Mandatory:
                ops (`obj`) : Learnt ops object.
                threshold_counter (`int`) : Counter vallue want to compare.
                r_obj (`list`) : List of ats.utils.objects.R objects which
                                 contains the keys structure of desired
                                 information for find function.
              Optional:
                relation (`str`) : Relation between the uptime and
                                   threshold_time.
                                   support '<' '>' '<=' '>='

            Returns:
                None

            Raises:
                Exception : uptime is not reset as expected
                Error: control_index does not have valid value when
                       extra_control_r is defined

            Example:
                >>> compare_counter(bgp = <bgp_ops_obj>, threshold_counter = 20,
                      relation = '<', 
                      r_obj=R(['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                 '(?P<peer>.*)', 'statistics', 'sa_policy',
                                 'out', '(?P<sa_filter_out>.*)', '(?P<match>.*)',
                                 'num_of_comparison', '(.*)'])))
        '''
        # find required info from ops obj
        counters = find([ops], *r_obj, filter_=False)

        if not counters:
            raise Exception('No required counters are found. '
                'Required: \n{}'.format([r.args for r in r_obj]))

        # Compare counter
        for items in counters:
            # get counter from find result
            counter = items[0]
            if counter == 0 and threshold_counter == 0:
                relation = list(relation)[0] + '='

            log.info('Check - {n}: {t} {r} {tt}'
                     .format(n=items[1][1:], t=counter, r=relation,
                            tt=threshold_counter))

            result = {'>': counter > threshold_counter,
                      '<': counter < threshold_counter,
                      '==': counter == threshold_counter,
                      '<=': counter <= threshold_counter,
                      '>=': counter >= threshold_counter}[relation]
            if not result:
                raise Exception('Fail - {n}: {t}s is not {r} {tt}s'
                                .format(n=items[1][1:],
                  r=relation, t=counter, tt=threshold_counter))


def configure_add_attributes(add_obj, base, add_attribute, add_method, **kwargs):

    # initial configuration attributes
    attrs = {}

    # populate base and add_attribute
    # loop for mapping.keys due to base and add_attribute
    # are seperate, cannot group the keys together
    for item in kwargs['self'].keys:        
        base_paths = kwargs['self']._populate_path(
                    base, kwargs['device'], keys=[item])
        add_attr_paths = kwargs['self']._populate_path(
                    add_attribute, kwargs['device'], keys=[item])
        # create add object instance
        add_inst = add_obj(device=kwargs['device'])

        for attr in add_attr_paths:
            if len(attr) == 2:
                setattr(add_inst, attr[0], attr[1])
            # TODO - when multiple lines class has more then 2 levels attributes
        
        ret = Configure._set_conf_attribute(conf=kwargs['conf_obj'],
                                 conf_structure=base_paths,
                                 return_attr=True)

        # add add_obj to the returned base conf object
        getattr(ret, add_method)(add_inst)
        attrs.update(Configure._build_attribute(base_paths))

    # apply configurations on devices
    if kwargs['unconfig']:
        kwargs['conf_obj'].build_unconfig(attributes=attrs)
    else:
        kwargs['conf_obj'].build_config(attributes=attrs)
