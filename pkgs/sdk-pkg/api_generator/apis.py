import os
import sys
import yaml
import json
import pathlib
import logging
import inspect
import argparse
import importlib
IGNORE_DIR = ['.git', '__pycache__', 'template', 'tests']
IGNORE_FILE = ['__init__.py', 'base.py', 'common.py']

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)

class CreateApiDoc(object):
    def __init__(self, datafile):
        assert 'VIRTUAL_ENV' in os.environ
        with open(datafile, 'r') as f:
            self.datafile = yaml.safe_load(f)
        self.output = {}

    def _expand(self, name):
        if '$env(VIRTUAL_ENV)' in name:
            # Replace '$env(VIRTUAL_ENV)' with the actual value
            return name.replace('$env(VIRTUAL_ENV)', os.environ['VIRTUAL_ENV'])
        return name

    # get all functions in a module
    def _find_functions(self, mod, tokens):
        abs_mod_name = self._get_mod_name(mod)
        for name, obj in inspect.getmembers(mod):
            # starts with _ are ignored
            if name.startswith('_'):
                continue
            # ignore the imported functions
            if inspect.isfunction(obj) and obj.__module__ == mod.__name__:
                sub_dict = self.output.setdefault(name, {})
                if not tokens:
                    tokens = ['com']
                for token in tokens:
                    if token not in sub_dict:
                        sub_dict[token] = {}
                    sub_dict = sub_dict[token]

                sub_dict['module_name'] = abs_mod_name
                sub_dict['doc'] = obj.__doc__
                sub_dict['uid'] = name
                line = inspect.getsourcelines(obj)[-1]

                temp_url = mod.__file__.replace(os.path.join(
                               os.environ['VIRTUAL_ENV'], 'pypi', 'genielibs') + '/', '')

                style = self.root['url']['style']

                if style == 'bitbucket':
                    url = '{p}{t}#{l}'.format(p=self.root['url']['link'], t=temp_url, l=line)
                elif style == 'github':
                    url = self.root['url']['link'].format(branch=self.root['url']['branch'])
                    url = '{p}{t}#L{l}'.format(p=url, t=temp_url, l=line)

                sub_dict['url'] = url

    def _get_mod_name(self, mod):
        mod_name = []
        name_list = mod.__name__.replace(self.root['root'], '').split('.')
        # if directory is abstracted
        for i, e in enumerate(name_list):
            if not hasattr(importlib.import_module(self.root['root'] + '.'.join(name_list[0:i+1])), '__abstract_token'):
                mod_name.append(e)
        return '.'.join(mod_name)[1:]

    def _is_abstract_dir(self, dir):
        mod = str(dir).replace(self.module_loc, '').replace('/', '.')
        return hasattr(importlib.import_module(mod, package=self.root['root']), '__abstract_token')

    def _add_functions(self, item, tokens):
        # Will give module path
        module_path = self.root['root'] + str(item).rsplit('.', 1)[0].\
                                  replace(self.module_loc, '').replace('/', '.')
        mod = importlib.import_module(module_path)
        self._find_functions(mod, tokens)

    def _recursive_find(self, item, token):
        for item in item.iterdir():
            if item.is_dir():
                if item.name in IGNORE_DIR:
                    # Ignore
                    continue
                elif self._is_abstract_dir(item.as_posix()):
                    self._recursive_find(item, token + [item.name])
                else:
                    self._recursive_find(item, token)

            elif item.is_file():
                if item.name in IGNORE_FILE or item.suffix != '.py':
                    continue
                # Then add it to the self.datafile
                self._add_functions(item, token)

    def find_all_apis(self):
        if 'root_directories' not in self.datafile:
            return {}

        for name, values in self.datafile['root_directories'].items():
            log.info("Learning '{name}'".format(name=name))

            # Figure out location of package so you can walk it
            self.root = values
            self.module_loc = importlib.import_module(self.root['root']).__path__[0]

            # Walk all file in there and go through the apis
            self._recursive_find(pathlib.Path(self.module_loc), [])

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-datafile',
                        metavar='FILE',
                        type=str,
                        default=None,
                        help='File containing directory information')
    parser.add_argument('-save_location',
                        metavar='FILE',
                        type=str,
                        default=None,
                        help='Location to save the output file')
    custom_args = parser.parse_known_args()[0]
    apiDoc = CreateApiDoc(custom_args.datafile)
    apiDoc.find_all_apis()
    output = json.dumps(apiDoc.output)
    os.makedirs(os.path.dirname(custom_args.save_location), exist_ok=True)
    with open(custom_args.save_location, 'w+') as f:
        f.write(output)
