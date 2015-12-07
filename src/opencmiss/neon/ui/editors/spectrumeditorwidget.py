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
from PySide import QtCore, QtGui

from opencmiss.zinc.spectrum import Spectrumcomponent

from opencmiss.neon.ui.editors.ui_spectrumeditorwidget import Ui_SpectrumEditorWidget
from opencmiss.neon.settings.mainsettings import FLOAT_STRING_FORMAT

COMPONENT_NAME_FORMAT = '{:d}. '
SPECTRUM_GLYPH_NAME_FORMAT = 'colour_bar_{0}'
SPECTRUM_DATA_ROLE = QtCore.Qt.UserRole + 1
REGION_DATA_ROLE = QtCore.Qt.UserRole + 2


class SpectrumEditorWidget(QtGui.QWidget):

    def __init__(self, parent=None, shared_context=None):
        super(SpectrumEditorWidget, self).__init__(parent)
        self._ui = Ui_SpectrumEditorWidget()
        self._ui.setupUi(self, shared_context)

        self._ui.comboBoxColourMap.addItems(extractColourMappingEnum())
        self._ui.comboBoxScale.addItems(extractScaleTypeEnum())

        self._selected_spectrum_row = -1
        self._selected_spectrum_components_row = -1
        self._empty_region = None
        self._updateUi()

        self._makeConnections()

    def _makeConnections(self):
        self._ui.pushButtonAddSpectrum.clicked.connect(self._addSpectrumClicked)
        self._ui.pushButtonDeleteSpectrum.clicked.connect(self._deleteSpectrumClicked)
        self._ui.pushButtonAddSpectrumComponent.clicked.connect(self._addSpectrumComponentClicked)
        self._ui.pushButtonDeleteSpectrumComponent.clicked.connect(self._deleteSpectrumComponentClicked)

        self._ui.listWidgetSpectrums.itemClicked.connect(self._spectrumItemClicked)
        self._ui.listWidgetSpectrums.itemChanged.connect(self._spectrumChanged)
        self._ui.checkBoxOverwrite.clicked.connect(self._overwriteClicked)
        self._ui.checkBoxDefault.clicked.connect(self._defaultClicked)

        self._ui.listWidgetSpectrumComponents.itemClicked.connect(self._spectrumComponentItemClicked)

        self._ui.pushButtonMoveDownSpectrumComponent.clicked.connect(self._moveDownSpectrumComponentClicked)
        self._ui.pushButtonMoveUpSpectrumComponent.clicked.connect(self._moveUpSpectrumComponentClicked)
        self._ui.comboBoxColourMap.currentIndexChanged.connect(self._colourMapIndexChanged)
        self._ui.comboBoxScale.currentIndexChanged.connect(self._scaleIndexChanged)
        self._ui.checkBoxReverse.clicked.connect(self._reverseClicked)

        self._ui.widget.graphicsInitialized.connect(self._graphicsInitialised)

    def _clearSpectrumUi(self):
        self._ui.listWidgetSpectrumComponents.clear()
        self._ui.checkBoxOverwrite.setChecked(False)
        self._clearSpectrumComponentUi()

    def _clearSpectrumComponentUi(self):
        self._ui.comboBoxColourMap.setCurrentIndex(0)
        self._ui.comboBoxScale.setCurrentIndex(0)
        self._ui.checkBoxReverse.setChecked(False)

    def _updateUi(self):
        self._clearSpectrumUi()
        spectrum_items = self._ui.listWidgetSpectrums.selectedItems()
        spectrum_selected = len(spectrum_items)

        self._ui.pushButtonDeleteSpectrum.setEnabled(spectrum_selected)
        self._ui.groupBoxPreview.setEnabled(spectrum_selected)
        self._ui.groupBoxSpectrumProperties.setEnabled(spectrum_selected)
        self._ui.groupBoxComponents.setEnabled(spectrum_selected)
        self._ui.groupBoxComponentProperties.setEnabled(spectrum_selected)

        if spectrum_selected:
            # Only one spectrum can be selected at a time.
            active_item = spectrum_items[0]
            s = active_item.data(SPECTRUM_DATA_ROLE)
            sm = self._ui.widget.getContext().getSpectrummodule()
            default_spectrum = s == sm.getDefaultSpectrum()
            self._ui.pushButtonDeleteSpectrum.setEnabled(not default_spectrum)
            self._ui.checkBoxDefault.setChecked(default_spectrum)
            self._ui.checkBoxOverwrite.setChecked(s.isMaterialOverwrite())
            sc = s.getFirstSpectrumcomponent()
            while sc.isValid():
                count = self._ui.listWidgetSpectrumComponents.count() + 1
                self._ui.listWidgetSpectrumComponents.addItem(createItem(getComponentString(sc, count), sc))
                sc = s.getNextSpectrumcomponent(sc)

            if self._ui.listWidgetSpectrumComponents.count():
                self._ui.listWidgetSpectrumComponents.setCurrentRow(0)

        self._updateComponentUi()

    def _updateComponentUi(self):
        spectrum_component_items = self._ui.listWidgetSpectrumComponents.selectedItems()
        spectrum_component_selected = len(spectrum_component_items)

        self._ui.pushButtonDeleteSpectrumComponent.setEnabled(spectrum_component_selected)
        self._ui.comboBoxColourMap.setEnabled(spectrum_component_selected)
        self._ui.pushButtonAutorange.setEnabled(spectrum_component_selected)
        self._ui.comboBoxScene.setEnabled(spectrum_component_selected)
        self._ui.comboBoxScale.setEnabled(spectrum_component_selected)
        self._ui.spinBoxDataFieldComponent.setEnabled(spectrum_component_selected)
        self._ui.checkBoxReverse.setEnabled(spectrum_component_selected)
        self._ui.lineEditRangeMin.setEnabled(spectrum_component_selected)
        self._ui.lineEditRangeMax.setEnabled(spectrum_component_selected)
        self._ui.lineEditNormalisedRangeMin.setEnabled(spectrum_component_selected)
        self._ui.lineEditNormalisedRangeMax.setEnabled(spectrum_component_selected)
        self._ui.pushButtonMoveDownSpectrumComponent.setEnabled(spectrum_component_selected)
        self._ui.pushButtonMoveUpSpectrumComponent.setEnabled(spectrum_component_selected)

        if spectrum_component_selected:
            active_spectrum_component = spectrum_component_items[0]
            sc = active_spectrum_component.data(SPECTRUM_DATA_ROLE)
            self._ui.comboBoxColourMap.setCurrentIndex(sc.getColourMappingType())
            self._ui.comboBoxScale.setCurrentIndex(sc.getScaleType())
            self._ui.spinBoxDataFieldComponent.setValue(sc.getFieldComponent())
            self._ui.checkBoxReverse.setChecked(sc.isColourReverse())
            self._ui.lineEditRangeMin.setText(FLOAT_STRING_FORMAT.format(sc.getRangeMinimum()))
            self._ui.lineEditRangeMax.setText(FLOAT_STRING_FORMAT.format(sc.getRangeMaximum()))
            self._ui.lineEditNormalisedRangeMin.setText(FLOAT_STRING_FORMAT.format(sc.getRangeMinimum()))
            self._ui.lineEditNormalisedRangeMax.setText(FLOAT_STRING_FORMAT.format(sc.getRangeMaximum()))
            row = self._ui.listWidgetSpectrumComponents.row(active_spectrum_component)
            self._ui.pushButtonMoveUpSpectrumComponent.setEnabled(row > 0)
            self._ui.pushButtonMoveDownSpectrumComponent.setEnabled(row < (self._ui.listWidgetSpectrumComponents.count() - 1))

            active_spectrum_component.setText(getComponentString(sc, row + 1))

    def _spectrumChanged(self, item):
        s = item.data(SPECTRUM_DATA_ROLE)
        s.setName(item.text())
        r = item.data(REGION_DATA_ROLE)
        scene = r.getScene()
        graphics = scene.getFirstGraphics()
        graphics.setName(SPECTRUM_GLYPH_NAME_FORMAT.foramt(s.getName()))

    def _spectrumItemClicked(self, item):
        lws = self._ui.listWidgetSpectrums
        selected_items = lws.selectedItems()
        if len(selected_items):
            if self._selected_spectrum_row == lws.row(item):
                self._ui.listWidgetSpectrums.clearSelection()
                self._selected_spectrum_row = -1
                self._ui.widget.getSceneviewer().setScene(self._empty_region.getScene())
            else:
                self._selected_spectrum_row = lws.row(item)
                region = item.data(REGION_DATA_ROLE)
                self._ui.widget.getSceneviewer().setScene(region.getScene())

        self._updateUi()

    def _spectrumComponentItemClicked(self, item):
        lwsc = self._ui.listWidgetSpectrumComponents
        selected_items = lwsc.selectedItems()
        if len(selected_items):
            if self._selected_spectrum_components_row == lwsc.row(item):
                self._ui.listWidgetSpectrumComponents.clearSelection()
                self._selected_spectrum_components_row = -1
                self._clearSpectrumComponentUi()
            else:
                self._selected_spectrum_components_row = lwsc.row(item)

        self._updateComponentUi()

    def _addSpectrumClicked(self):
        context = self._ui.widget.getContext()
        sm = context.getSpectrummodule()
        s = sm.createSpectrum()
        region = addPrivateSpectrumRegion(self._ui.widget.getContext(), s)
        self._ui.listWidgetSpectrums.addItem(createItem(s.getName(), s, True, region))
        self._updateUi()

    def _deleteSpectrumClicked(self):
        selected_items = self._ui.listWidgetSpectrums.selectedItems()
        if len(selected_items):
            active_spectrum = selected_items[0]
            self._ui.listWidgetSpectrums.takeItem(self._ui.listWidgetSpectrums.row(active_spectrum))

        self._updateUi()

    def _addSpectrumComponentClicked(self):
        selected_items = self._ui.listWidgetSpectrums.selectedItems()
        item = selected_items[0]
        s = item.data(SPECTRUM_DATA_ROLE)
        sc = s.createSpectrumcomponent()
        count = self._ui.listWidgetSpectrumComponents.count() + 1
        item = createItem(getComponentString(sc, count), sc)
        self._ui.listWidgetSpectrumComponents.addItem(item)
        item.setSelected(True)
        self._spectrumComponentItemClicked(item)
#         self._updateComponentUi()

    def _deleteSpectrumComponentClicked(self):
        selected_items = self._ui.listWidgetSpectrumComponents.selectedItems()
        if len(selected_items):
            self._ui.listWidgetSpectrumComponents.takeItem(self._ui.listWidgetSpectrumComponents.row(selected_items[0]))

        self._updateComponentUi()

    def _defaultClicked(self):
        active_item = self._ui.listWidgetSpectrums.selectedItems()[0]
        s = active_item.data(SPECTRUM_DATA_ROLE)
        sm = self._ui.widget.getContext().getSpectrummodule()
        sm.setDefaultSpectrum(s)

        self._updateUi()

    def _overwriteClicked(self):
        active_item = self._ui.listWidgetSpectrums.selectedItems()[0]
        s = active_item.data(SPECTRUM_DATA_ROLE)
        s.setMaterialOverwrite(self._ui.checkBoxOverwrite.isChecked())

    def _reverseClicked(self):
        selected_items = self._ui.listWidgetSpectrumComponents.selectedItems()
        if len(selected_items):
            active_item = selected_items[0]
            sc = active_item.data(SPECTRUM_DATA_ROLE)
            sc.setColourReverse(self._ui.checkBoxReverse.isChecked())

            self._updateComponentUi()

    def _colourMapIndexChanged(self, index):
        selected_items = self._ui.listWidgetSpectrumComponents.selectedItems()
        if len(selected_items):
            active_item = selected_items[0]
            sc = active_item.data(SPECTRUM_DATA_ROLE)
            sc.setColourMappingType(index)

            self._updateComponentUi()

    def _scaleIndexChanged(self, index):
        selected_items = self._ui.listWidgetSpectrumComponents.selectedItems()
        if len(selected_items):
            active_item = selected_items[0]
            sc = active_item.data(SPECTRUM_DATA_ROLE)
            sc.setScaleType(index)

            self._updateComponentUi()

    def _moveDownSpectrumComponentClicked(self):
        self._moveSpectrumComponent(1)

    def _moveSpectrumComponent(self, direction):
        selected_items = self._ui.listWidgetSpectrumComponents.selectedItems()
        if len(selected_items):
            active_item = selected_items[0]
            row = self._ui.listWidgetSpectrumComponents.row(active_item)
            next_row = row + direction
            self._ui.listWidgetSpectrumComponents.takeItem(row)
            self._ui.listWidgetSpectrumComponents.insertItem(next_row, active_item)
            item = self._ui.listWidgetSpectrumComponents.item(row)
            sc = item.data(SPECTRUM_DATA_ROLE)
            item.setText(getComponentString(sc, row + 1))
            self._ui.listWidgetSpectrumComponents.setCurrentRow(next_row)
            self._selected_spectrum_components_row = next_row

            self._updateComponentUi()

    def _moveUpSpectrumComponentClicked(self):
        self._moveSpectrumComponent(-1)

    def _graphicsInitialised(self):
        if self._ui.listWidgetSpectrums.count():
            self._ui.listWidgetSpectrums.setCurrentRow(0)
            first_item = self._ui.listWidgetSpectrums.item(0)
            self._spectrumItemClicked(first_item)

    def setContext(self, context):
        self._ui.widget.setContext(context)
        self._empty_region = context.createRegion()

        sm = context.getSpectrummodule()
        si = sm.createSpectrumiterator()
        s = si.next()
        while s.isValid():
            region = addPrivateSpectrumRegion(context, s)
            self._ui.listWidgetSpectrums.addItem(createItem(s.getName(), s, True, region))
            s = si.next()


INVALID_POSTFIX = '_INVALID'
COLOUR_MAPPING_PREFIX = 'COLOUR_MAPPING_TYPE_'
SCALE_TYPE_PREFIX = 'SCALE_TYPE_'
PRIVATE_SPECTRUM_FORMAT = 'spectrum_{0}'

from opencmiss.zinc.scenecoordinatesystem import SCENECOORDINATESYSTEM_NORMALISED_WINDOW_FILL as NORMALISED_WINDOW_FILL


def addPrivateSpectrumRegion(c, s):
    r = c.createRegion()
    scene = r.getScene()
    scene.beginChange()

    glyphmodule = scene.getGlyphmodule()

    graphics = scene.createGraphicsPoints()
    graphics.setScenecoordinatesystem(NORMALISED_WINDOW_FILL)
    attributes = graphics.getGraphicspointattributes()
    colour_bar = glyphmodule.createGlyphColourBar(s)
    colour_bar.setAxis([1, 0, 0])
    colour_bar.setSideAxis([0, 1, 0])
    colour_bar.setNumberFormat('%.2f')
    colour_bar.setName(SPECTRUM_GLYPH_NAME_FORMAT.format(s.getName()))
    attributes.setGlyph(colour_bar)
    attributes.setBaseSize(1.0)

    scene.endChange()
    return r


def createItem(name, data, editable=False, region=None):
    i = QtGui.QListWidgetItem(name)
    i.setData(SPECTRUM_DATA_ROLE, data)
    if editable:
        i.setFlags(i.flags() | QtCore.Qt.ItemIsEditable)
    if region is not None:
        i.setData(REGION_DATA_ROLE, region)

    return i


def getComponentString(sc, row):
    name = COMPONENT_NAME_FORMAT.format(row)
    name += ' ' + stringFromColourMappingInt(sc.getColourMappingType())
    name += ' ' + stringFromScaleInt(sc.getScaleType())
    if sc.isColourReverse():
        name += ' reverse'
    return name


def stringFromColourMappingInt(value):
    attr_dict = Spectrumcomponent.__dict__
    for key in attr_dict:
        if key.startswith(COLOUR_MAPPING_PREFIX) and attr_dict[key] == value:
            return key.replace(COLOUR_MAPPING_PREFIX, '').lower()

    return 'invalid'


def stringFromScaleInt(value):
    attr_dict = Spectrumcomponent.__dict__
    for key in attr_dict:
        if key.startswith(SCALE_TYPE_PREFIX) and attr_dict[key] == value:
            return key.replace(SCALE_TYPE_PREFIX, '').lower()

    return 'invalid'


def extractColourMappingEnum():
    enum = []
    attr_dict = Spectrumcomponent.__dict__
    for key in attr_dict:
        if key.startswith(COLOUR_MAPPING_PREFIX):
            if key.endswith(INVALID_POSTFIX):
                enum.append((attr_dict[key], '---'))
            else:
                enum.append((attr_dict[key], key.replace(COLOUR_MAPPING_PREFIX, '')))

    sorted_enum = sorted(enum)
    return [a[1] for a in sorted_enum]


def extractScaleTypeEnum():
    enum = []
    attr_dict = Spectrumcomponent.__dict__
    for key in attr_dict:
        if key.startswith(SCALE_TYPE_PREFIX):
            if key.endswith(INVALID_POSTFIX):
                enum.append((attr_dict[key], '---'))
            else:
                enum.append((attr_dict[key], key.replace(SCALE_TYPE_PREFIX, '')))

    sorted_enum = sorted(enum)
    return [a[1] for a in sorted_enum]
