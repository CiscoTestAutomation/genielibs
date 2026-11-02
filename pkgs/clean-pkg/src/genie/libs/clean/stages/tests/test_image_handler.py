import copy
import importlib
import unittest
from unittest.mock import Mock, call, patch

from pyats.utils.schemaengine import SchemaError

from genie.libs.clean.stages.image_handler import BaseImageHandler, normalize_image_paths


class TestNormalizeImagePaths(unittest.TestCase):

    IMAGE = '/auto/image.bin'

    def test_supported_image_formats(self):
        for images in (self.IMAGE, [self.IMAGE], {'file': [self.IMAGE]},
                       {'image': [self.IMAGE]}, {'image': {'file': [self.IMAGE]}},
                       [{'image': {'file': [self.IMAGE]}}]):
            with self.subTest(images=images):
                self.assertEqual(normalize_image_paths(images), [self.IMAGE])

    def test_multi_file_paths_keep_bytes_and_order(self):
        paths = ['file:///auto/image.bin', 'flash:/packages.conf', '/auto/package.bin']
        for images in (paths, {'file': paths}):
            with self.subTest(images=images):
                normalized = normalize_image_paths(images, require_single=False)
                self.assertEqual(normalized, paths)
                self.assertIsNot(normalized, paths)

    def test_no_mutation_or_list_aliasing(self):
        metadata = [{'image': {'file': [self.IMAGE]}}]
        original = copy.deepcopy(metadata)
        paths = normalize_image_paths(metadata)
        paths.append('/auto/another.bin')
        self.assertEqual(metadata, original)

    def test_missing_metadata(self):
        for metadata in (None, [], {}, {'file': []}, {'image': None},
                         [{'image': {'file': []}}], [self.IMAGE, {'file': []}]):
            with self.subTest(metadata=metadata), self.assertRaisesRegex(SchemaError, 'missing|empty'):
                normalize_image_paths(metadata)

    def test_invalid_path_strings(self):
        for images, message in (
                ('', 'single-line image path'),
                (' ', 'single-line image path'),
                (['/auto/image.bin\nboot stale.bin'], 'single-line image path'),
                (['/auto/image.bin\r'], 'single-line image path'),
                (str([self.IMAGE]), 'serialized mapping/list'),
                (str({'image': {'file': [self.IMAGE]}}), 'serialized mapping/list')):
            with self.subTest(images=images), self.assertRaisesRegex(SchemaError, message):
                normalize_image_paths(images)

    def test_unsupported_types_and_shapes(self):
        for metadata in (1, False, b'/auto/image.bin', ('/auto/image.bin',),
                         {'path': self.IMAGE}, {'image': [self.IMAGE], 'file': [self.IMAGE]},
                         {'image': [self.IMAGE], 'packages': ['/auto/package.bin']}, [[self.IMAGE]],
                         {'file': [123]}, [self.IMAGE, None],
                         {'image': {'image': [self.IMAGE]}}):
            with self.subTest(metadata=metadata), self.assertRaisesRegex(SchemaError, 'unsupported|missing|Expected'):
                normalize_image_paths(metadata)

    def test_image_paths_reject_terminal_controls_and_surrounding_whitespace(self):
        controls = ''.join(chr(value) for value in (*range(32), *range(127, 160))) + '\u2028\u2029'
        paths = [self.IMAGE + control + suffix for control in controls
                 for suffix in ('', 'boot flash:/stale-golden.bin')]
        paths.extend(control + self.IMAGE for control in controls)
        paths.extend((' ' + self.IMAGE, self.IMAGE + ' '))
        for path in paths:
            for metadata in (path, [{'image': {'file': [path]}}]):
                with self.subTest(metadata=metadata), self.assertRaisesRegex(SchemaError, 'image path'):
                    normalize_image_paths(metadata)

    def test_primary_image_must_be_unique(self):
        for metadata in ([self.IMAGE, '/auto/other.bin'], {'file': [self.IMAGE, '/auto/other.bin']},
                         [{'image': {'file': [self.IMAGE, '/auto/other.bin']}}],
                         [{'image': [self.IMAGE]}, {'image': ['/auto/other.bin']}],
                         [self.IMAGE, self.IMAGE]):
            with self.subTest(metadata=metadata), self.assertRaisesRegex(SchemaError, 'exactly one image path'):
                normalize_image_paths(metadata)


class TestPlatformLoaderNormalization(unittest.TestCase):

    PLATFORMS = {
        'iosxe': ('image',), 'ios': ('image',), 'viptela': ('image',),
        'iosxr': ('image',), 'cheetah.ap': ('image',),
        'nxos.n9k': ('system',), 'nxos.n3k': ('system',),
        'nxos.n7k': ('kickstart', 'system'), 'nxos.n5k': ('kickstart', 'system'),
        'nxos.mds': ('kickstart', 'system'), 'nxos.aci': ('switch',),
        'apic': ('controller', 'switch'),
    }

    def test_shared_role_normalization_preserves_optional_and_multi_file_roles(self):
        handler = BaseImageHandler(Mock())
        handler.image = ['/auto/image.bin']
        handler.packages = ['/auto/pkg1.bin', '/auto/pkg2.bin']
        handler.other = []
        handler.unselected = {'unsupported': None}
        with patch('genie.libs.clean.stages.image_handler.normalize_image_paths',
                   wraps=normalize_image_paths) as normalize:
            handler.normalize_image_roles(('image', 'packages', 'other', 'missing'))
        self.assertEqual(normalize.call_args_list, [
            call(['/auto/image.bin'], require_single=False),
            call(['/auto/pkg1.bin', '/auto/pkg2.bin'], require_single=False),
        ])
        self.assertEqual(handler.image, ['/auto/image.bin'])
        self.assertEqual(handler.packages, ['/auto/pkg1.bin', '/auto/pkg2.bin'])
        self.assertEqual(handler.other, [])
        self.assertFalse(hasattr(handler, 'missing'))
        self.assertEqual(handler.unselected, {'unsupported': None})

    def test_existing_platform_formats(self):
        for platform, roles in self.PLATFORMS.items():
            handler = importlib.import_module(f'genie.libs.clean.stages.{platform}.image_handler').ImageHandler
            paths = {role: [f'/auto/{role}.bin'] for role in roles}
            for metadata in (sum(paths.values(), []), paths,
                             {role: {'file': value} for role, value in paths.items()}):
                with self.subTest(platform=platform, metadata=metadata):
                    original = copy.deepcopy(metadata)
                    instance = handler(Mock(), metadata)
                    for role, expected in paths.items():
                        self.assertEqual(getattr(instance, role), expected)
                    self.assertEqual(metadata, original)

    def test_schema_rejection_happens_before_normalization(self):
        for platform in ('iosxe', 'ios', 'viptela', 'nxos.n9k', 'nxos.n7k',
                         'nxos.n5k', 'nxos.mds', 'nxos.aci', 'apic'):
            module = importlib.import_module(f'genie.libs.clean.stages.{platform}.image_handler')
            with self.subTest(platform=platform), \
                    patch('genie.libs.clean.stages.image_handler.normalize_image_paths') as normalize:
                with self.assertRaisesRegex(Exception, 'Expected one of the following structures'):
                    module.ImageHandler(Mock(), {'unsupported_role': ['/auto/image.bin']})
                normalize.assert_not_called()

    def test_iosxe_smu_only_and_multiple_packages_remain_supported(self):
        from genie.libs.clean.stages.iosxe.image_handler import ImageHandler

        self.assertEqual(ImageHandler(Mock(), ['/auto/smu.bin']).image, [])
        handler = ImageHandler(Mock(), {
            'image': {'file': ['/auto/image.bin']},
            'packages': {'file': ['/auto/pkg1.bin', '/auto/pkg2.bin']}, 'other': {'file': []},
        })
        self.assertEqual(handler.packages, ['/auto/pkg1.bin', '/auto/pkg2.bin'])
        self.assertEqual(handler.other, [])

    def test_standalone_load_normalizes_only_after_schema_acceptance(self):
        for platform in ('iosxe', 'ios', 'viptela', 'nxos.n9k', 'nxos.n7k',
                         'nxos.n5k', 'nxos.mds', 'nxos.aci', 'apic'):
            module = importlib.import_module(f'genie.libs.clean.stages.{platform}.image_handler')
            loader = module.ImageLoader()
            roles = self.PLATFORMS[platform]
            metadata = {role: {'file': [f'/auto/{role}.bin']} for role in roles}
            events = []
            validate = loader.valid_structure_3

            def validate_schema(images):
                result = validate(images)
                self.assertTrue(result)
                events.append('schema accepted')
                return result

            def normalize(paths, **kwargs):
                self.assertEqual(events[0], 'schema accepted')
                self.assertEqual(kwargs, {'require_single': False})
                events.append('normalized')
                return normalize_image_paths(paths, **kwargs)

            with self.subTest(platform=platform), \
                    patch.object(loader, 'valid_structure_3', side_effect=validate_schema), \
                    patch('genie.libs.clean.stages.image_handler.normalize_image_paths', side_effect=normalize):
                loader.load(metadata)
                self.assertEqual(events, ['schema accepted'] + ['normalized'] * len(roles))
