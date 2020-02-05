'''CLI utilities'''

try:
    import pyats.tcl
    from pyats.tcl import tclstr
except Exception:
    pass

import re
import functools
import logging
logger = logging.getLogger(__name__)

__all__ = (
    'clean_cli_output',
    'config_cli_to_tree',
    'cli_tree_to_config',
)


def clean_cli_output(output, cmd=None, os=None,
                     return_dict=False,
                     remove_prompt=True, remove_timestamp=True):
    d = {
        'cmd': None,
        'timestamp': None,
        'prompt': None,
    }
    try:
        output = tclstr(output)
    except NameError:
        pass

    from genie.libs.conf.utils import ansi

    output = re.sub(r'\t', r' ', output)
    output = re.sub(r'\r+\n', r'\n', output)
    output = re.sub(r'.*\r', r'', output, re.MULTILINE)
    output = re.sub(ansi.re_generic, r'', output)
    output = re.sub(r'\s+$', r'', output, re.MULTILINE)

    if cmd:
        m = re.match(r'^(?P<cmd>(?:do )?' + re.escape(cmd) + r')(?:\n|$)', output)
        if m:
            d.update(m.groupdict())
            output = output[:m.start(0)] + output[m.end(0):]

    if remove_timestamp:
        # Extract timestamp in the form "Thu May 29 01:56:01.913 UTC" or "Wed Jul 27 07:13:33 UTC 2011"
        # Only find it on first or second line and remove the whole line from the output
        m = re.search(r'''
            \A              # From start of string...
            (?:.*\n)?       # Skip the first line, or not
            (?P<line>       # The timestamp line
                #\r*        # Skip carriage returns (not needed based on previous cleaning)
                (?P<timestamp>
                    (?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)     # Day of week name
                    \ [A-Za-z]{3}                       # Month name
                    \ +\d+                              # Day of month
                    \ \d+:\d+:\d+                       # Time
                    (?:\.\d+)?                          # Optional milliseconds
                    \ [A-Za-z]{3,}                      # Timezone
                    (?:\ \d{4})?                        # Optional year
                )
                #[\ \t\r]*  # Skip spaces (not needed based on previous cleaning)
                (?:\n|\Z)   # End of line (or string)
            )
            ''', output, re.VERBOSE | re.MULTILINE)
        if m:
            d['timestamp'] = m.group('timestamp')
            output = output[:m.start('line')] + output[m.end('line'):]

    if remove_prompt:
        for once in [1]:
            m = re.search(r'''
                (?:^|\n)
                (?P<prompt>
                    (?P<prompt_location>D?RP/\d+/(?:RP|RSP)?\d+/(?:CPU)?\d+):
                    (?:
                        (?P<prompt_hostname>[\w-]+)
                        (?:
                            \((?P<prompt_mode>[^)]+)\)
                        )?
                        (?P<prompt_mark>[\#>])
                    )?
                )
                $
            ''', output, re.VERBOSE)
            if m:
                # IOS-XR:
                #   RP/0/0/CPU0:
                #   RP/0/0/CPU0:JSTVXR-R1#
                #   RP/0/0/CPU0:JSTVXR-R1(config)#
                d.update(m.groupdict())
                output = output[:m.start(0)] + output[m.end(0):]
                break
            m = re.search(r'(?:^|\n)(?P<prompt>[\w-]+(\([^\)]+\)){0,2}#)$', output)
            if m:
                # IOS / NX-OS:
                #   N7K-Get-well-R1#
                #   JSTVNX-R1(config)(xmlin)#
                d.update(m.groupdict())
                output = output[:m.start(0)] + output[m.end(0):]
                break
            m = re.search(r'(^|\n)(?P<prompt>\w+@[\w-]+[#>])$', output)
            if m:
                # Juniper:
                #   admin@MX4#
                d.update(m.groupdict())
                output = output[:m.start(0)] + output[m.end(0):]
                break

    if return_dict:
        d['output'] = output
        return d
    else:
        return output


def config_cli_to_tree(cli, *, os=None, strip=False, sort=False, keylist=False,
                       consistency_checks=False, keep_all=False,
                       keep_empty=False, keep_comments=False,
                       keep_closures=False):
    try:
        cli = tclstr(cli)
    except NameError:
        pass

    if keep_all:
        keep_empty = True
        keep_comments = True
        keep_closures = True

    tcl_imported = True

    try:
        from pyats.tcl.internal import DictionaryCompare
    except ImportError:
        tcl_imported = False
        pass

    def _DictionaryCompare_index0(first, second):
        if tcl_imported:
            return DictionaryCompare(first[0], second[0])
        else:
            return 0

    cli = clean_cli_output(cli, os=os)
    if keylist:
        cli = cli.replace('.', '_')

    if os == 'junos':

        if strip:
            cli = re.sub(r'^ +| +$', r'', cli, re.MULTILINE)

        if keep_comments:
            # Put inline comments on their own line
            cli = re.sub(r'; #', r';\n#', cli)
        else:
            # Remove inline comments
            cli = re.sub(r'; #.*', r'', cli)

        # Protect sub-modes with braces (Adds an extra open brace)
        cli = re.sub(r'^.*\S(?= +\{$)', r'{{&}', cli, re.MULTILINE)

        if keep_comments:
            # Protect comment lines
            if keylist:
                cli = re.sub(r'^ *#.*', r'{{&} {}}', cli, re.MULTILINE)
            else:
                cli = re.sub(r'^ *#.*', r'{{&}}', cli, re.MULTILINE)
        else:
            # Remove comment lines
            cli = re.sub(r'^ *#.*', r'', cli, re.MULTILINE)

        # Protect value config lines (drop the ;)
        if keylist:
            cli = re.sub(r'^(.*\S);$', r'{{\1} {}}', cli, re.MULTILINE)
        else:
            cli = re.sub(r'^(.*\S);$', r'{{\1}}', cli, re.MULTILINE)

        # Add an extra close brace to end of sub-modes
        cli = re.sub(r'^ *\}$', r'}}', cli, re.MULTILINE)

        # Need to get rid of the non-canonical string representations
        # and recurse into children
        if sort:

            def _clean_cli(clie):
                clie = pyats.tcl.cast_list(clie)
                if len(clie) == 2:
                    return (clie[0], tuple(sorted(
                        (_clean_cli(e) for e in pyats.tcl.cast_list(clie[1])),
                        key=functools.cmp_to_key(_DictionaryCompare_index0))))
                else:
                    return (clie[0], None)

            tree = tuple(sorted(
                (_clean_cli(e) for e in pyats.tcl.cast_list(cli)),
                key=functools.cmp_to_key(_DictionaryCompare_index0)))
        else:

            def _clean_cli(clie):
                clie = pyats.tcl.cast_list(clie)
                if len(clie) == 2:
                    return (clie[0], tuple(
                        (_clean_cli(e) for e in pyats.tcl.cast_list(clie[1]))))
                else:
                    return (clie[0], None)

            tree = tuple(
                (_clean_cli(e) for e in pyats.tcl.cast_list(cli)))

        return tree

    else:

        is_nxos = os == 'nxos'

        lvl = 0
        lvl_indent = {
            lvl: 0,
        }
        lvl_tree = {
            lvl: [],
        }

        def _wrap_up_one_lvl():
            # Generic code to wrap up lvl's tree to children and move up to lvl-=1
            nonlocal lvl
            nonlocal lvl_tree
            children = lvl_tree[lvl]
            if sort:
                children = sorted(
                    children,
                    key=functools.cmp_to_key(_DictionaryCompare_index0))
            lvl -= 1
            lvl_tree[lvl][-1] = (lvl_tree[lvl][-1][0], tuple(children))

        lines = cli.splitlines()
        for iline, my_line in enumerate(lines):
            keep_line = True

            if re.match(r'^Building configuration', my_line) \
                    or re.match(r'^Current configuration', my_line) \
                    or re.match(r'^!!? Last configuration change at', my_line) \
                    or re.match(r'^!!? NVRAM config last updated at', my_line) \
                    or re.match(r'^!(Command|Time):', my_line):
                continue

            my_indent = len(re.match(r'^ *', my_line).group(0))
            if strip:
                my_line = my_line.strip()

            if consistency_checks:
                if is_nxos:
                    if my_indent % 2:
                        pass  # TODO
                elif os is not None:
                    if my_indent > lvl_indent[lvl] + 1:
                        pass  # TODO

            if my_indent > lvl_indent[lvl]:

                # Scenario:
                #
                # a        (l=0, i=0)
                #  b       (l=1, i=1)
                #   c      (l=?, i=2)

                # Action: New level.
                #
                # a        (l=0, i=0)
                #  b       (l=1, i=1)
                #   c      (l=2, i=2)

                lvl += 1
                lvl_indent[lvl] = my_indent
                lvl_tree[lvl] = []

            else:
                while my_indent < lvl_indent[lvl]:

                    # a        (l=0, i=0)
                    #  b       (l=1, i=1)
                    #   c      (l=2, i=2)
                    # d        (l=?, i<2)

                    if my_indent <= lvl_indent[lvl - 1]:
                        # Scenarios:
                        #
                        #   a        (l=0, i=0)
                        #    b       (l=1, i=1)
                        #     c      (l=2, i=2)
                        #    d       (l=?, i=1)
                        #
                        #   a        (l=0, i=0)
                        #    b       (l=1, i=1)
                        #     c      (l=2, i=2)
                        #   d        (l=?, i=0)

                        # Action: Wrap up c(l=lvl) as child of b(l=lvl-1)
                        #
                        #   a        (l=0, i=0)
                        #    b       (l=1, i=1)  { c }
                        #    d       (l=?, i=1)
                        #
                        #   a        (l=0, i=0)
                        #    b       (l=1, i=1)  { c }
                        #   d        (l=?, i=0)

                        _wrap_up_one_lvl()

                    else:
                        # { lvl_indent[lvl - 1] < my_indent < lvl_indent[lvl] }

                        # Scenario:
                        #
                        # a        (l=0, i=0)
                        #  b       (l=1, i=1)
                        #    c     (l=2, i=3)
                        #   d      (l=?, i=2)

                        # Action: Fix bad indentation of previous block to match current
                        #
                        # a        (l=0, i=0)
                        #  b       (l=1, i=1)
                        #   c      (l=2, i=2)
                        #   d      (l=?, i=2)

                        if consistency_checks:
                            pass  # TODO

                        lvl_indent[lvl] = my_indent
                        break

            max_lvl = lvl

            for once in [1]:
                m = re.match(r'^ *exit$', my_line)
                if m:

                    # Scenario:
                    #
                    # a        (l=0, i=0)
                    #  b       (l=1, i=1)
                    #   "exit" (l=2, i=2)

                    # Action: Force current level to exit
                    #
                    # a        (l=0, i=0)
                    #  b       (l=1, i=1)

                    if lvl:
                        max_lvl = lvl - 1
                    elif consistency_checks:
                        pass  # TODO
                    keep_line = keep_closures
                    break

                m = re.match(r'^ *quit$', my_line)
                if m:

                    # Scenario:
                    #
                    # a        (l=0, i=0)
                    #  b       (l=1, i=1)
                    #   "quit" (l=2, i=2)

                    # Action: Force all levels to exit
                    #
                    # a        (l=0, i=0)
                    #  b       (l=1, i=1)

                    max_lvl = 0
                    keep_line = keep_closures
                    break

                m = re.match(r'^end$', my_line)
                if m:

                    # Scenario:
                    #
                    # a        (l=0, i=0)
                    #  b       (l=1, i=1)
                    # "end"    (l=2, i=0)

                    # Action: None
                    #
                    # a        (l=0, i=0)
                    #  b       (l=1, i=1)

                    max_lvl = 0
                    keep_line = keep_closures

                    if consistency_checks and iline != len(lines) - 1:
                        pass  # TODO
                    break

                m = re.match(r'^ *!', my_line)
                if m:
                    keep_line = keep_comments
                    break

                m = re.match(r'^$', my_line)
                if m:
                    keep_line = keep_empty
                    break

            if keep_line:
                if keylist:
                    lvl_tree[lvl].append((my_line, ()))
                else:
                    lvl_tree[lvl].append((my_line, None))

            while lvl > max_lvl:
                _wrap_up_one_lvl()

        while lvl:
            _wrap_up_one_lvl()

        # assert lvl == 0

        tree = lvl_tree[0]
        if sort:
            tree = sorted(
                tree,
                key=functools.cmp_to_key(_DictionaryCompare_index0))

        return tuple(tree)


def cli_tree_to_config(cli_tree, *, os=None):

    def _merge_cli_tree(line1, subcli1, ctx_lines=(), indent=''):
        line1 = line1.strip()
        lines = []
        if line1 != 'end':
            lines.append(indent + line1)
        sub_tree = ctx_lines + (line1,)
        sub_indent = indent + ' '
        sub_lines = []
        for line2, subcli2 in subcli1 or ():
            sub_lines += _merge_cli_tree(line2, subcli2, sub_tree, sub_indent)
        if sub_lines:
            lines += sub_lines
            m = re.match(r'^(?P<kw1>\S+)', line1)
            assert m, line1
            kw1 = m.group('kw1')
            if kw1 == 'if' \
                    and len(ctx_lines) == 1 \
                    and re.match(r'^route-policy ', ctx_lines[0]):
                pass  # else or endif follows
            elif kw1 == 'else' \
                    and len(ctx_lines) == 1 \
                    and re.match(r'^route-policy ', ctx_lines[0]):
                pass  # endif follows
            elif kw1 in (
                'route-policy',
                'community-set',
            ) \
                and len(ctx_lines) == 0:
                pass  # end-policy/end-set follows
            else:
                # Need exit
                sub_exit = sub_indent + 'exit'
                if sub_lines[-1] != sub_exit:
                    lines.append(sub_exit)
        return lines

    lines = []
    for line1, subcli1 in cli_tree or ():
        lines += _merge_cli_tree(line1, subcli1)

    return '\n'.join(lines)

