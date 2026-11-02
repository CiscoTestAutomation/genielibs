'''Common OS: Image Handler Class'''

from collections.abc import Mapping

from pyats.utils.schemaengine import Schema, ListOf, SchemaError


def normalize_image_paths(images, *, require_single=True) -> list[str]:
    '''Normalize Clean image metadata to a list of image paths.

    Args:
        images: A path string, flat path list, or image/file mapping, including
            wrappers such as ``[{'image': {'file': ['/auto/image.bin']}}]``.
        require_single (bool, optional): Require exactly one primary boot image.
            Defaults to True. Platform loaders use False for multi-file roles
            after their existing schema validation and role separation.

    Returns:
        list[str]: A new list of unchanged paths in input order. Input metadata
            is not mutated; paths are not deduplicated or selected by filename.
            Paths must be printable and have no surrounding whitespace.

    Raises:
        SchemaError: Missing, empty, unsupported or invalid metadata,
            or multiple paths when require_single is True.
    '''
    if not isinstance(images, list):
        images = [images]

    paths = []
    for image in images:
        if isinstance(image, list):
            raise SchemaError('Nested path lists are unsupported; use a flat path list')

        # Resolve only the supported image/file wrappers, not arbitrary nesting.
        for key in ('image', 'file'):
            if isinstance(image, Mapping) and key in image:
                if len(image) != 1:
                    raise SchemaError(
                        'unsupported or ambiguous image mapping; '
                        'provide exactly one image or file key')
                image = image[key]

        if image is None or (isinstance(image, (list, Mapping)) and not image):
            raise SchemaError('Image metadata is missing or empty; provide an image path')
        if isinstance(image, str):
            image = [image]
        Schema(ListOf(str)).validate(image)

        for path in image:
            text = path.strip()
            # Preserve the exact ROMMON value without accepting terminal controls.
            if not text or path != text or not path.isprintable():
                raise SchemaError(
                    'Provide a non-empty, printable, single-line image path string '
                    'without surrounding whitespace')
            if ((text.startswith('{') and text.endswith('}')) or
                    (text.startswith('[') and text.endswith(']'))):
                raise SchemaError(
                    'serialized mapping/list is not an image path; use image/file metadata')
            paths.append(path)

    if not paths:
        raise SchemaError('Image metadata is empty; provide at least one image path')
    if require_single and len(paths) != 1:
        raise SchemaError(
            f'Ambiguous primary boot image: found {len(paths)} image paths; '
            'specify exactly one image path, separate from packages/other files')
    return paths


class BaseImageHandler(object):

    def __init__(self, device, *args, **kwargs):
        self.device = device

        # keep track of stages calling image handler
        self.history = []

        # By default, override images for stages, even if user specified
        # User can configure this via `image_handler.override_stage_images`
        # boolean in clean.yaml file
        self.override_stage_images = True

    def normalize_image_roles(self, roles):
        """Normalize platform-validated roles without merging their image paths."""
        for image_type in roles:
            paths = getattr(self, image_type, [])
            if paths:
                setattr(self, image_type, normalize_image_paths(paths, require_single=False))

    def update_section(self, section_uid, update_history=False):
        ''' Initializes section dictionary and calls update method for
            respective method '''
        if update_history:
            self.history.append(section_uid)

        if (section_uid not in self.device.clean or
                not self.device.clean[section_uid]):
            self.device.clean[section_uid] = {}

        sections = section_uid.split("__")
        if len(sections) == 1:
            section_uid = sections[0]
            number = ''
        else:
            section_uid = sections[0]
            number = '__{}'.format(sections[1])

        # call the ImageHandler update method
        if hasattr(self, 'update_' + section_uid):
            getattr(self, 'update_' + section_uid)(number)
