from pyats.utils import utils
try:
    from pyats.utils.yaml.markup import Processor, REFERENCE_PATTERN
except Exception:
    from pyats.utils.yaml.markup import Processor, PATTERN as REFERENCE_PATTERN

from pyats.utils.yaml.exceptions import MarkupError

class TopologyMarkupProcessor(Processor):

    def _process_str(self, data, index, locations=None):
        # overload the string processor to support %{self}

        while True:
            # cannot use for match in REGEX.finditer(data)
            # because data is a moving target (changes per subsitution)
            # note that this mechanism is also nested - if a refers to b which
            # refers to C, it will recursively replace everything.

            match = REFERENCE_PATTERN.search(data)

            if not match: break

            # support for self keyword
            if match.group(2) == 'self' or match.group(2).startswith('self.'):
                if index[0] != 'devices':
                        raise MarkupError(
                                "Keyword 'self' can only be used within "
                                "'devices' section:\n"
                                "Index: %s\n"
                                "Markup: %s" % ('.'.join(index),
                                                match.group(0)))

            if match.group(2) == 'self':
                # self represents device name (index:1)
                data = data.replace(data[slice(*match.span(0))], index[1])

            else:
                # data reference pointer
                match_list = match.group(2)

                if match_list.startswith('self.'):
                    # self.x.y.z -> device.<name>.x.y.z
                    # replace the first self (limit to 1)
                    match_list = match.group(2).replace('self',
                                                        '.'.join(index[0:2]),
                                                        1)

                # collect the corresponding value
                try:
                    value = utils.chainget(self.original, match_list)

                except KeyError as e:
                    raise MarkupError(
                            "Caught error while processing markups: \n"
                            "Index: %s\n"
                            "Markup: %s\n"
                            %  ('.'.join(index), match.group(0))) from e

                else:
                    # test for recursion
                    # warning: doesn't test if list item refers to list's self
                    #          or dict's item doesn't refer to dict's self
                    if value ==  utils.chainget(self.original, index):
                        raise MarkupError('Detected recursion markup: \n'
                                          "Index: %s\n"
                                          "Markup: %s\n"
                                          %  ('.'.join(index), match.group(0)))

                # do replacement
                data = data.replace(data[slice(*match.span(0))], str(value))

        return data




    # def process_markup(self, content, index = None, original = None):
    #     '''Process Markup Function

    #     Helper API. Used to process markup languages within the topology yaml
    #     file into concrete content. This is a functionality outside of YAML
    #     standard, and is intended to mimic variablelizing YAML content.

    #     Arguments
    #     ---------
    #         content (dict): input dictionary content
    #         index (list): list tracking current nested dictionary index
    #         original (dict): original dictionary that this call was called with.
    #                          required because this is a nested api call.

    #     Returns
    #     -------
    #         dict() of converted content with all markups translated.

    #     '''

    #     elif isinstance(content, str):
    #         # only string can be processed:
    #         for match in re.findall('%{ *(.+?) *}', content):
    #             if match == 'self' or match.startswith('self.'):
    #                 if index[0] != 'devices':
    #                     raise MarkupError(
    #                              "Keyword 'self' can only be used within "
    #                              "'devices' section:\n"
    #                              "Index: %s\n"
    #                              "Markup: %s" % ('.'.join(index), content))

    #             try:
    #                 if match == 'self':
    #                         content = re.sub('%%{ *%s *}' % match, index[1] , content)
    #                 elif match.startswith('self.'):
    #                     match_list = index[0:2] + match.split('.')[1:]

    #                     content = re.sub('%%{ *%s *}' % match,
    #                                   str(self.chain_get(match_list, original)),
    #                                   content)
    #                 else:
    #                     content = re.sub('%%{ *%s *}' % match,
    #                                   str(self.chain_get(match.split('.'),
    #                                                      original)),
    #                                   content)
    #             except Exception as e:
    #                 raise MarkupError(
    #                         "Caught error while processing markups: \n"
    #                         "Index: %s\n"
    #                         "Markup: %s\n"
    #                         %  ('.'.join(index), content)) from e
    #     return content
