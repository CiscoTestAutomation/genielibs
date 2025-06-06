"""IOSXE: Image Handler Class"""

import yaml

from genie.libs.clean.stages.image_handler import BaseImageHandler

from pyats.utils.schemaengine import Schema, ListOf, Optional


class ImageLoader(object):

    EXPECTED_IMAGE_STRUCTURE_MSG = """\
Expected one of the following structures for 'images' in the clean yaml

Other images are optional other files, in structure #1 other files are not supported because there is no way to distinguish them from optional packages

Structure #1
------------
images:
- /path/to/image.bin
- /path/to/smu.bin
- /path/to/optional_package1
- /path/to/optional_package2

Structure #2
------------
images:
  image:
  - /path/to/image.bin
  smu: <<< optional
  - /path/to/smu.bin
  packages:   <<< optional
  - /path/to/optional_package1
  - /path/to/optional_package2
  other:   <<< optional
  - /path/to/other/images.bin

Structure #3
------------
images:
  image:
    file:
    - /path/to/image.bin
  smu:  <<< optional
    file:
    - /path/to/smu.bin
  packages:  <<< optional
    file:
    - /path/to/optional_package1
    - /path/to/optional_package2
  other:  <<< optional
    file:
    - /path/to/other/images.bin

But got the following structure
-------------------------------
{}"""

    def load(self, images):
        if (
            not self.valid_structure_1(images)
            and not self.valid_structure_2(images)
            and not self.valid_structure_3(images)
        ):

            raise Exception(
                self.EXPECTED_IMAGE_STRUCTURE_MSG.format(yaml.dump({"images": images}))
            )

    def valid_structure_1(self, images):

        schema = ListOf(str)
        smus = []
        packages = []

        try:
            Schema(schema).validate(images)
        except Exception:
            return False

        if len(images) == 1:
            if "smu" in images[0]:
                setattr(self, "smu", images)
            else:
                setattr(self, "image", images)
            return True
        if len(images) >= 2:
            setattr(self, "image", images[:1])

            for image in images[1:]:

                if "smu" in image:
                    smus.append(image)
                    setattr(self, "smu", smus)
                    continue

                packages.append(image)
                setattr(self, "packages", packages)

            return True
        else:
            return False

    def valid_structure_2(self, images):

        schema = {
            "image": ListOf(str),
            Optional("smu"): ListOf(str),
            Optional("packages"): ListOf(str),
            Optional("other"): ListOf(str),
        }

        try:
            Schema(schema).validate(images)
        except Exception:
            return False

        if len(images["image"]) != 1:
            return False
        else:
            setattr(self, "image", images["image"])

        if "smu" in images:
            setattr(self, "smu", images["smu"])

        if "packages" in images:
            setattr(self, "packages", images["packages"])

        setattr(self, "other", images.get("other", []))

        return True

    def valid_structure_3(self, images):

        schema = {
            "image": {"file": ListOf(str)},
            Optional("smu"): {"file": ListOf(str)},
            Optional("packages"): {"file": ListOf(str)},
            Optional("other"): {"file": ListOf(str)},
        }

        try:
            Schema(schema).validate(images)
        except Exception:
            return False

        if len(images["image"]["file"]) != 1:
            return False
        else:
            setattr(self, "image", images["image"]["file"])

        if "smu" in images:
            setattr(self, "smu", images["smu"]["file"])

        if "packages" in images:
            setattr(self, "packages", images["packages"]["file"])

        setattr(self, "other", images.get("other", {}).get("file", []))

        return True


class ImageHandler(BaseImageHandler, ImageLoader):

    def __init__(self, device, images, *args, **kwargs):

        # Set default
        self.image = []
        self.smu = []
        self.packages = []
        self.other = []

        # Check if images is one of the valid structures and
        # load into a consolidated structure
        ImageLoader.load(self, images)

        # Temp workaround for XPRESSO
        self.image = [self.image[0].replace("file://", "")] if self.image else []

        if hasattr(self, "smu"):
            self.smu = [x.replace("file://", "") for x in self.smu]

        if hasattr(self, "packages"):
            self.packages = [x.replace("file://", "") for x in self.packages]

        if hasattr(self, "other"):
            self.other = [x.replace("file://", "") for x in self.other]

        self.original_image = [self.image[0].replace("file://", "")] if self.image else []

        super().__init__(device, *args, **kwargs)

    def update_image_references(self, section):
        # section.parameters['image_mapping'] shall be saved in any
        # stage that modifies the image name/path
        if "image_mapping" in section.parameters:

            for index, image in enumerate(self.image):
                # change the saved image to the new image name/path
                self.image[index] = section.parameters["image_mapping"].get(
                    image, image
                )

            for index, smu in enumerate(self.smu):
                # change the saved smu image to the new smu image name/path
                self.smu[index] = section.parameters["image_mapping"].get(smu, smu)

            for index, package in enumerate(self.packages):
                # change the saved package to the new package name/path
                self.packages[index] = section.parameters["image_mapping"].get(
                    package, package
                )

            if hasattr(self, "other"):
                for index, image in enumerate(self.other):
                    self.other[index] = section.parameters["image_mapping"].get(
                        image, self.other[index]
                    )

    def update_tftp_boot(self, number=""):
        """Update clean section 'tftp_boot' with image information"""
        tftp_boot = self.device.clean.setdefault("tftp_boot" + number, {})
        if self.override_stage_images:
            tftp_boot.update({"image": self.image})
        else:
            tftp_boot.setdefault("image", self.image)

    def update_copy_to_linux(self, number=""):
        """Update clean section 'copy_to_linux' with image information"""

        origin = self.device.clean.setdefault("copy_to_linux" + number, {}).setdefault(
            "origin", {}
        )

        if self.override_stage_images:
            origin.update({"files": self.image + self.smu + self.packages + self.other})
        else:
            origin.setdefault(
                "files", self.image + self.smu + self.packages + self.other
            )

    def update_copy_to_device(self, number=""):
        """Update clean stage 'copy_to_device' with image information"""

        origin = self.device.clean.setdefault("copy_to_device" + number, {}).setdefault(
            "origin", {}
        )

        if self.override_stage_images:
            origin.update({"files": self.image + self.smu + self.packages + self.other})
        else:
            origin.setdefault(
                "files", self.image + self.smu + self.packages + self.other
            )

    def update_change_boot_variable(self, number=""):
        """Update clean stage 'change_boot_variable' with image information"""

        change_boot_variable = self.device.clean.setdefault(
            "change_boot_variable" + number, {}
        )
        if self.override_stage_images:
            change_boot_variable.update({"images": self.image})
        else:
            change_boot_variable.setdefault("images", self.image)

    def update_expand_image(self, number=""):
        """Update clean stage 'expand_image' with image information"""

        expand_image = self.device.clean.setdefault("expand_image" + number, {})
        if self.override_stage_images:
            expand_image.update({"image": self.image})
        else:
            expand_image.setdefault("image", self.image)

    def update_verify_running_image(self, number=""):
        """Update clean stage 'verify_running_image' with image information"""
        verify_running_image = self.device.clean.setdefault(
            "verify_running_image" + number, {}
        )

        if verify_running_image.get("verify_md5"):
            if self.override_stage_images:
                verify_running_image.update({"images": self.original_image})
            else:
                verify_running_image.setdefault("images", self.original_image)
        else:
            if self.override_stage_images:
                verify_running_image.update({"images": self.image})
            else:
                verify_running_image.setdefault("images", self.image)

    def update_install_image(self, number=""):
        """Update clean stage 'install_image' with image information"""

        install_image = self.device.clean.setdefault("install_image" + number, {})
        if self.override_stage_images:
            install_image.update({"images": self.image})
        else:
            install_image.setdefault("images", self.image)

    def update_install_smu(self, number=""):
        """Update clean stage 'install_smu' with smu image information"""

        install_smu = self.device.clean.setdefault("install_smu" + number, {})
        if self.override_stage_images:
            install_smu.update({"images": self.smu})
        else:
            install_smu.setdefault("images", self.smu)

    def update_install_packages(self, number=""):
        """Update clean stage 'install_packages' with package information"""

        install_packages = self.device.clean.setdefault("install_packages" + number, {})
        if self.override_stage_images:
            install_packages.update({"packages": self.packages})
        else:
            install_packages.setdefault("packages", self.packages)

    def update_reload(self, number=""):
        """Update reload stage reload_service_args.image with image information

        Only updates image info if `copy_to_device` stage was executed.
        """
        if "copy_to_device" in self.history and self.image:
            reload_service_args = self.device.clean.setdefault(
                "reload" + number, {}
            ).setdefault("reload_service_args", {})
            reload_service_args["image"] = self.image[0]

    def update_install_remove_inactive(self, number=""):
        """Update install_remove_inactive stage images with image information"""
        install_remove_inactive = self.device.clean.setdefault(
            "install_remove_inactive" + number, {}
        )
        if self.override_stage_images:
            install_remove_inactive.update({"images": self.image})
        else:
            install_remove_inactive.setdefault("images", self.image)
