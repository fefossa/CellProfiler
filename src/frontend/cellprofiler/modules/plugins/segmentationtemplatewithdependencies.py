#################################
#
# Imports from useful Python libraries
#
#################################

import numpy
import os
import skimage
import importlib.metadata
import subprocess
import uuid
import shutil
import logging
import sys

import your_dependency_with_a_long_and_improbable_name

#################################
#
# Imports from CellProfiler
#
##################################

from cellprofiler_core.image import Image
from cellprofiler_core.module.image_segmentation import ImageSegmentation
from cellprofiler_core.object import Objects
from cellprofiler_core.setting import Binary, ValidationError
from cellprofiler_core.setting.choice import Choice
from cellprofiler_core.setting.do_something import DoSomething
from cellprofiler_core.setting.subscriber import ImageSubscriber
from cellprofiler_core.preferences import get_default_output_directory
from cellprofiler_core.setting.text import (
    Integer,
    ImageName,
    Directory,
    Filename,
    Float,
)

LOGGER = logging.getLogger(__name__)

__doc__ = f"""\
SegmentationTemplateWithDependencies
====================================

============ ============ ===============
Supports 2D? Supports 3D? Respects masks?
============ ============ ===============
YES/NO       YES/NO       YES/NO
============ ============ ===============

"""
#
# Constants
#
# It's good programming practice to replace things like strings with
# constants if they will appear more than once in your program. That way,
# if someone wants to change the text, that text will change everywhere.
# Also, you can't misspell it by accident.
#

DOCKER_NAME = "cellprofiler/cellprofiler:v4.2.6"

SOME_CHOICES = []


class SegmentationTemplateWithDependencies(ImageSegmentation):
    category = "Object Processing"

    module_name = "SegmentationTemplateWithDependencies"

    variable_revision_number = 1

    doi = {
        "Optional paper that one can ask the user to cite:": "https://doi.org/some_doi",
    }

    def create_settings(self):
        super(SegmentationTemplateWithDependencies, self).create_settings()

        self.docker_or_python = Choice(
            text="Run this segmentation thing in docker or local python environment",
            choices=["Docker", "Python"],
            value="Docker",
            doc="""\
If Docker is selected, ensure that Docker Desktop is open and running on your
computer. On first run of the X plugin, the Docker container will be
downloaded, which may be slow . However, this slow downloading process will only have to happen
once.

If Python is selected, the Python environment in which CellProfiler is installed will be used.
""",
        )

        self.docker_image = Choice(
            text="Select your external docker image",
            choices=[DOCKER_NAME],
            value=DOCKER_NAME,
            doc="""\
Select which Docker image to use for running your plugin.
"""
        )

        self.some_numerical_parameter = Integer(
            text="Some configurable parameter",
            value=30,
            minval=0,
            doc="""\
""",
        )

        self.some_listy_parameter = Choice(
            text="Parameter where the user picks from a list",
            choices=SOME_CHOICES,
            value=SOME_CHOICES[0],
            doc="""
""",
        )


    def settings(self):
        return [
            self.x_name,
            self.docker_or_python,
            self.docker_image,
            self.some_listy_parameter,
            self.some_numerical_parameter,
            self.y_name,
        ]

    def visible_settings(self):
        vis_settings = [self.docker_or_python]

        if self.docker_or_python.value == "Docker":
            vis_settings += [self.docker_image]


        vis_settings += [
            self.some_numerical_parameter,
            self.some_listy_parameter,
            self.y_name,
        ]

        if self.docker_or_python.value == 'Python':
            if self.use_gpu.value:
                vis_settings += [self.gpu_test]

        return vis_settings


    def run(self, workspace):
        x_name = self.x_name.value
        y_name = self.y_name.value
        images = workspace.image_set
        x = images.get_image(x_name)
        x_data = x.pixel_data
        dimensions = x.dimensions

        if self.docker_or_python.value == "Python":

            from your_dependency_with_a_long_and_improbable_name import somefunction

            try:
                y_data = some_function(uses_our_parameters)
        

            except Exception as a:
                        print(f"Unable to create masks. Check your module settings. {a}")
        elif self.docker_or_python.value == "Docker":
            # Define how to call docker
            docker_path = "docker" if sys.platform.lower().startswith("win") else "/usr/local/bin/docker"
            # Create a UUID for this run
            unique_name = str(uuid.uuid4())
            # Directory that will be used to pass images to the docker container
            temp_dir = os.path.join(get_default_output_directory(), ".cellprofiler_temp", unique_name)
            temp_img_dir = os.path.join(temp_dir, "img")
            
            os.makedirs(temp_dir, exist_ok=True)
            os.makedirs(temp_img_dir, exist_ok=True)

            temp_img_path = os.path.join(temp_img_dir, unique_name+".tiff")

            # Save the image to the Docker mounted directory
            skimage.io.imsave(temp_img_path, x_data)

            cmd = f"""
            {docker_path} run --rm -v {temp_dir}:/data
            {self.docker_image.value}
            {some_flags}
            """

            try:
                subprocess.run(cmd.split(), text=True)
                #here the external library made a numpy array, you might use skimage.io.imread if it's a tiff file, etc
                y_data = numpy.load(os.path.join(temp_img_dir, "some_segmentation_file_name"), allow_pickle=True).item()

            finally:      
                # Delete the temporary files
                try:
                    shutil.rmtree(temp_dir)
                except:
                    LOGGER.error("Unable to delete temporary directory, files may be in use by another program.")
                    LOGGER.error("Temp folder is subfolder {tempdir} in your Default Output Folder.\nYou may need to remove it manually.")


        y = Objects()
        y.segmented = y_data
        y.parent_image = x.parent_image
        objects = workspace.object_set
        objects.add_objects(y, y_name)


        self.add_measurements(workspace)

        if self.show_window:
            if x.volumetric:
                workspace.display_data.x_data = x.pixel_data
            else:
                workspace.display_data.x_data = x_data
            workspace.display_data.y_data = y_data
            workspace.display_data.dimensions = dimensions

    def display(self, workspace, figure):

        layout = (2, 1)

        figure.set_subplots(
            dimensions=workspace.display_data.dimensions, subplots=layout
        )

        figure.subplot_imshow(
            colormap="gray",
            image=workspace.display_data.x_data,
            title="Input Image",
            x=0,
            y=0,
        )

        figure.subplot_imshow_labels(
            image=workspace.display_data.y_data,
            sharexy=figure.subplot(0, 0),
            title=self.y_name.value,
            x=1,
            y=0,
        )


