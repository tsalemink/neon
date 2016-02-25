'''n
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

from opencmiss.neon.core.visualisations.base import BaseVisualisation


class Biomeng321Lab1(BaseVisualisation):

    def __init__(self):
        super(Biomeng321Lab1, self).__init__()
        self.setName('Bioemeng 321 Lab1 Visualisation')

    def visualise(self, document):
        node_filename = self._simulation.getNodeFilename()
        element_filename = self._simulation.getElementFilename()
        visualisation_description = default_visualisation
        visualisation_description['RootRegion']['Model']['Sources'][0]['FileName'] = node_filename
        visualisation_description['RootRegion']['Model']['Sources'][1]['FileName'] = element_filename
        state = json.dumps(visualisation_description)
        document.deserialize(state)

default_visualisation = {
  "OpenCMISS-Neon Version": [
    0,
    2,
    0
  ],
  "Project": "{\"problem\": \"{\\\"boundary_condition\\\": \\\"Model 4\\\"}\"}",
  "RootRegion": {
    "Model": {
      "Sources": [
        {
          "FileName": "../../tmp/biomeng321_lab1_cfoYB4.exnode",
          "Type": "FILE"
        },
        {
          "FileName": "../../tmp/biomeng321_lab1_cfoYB4.exelem",
          "Type": "FILE"
        }
      ]
    },
    "Scene": {
      "Graphics": [
        {
          "CoordinateField": "DeformedGeometry",
          "ElementFaceType": "ALL",
          "Exterior": False,
          "FieldDomainType": "MESH1D",
          "LineAttributes": {
            "BaseSize": [
              0.04,
              0.04
            ],
            "ScaleFactors": [
              1,
              1
            ],
            "ShapeType": "CIRCLE_EXTRUSION"
          },
          "Lines": {},
          "Material": "green",
          "RenderLineWidth": 1,
          "RenderPointSize": 1,
          "RenderPolygonMode": "RENDER_POLYGON_SHADED",
          "Scenecoordinatesystem": "LOCAL",
          "SelectMode": "ON",
          "SelectedMaterial": "default_selected",
          "Tessellation": "default",
          "Type": "LINES",
          "VisibilityFlag": True
        },
        {
          "CoordinateField": "Geometry",
          "ElementFaceType": "ALL",
          "Exterior": False,
          "FieldDomainType": "MESH1D",
          "LineAttributes": {
            "BaseSize": [
              0.02,
              0.02
            ],
            "ScaleFactors": [
              1,
              1
            ],
            "ShapeType": "CIRCLE_EXTRUSION"
          },
          "Lines": {},
          "Material": "red",
          "RenderLineWidth": 1,
          "RenderPointSize": 1,
          "RenderPolygonMode": "RENDER_POLYGON_SHADED",
          "Scenecoordinatesystem": "LOCAL",
          "SelectMode": "ON",
          "SelectedMaterial": "default_selected",
          "Tessellation": "default",
          "Type": "LINES",
          "VisibilityFlag": True
        },
        {
          "CoordinateField": "DeformedGeometry",
          "ElementFaceType": "ALL",
          "Exterior": False,
          "FieldDomainType": "NODES",
          "Material": "default",
          "PointAttributes": {
            "BaseSize": [
              1,
              1,
              1
            ],
            "Font": "default",
            "Glyph": "point",
            "GlyphOffset": [
              0,
              0,
              0
            ],
            "GlyphRepeatMode": "NONE",
            "GlyphShapeType": "POINT",
            "LabelField": "DeformedGeometry",
            "LabelOffset": [
              0.04,
              0.03,
              0
            ],
            "LabelText": [
              "",
              "",
              ""
            ],
            "ScaleFactors": [
              1,
              1,
              1
            ]
          },
          "Points": {},
          "RenderLineWidth": 1,
          "RenderPointSize": 1,
          "RenderPolygonMode": "RENDER_POLYGON_SHADED",
          "SamplingAttributes": {
            "ElementPointSamplingMode": "CELL_CENTRES",
            "Location": [
              0,
              0,
              0
            ]
          },
          "Scenecoordinatesystem": "LOCAL",
          "SelectMode": "ON",
          "SelectedMaterial": "default_selected",
          "Tessellation": "default_points",
          "Type": "POINTS",
          "VisibilityFlag": True
        },
        {
          "CoordinateField": "DeformedGeometry",
          "ElementFaceType": "ALL",
          "Exterior": False,
          "FieldDomainType": "NODES",
          "Material": "green",
          "PointAttributes": {
            "BaseSize": [
              0.04,
              0.04,
              0.04
            ],
            "Font": "default",
            "Glyph": "sphere",
            "GlyphOffset": [
              0,
              0,
              0
            ],
            "GlyphRepeatMode": "NONE",
            "GlyphShapeType": "SPHERE",
            "LabelOffset": [
              0,
              0,
              0
            ],
            "LabelText": [
              "",
              "",
              ""
            ],
            "ScaleFactors": [
              1,
              1,
              1
            ]
          },
          "Points": {},
          "RenderLineWidth": 1,
          "RenderPointSize": 1,
          "RenderPolygonMode": "RENDER_POLYGON_SHADED",
          "SamplingAttributes": {
            "ElementPointSamplingMode": "CELL_CENTRES",
            "Location": [
              0,
              0,
              0
            ]
          },
          "Scenecoordinatesystem": "LOCAL",
          "SelectMode": "ON",
          "SelectedMaterial": "default_selected",
          "Tessellation": "default_points",
          "Type": "POINTS",
          "VisibilityFlag": True
        },
        {
          "CoordinateField": "Geometry",
          "ElementFaceType": "ALL",
          "Exterior": False,
          "FieldDomainType": "NODES",
          "Material": "red",
          "PointAttributes": {
            "BaseSize": [
              0.02,
              0.02,
              0.02
            ],
            "Font": "default",
            "Glyph": "sphere",
            "GlyphOffset": [
              0,
              0,
              0
            ],
            "GlyphRepeatMode": "NONE",
            "GlyphShapeType": "SPHERE",
            "LabelOffset": [
              0,
              0,
              0
            ],
            "LabelText": [
              "",
              "",
              ""
            ],
            "ScaleFactors": [
              1,
              1,
              1
            ]
          },
          "Points": {},
          "RenderLineWidth": 1,
          "RenderPointSize": 1,
          "RenderPolygonMode": "RENDER_POLYGON_SHADED",
          "SamplingAttributes": {
            "ElementPointSamplingMode": "CELL_CENTRES",
            "Location": [
              0,
              0,
              0
            ]
          },
          "Scenecoordinatesystem": "LOCAL",
          "SelectMode": "ON",
          "SelectedMaterial": "default_selected",
          "Tessellation": "default_points",
          "Type": "POINTS",
          "VisibilityFlag": True
        }
      ],
      "VisibilityFlag": True
    }
  },
  "Spectrums": {
    "DefaultSpectrum": "default",
    "Spectrums": [
      {
        "Components": [
          {
            "Active": True,
            "BandedRatio": 0.2,
            "ColourMappingType": "RAINBOW",
            "ColourMaximum": 1,
            "ColourMinimum": 0,
            "ColourReverse": True,
            "Exaggeration": 1,
            "ExtendAbove": True,
            "ExtendBelow": True,
            "FieldComponent": 1,
            "NumberOfBands": 10,
            "RangeMaximum": 1,
            "RangeMinimum": 0,
            "ScaleType": "LINEAR",
            "StepValue": 0.5
          }
        ],
        "MaterialOverwrite": True,
        "Name": "default"
      }
    ]
  },
  "Tessellations": {
    "DefaultPointsTessellation": "default_points",
    "DefaultTessellation": "default",
    "Tessellations": [
      {
        "CircleDivisions": 12,
        "MinimumDivisions": [
          1
        ],
        "Name": "default",
        "RefinementFactors": [
          4
        ]
      },
      {
        "CircleDivisions": 12,
        "MinimumDivisions": [
          1
        ],
        "Name": "default_points",
        "RefinementFactors": [
          1
        ]
      }
    ]
  }
}

old_new_visualisation = {
  "OpenCMISS-Neon Version": [
    0,
    1,
    0
  ],
  "RootRegion": {
    "Model": {
      "Sources": [
        {
          "FileName": "../../tmp/biomeng321_lab1_fo00Ty.exnode",
          "Type": "FILE"
        },
        {
          "FileName": "../../tmp/biomeng321_lab1_fo00Ty.exelem",
          "Type": "FILE"
        }
      ]
    },
    "Scene": {
      "Graphics": [
        {
          "CoordinateField": "DeformedGeometry",
          "ElementFaceType": "ALL",
          "Exterior": False,
          "FieldDomainType": "MESH1D",
          "LineAttributes": {
            "BaseSize": [
              0.04,
              0.04
            ],
            "ScaleFactors": [
              1,
              1
            ],
            "ShapeType": "CIRCLE_EXTRUSION"
          },
          "Lines": {},
          "Material": "green",
          "RenderLineWidth": 1,
          "RenderPointSize": 1,
          "RenderPolygonMode": "RENDER_POLYGON_SHADED",
          "Scenecoordinatesystem": "LOCAL",
          "SelectMode": "ON",
          "SelectedMaterial": "default_selected",
          "Tessellation": "default",
          "Type": "LINES",
          "VisibilityFlag": True
        },
        {
          "CoordinateField": "Geometry",
          "ElementFaceType": "ALL",
          "Exterior": False,
          "FieldDomainType": "MESH1D",
          "LineAttributes": {
            "BaseSize": [
              0.02,
              0.02
            ],
            "ScaleFactors": [
              1,
              1
            ],
            "ShapeType": "CIRCLE_EXTRUSION"
          },
          "Lines": {},
          "Material": "red",
          "RenderLineWidth": 1,
          "RenderPointSize": 1,
          "RenderPolygonMode": "RENDER_POLYGON_SHADED",
          "Scenecoordinatesystem": "LOCAL",
          "SelectMode": "ON",
          "SelectedMaterial": "default_selected",
          "Tessellation": "default",
          "Type": "LINES",
          "VisibilityFlag": True
        },
        {
          "CoordinateField": "DeformedGeometry",
          "ElementFaceType": "ALL",
          "Exterior": False,
          "FieldDomainType": "NODES",
          "Material": "default",
          "PointAttributes": {
            "BaseSize": [
              1,
              1,
              1
            ],
            "Font": "default",
            "Glyph": "point",
            "GlyphOffset": [
              0,
              0,
              0
            ],
            "GlyphRepeatMode": "NONE",
            "GlyphShapeType": "POINT",
            "LabelField": "DeformedGeometry",
            "LabelOffset": [
              0.04,
              0.03,
              0
            ],
            "LabelText": [
              "",
              "",
              ""
            ],
            "ScaleFactors": [
              1,
              1,
              1
            ]
          },
          "Points": {},
          "RenderLineWidth": 1,
          "RenderPointSize": 1,
          "RenderPolygonMode": "RENDER_POLYGON_SHADED",
          "SamplingAttributes": {
            "ElementPointSamplingMode": "CELL_CENTRES",
            "Location": [
              0,
              0,
              0
            ]
          },
          "Scenecoordinatesystem": "LOCAL",
          "SelectMode": "ON",
          "SelectedMaterial": "default_selected",
          "Tessellation": "default_points",
          "Type": "POINTS",
          "VisibilityFlag": True
        }
      ],
      "VisibilityFlag": True
    }
  },
  "Spectrums": {
    "DefaultSpectrum": "default",
    "Spectrums": [
      {
        "Components": [
          {
            "Active": True,
            "BandedRatio": 0.2,
            "ColourMappingType": "RAINBOW",
            "ColourMaximum": 1,
            "ColourMinimum": 0,
            "ColourReverse": True,
            "Exaggeration": 1,
            "ExtendAbove": True,
            "ExtendBelow": True,
            "FieldComponent": 1,
            "NumberOfBands": 10,
            "RangeMaximum": 1,
            "RangeMinimum": 0,
            "ScaleType": "LINEAR",
            "StepValue": 0.5
          }
        ],
        "MaterialOverwrite": True,
        "Name": "default"
      }
    ]
  },
  "Tessellations": {
    "DefaultPointsTessellation": "default_points",
    "DefaultTessellation": "default",
    "Tessellations": [
      {
        "CircleDivisions": 12,
        "MinimumDivisions": [
          1
        ],
        "Name": "default",
        "RefinementFactors": [
          4
        ]
      },
      {
        "CircleDivisions": 12,
        "MinimumDivisions": [
          1
        ],
        "Name": "default_points",
        "RefinementFactors": [
          1
        ]
      }
    ]
  }
}


old_default_visualisation = {
  "OpenCMISS-Neon Version": [
    0,
    1,
    0
  ],
  "RootRegion": {
    "Model": {
      "Sources": [
        {
          "FileName": "../../tmp/biomeng321_lab1_I1rLR4.exnode",
          "Type": "FILE"
        },
        {
          "FileName": "../../tmp/biomeng321_lab1_YV4L4v.exelem",
          "Type": "FILE"
        }
      ]
    },
    "Scene": {
      "Graphics": [
        {
          "CoordinateField": "DeformedGeometry",
          "ElementFaceType": "ALL",
          "Exterior": False,
          "FieldDomainType": "MESH1D",
          "LineAttributes": {
            "BaseSize": [
              0,
              0
            ],
            "ScaleFactors": [
              1,
              1
            ],
            "ShapeType": "LINE"
          },
          "Lines": {},
          "Material": "gold",
          "RenderLineWidth": 1,
          "RenderPointSize": 1,
          "RenderPolygonMode": "RENDER_POLYGON_SHADED",
          "Scenecoordinatesystem": "LOCAL",
          "SelectMode": "ON",
          "SelectedMaterial": "default_selected",
          "Tessellation": "default",
          "Type": "LINES",
          "VisibilityFlag": True
        },
        {
          "CoordinateField": "Geometry",
          "ElementFaceType": "ALL",
          "Exterior": False,
          "FieldDomainType": "MESH1D",
          "LineAttributes": {
            "BaseSize": [
              0,
              0
            ],
            "ScaleFactors": [
              1,
              1
            ],
            "ShapeType": "LINE"
          },
          "Lines": {},
          "Material": "blue",
          "RenderLineWidth": 1,
          "RenderPointSize": 1,
          "RenderPolygonMode": "RENDER_POLYGON_SHADED",
          "Scenecoordinatesystem": "LOCAL",
          "SelectMode": "ON",
          "SelectedMaterial": "default_selected",
          "Tessellation": "default",
          "Type": "LINES",
          "VisibilityFlag": True
        }
      ],
      "VisibilityFlag": True
    }
  },
  "Spectrums": {
    "DefaultSpectrum": "default",
    "Spectrums": [
      {
        "Components": [
          {
            "Active": True,
            "BandedRatio": 0.2,
            "ColourMappingType": "RAINBOW",
            "ColourMaximum": 1,
            "ColourMinimum": 0,
            "ColourReverse": True,
            "Exaggeration": 1,
            "ExtendAbove": True,
            "ExtendBelow": True,
            "FieldComponent": 1,
            "NumberOfBands": 10,
            "RangeMaximum": 1,
            "RangeMinimum": 0,
            "ScaleType": "LINEAR",
            "StepValue": 0.5
          }
        ],
        "MaterialOverwrite": True,
        "Name": "default"
      }
    ]
  },
  "Tessellations": {
    "DefaultPointsTessellation": "default_points",
    "DefaultTessellation": "default",
    "Tessellations": [
      {
        "CircleDivisions": 12,
        "MinimumDivisions": [
          1
        ],
        "Name": "default",
        "RefinementFactors": [
          4
        ]
      },
      {
        "CircleDivisions": 12,
        "MinimumDivisions": [
          1
        ],
        "Name": "default_points",
        "RefinementFactors": [
          1
        ]
      }
    ]
  }
}
