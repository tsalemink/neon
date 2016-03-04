'''
   Copyright 2015 University of Auckland

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
import json


class NeonSceneviewer(object):

    def __init__(self, zinc_context, parent=None):
        self._zinc_context = zinc_context
        self._parent = parent
        self._anti_alias_sampling = default_anti_alias_sampling
        self._background_colour_RGB = default_background_colour_RGB
        self._eye_position = default_eye_position
        self._far_clipping_plane = default_far_clipping_plane
        self._lighting_local_viewer = default_lighting_local_viewer
        self._lighting_two_sided = default_lighting_two_sided
        self._lookat_position = default_lookat_position
        self._near_clipping_plane = default_near_clipping_plane
        self._perturb_lines_flag = default_perturb_lines_flag
        self._project_mode = default_project_mode
        self._scene = default_scene
        self._scene_filter = default_scene_filter
        self._translation_rate = default_translation_rate
        self._transparency_mode = default_transparency_mode
        self._tumble_rate = default_tumble_rate
        self._up_vector = default_up_vector
        self._view_angle = default_view_angle
        self._zoom_rate = default_zoom_rate

    def deserialize(self, d):
        # d = json.loads(s)
        self._anti_alias_sampling = d["AntialiasSampling"] if "AntialiasSampling" in d else default_anti_alias_sampling
        self._background_colour_RGB = d["BackgroundColourRGB"] if "BackgroundColourRGB" in d else default_background_colour_RGB
        self._eye_position = d["EyePosition"] if "EyePosition" in d else default_eye_position
        self._far_clipping_plane = d["FarClippingPlane"] if "FarClippingPlane" in d else default_far_clipping_plane
        self._lighting_local_viewer = d["LightingLocalViewer"] if "LightingLocalViewer" in d else default_lighting_local_viewer
        self._lighting_two_sided = d["LightingTwoSided"] if "LightingTwoSided" in d else default_lighting_two_sided
        self._lookat_position = d["LookatPosition"] if "LookatPosition" in d else default_lookat_position
        self._near_clipping_plane = d["NearClippingPlane"] if "NearClippingPlane" in d else default_near_clipping_plane
        self._perturb_lines_flag = d["PerturbLinesFlag"] if "PerturbLinesFlag" in d else default_perturb_lines_flag
        self._project_mode = d["ProjectionMode"] if "ProjectionMode" in d else default_project_mode
        self._scene = d["Scene"] if "Scene" in d else default_scene
        self._scene_filter = d["Scenefilter"] if "Scenefilter" in d else default_scene_filter
        self._translation_rate = d["TranslationRate"] if "TranslationRate" in d else default_translation_rate
        self._transparency_mode = d["TransparencyMode"] if "TransparencyMode" in d else default_transparency_mode
        self._tumble_rate = d["TumbleRate"] if "TumbleRate" in d else default_tumble_rate
        self._up_vector = d["UpVector"] if "UpVector" in d else default_up_vector
        self._view_angle = d["ViewAngle"] if "ViewAngle" in d else default_view_angle
        self._zoom_rate = d["ZoomRate"] if "ZoomRate" in d else default_zoom_rate

    def serialize(self):
        d = {}
        d["AntialiasSampling"] = self._anti_alias_sampling
        d["BackgroundColourRGB"] = self._background_colour_RGB
        d["EyePosition"] = self._eye_position
        d["FarClippingPlane"] = self._far_clipping_plane
        d["LightingLocalViewer"] = self._lighting_local_viewer
        d["LightingTwoSided"] = self._lighting_two_sided
        d["LookatPosition"] = self._lookat_position
        d["NearClippingPlane"] = self._near_clipping_plane
        d["PerturbLinesFlag"] = self._perturb_lines_flag
        d["ProjectionMode"] = self._project_mode
        d["Scene"] = self._scene
        d["Scenefilter"] = self._scene_filter
        d["TranslationRate"] = self._translation_rate
        d["TransparencyMode"] = self._transparency_mode
        d["TumbleRate"] = self._tumble_rate
        d["UpVector"] = self._up_vector
        d["ViewAngle"] = self._view_angle
        d["ZoomRate"] = self._zoom_rate
        return d


default_anti_alias_sampling = 0
default_background_colour_RGB = [0, 0, 0]
default_eye_position = [0, 0, 3.88551982890656]
default_far_clipping_plane = 7.88551982890656
default_lighting_local_viewer = False
default_lighting_two_sided = True
default_lookat_position = [0, 0, 0]
default_near_clipping_plane = 0.1942759914453282
default_perturb_lines_flag = False
default_project_mode = "PERSPECTIVE"
default_scene = "/"
default_scene_filter = "default"
default_translation_rate = 1
default_transparency_mode = "FAST"
default_tumble_rate = 1.5
default_up_vector = [0, 1, 0]
default_view_angle = 0.6981317007977318
default_zoom_rate = 1
