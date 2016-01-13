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
from opencmiss.zinc.status import OK as ZINC_OK

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

        self._zincContext = None
        self._selected_spectrum_row = -1
        self._selected_spectrum_components_row = -1
        self._privateZincRegion = None
        self._privateZincScene = None
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
        self._ui.pushButtonAutorange.clicked.connect(self._autorangeClicked)

        self._ui.listWidgetSpectrumComponents.itemClicked.connect(self._spectrumComponentItemClicked)

        self._ui.pushButtonMoveDownSpectrumComponent.clicked.connect(self._moveDownSpectrumComponentClicked)
        self._ui.pushButtonMoveUpSpectrumComponent.clicked.connect(self._moveUpSpectrumComponentClicked)
        self._ui.comboBoxColourMap.currentIndexChanged.connect(self._colourMapIndexChanged)
        self._ui.checkBoxReverse.clicked.connect(self._reverseClicked)

        self._ui.spinBoxDataFieldComponent.valueChanged.connect(self._dataFieldComponentValueChanged)

        self._ui.lineEditDataRangeMin.editingFinished.connect(self._dataRangeMinEntered)
        self._ui.lineEditDataRangeMax.editingFinished.connect(self._dataRangeMaxEntered)
        self._ui.lineEditColourRangeMin.editingFinished.connect(self._colourRangeMinEntered)
        self._ui.lineEditColourRangeMax.editingFinished.connect(self._colourRangeMaxEntered)
        self._ui.checkBoxExtendBelow.clicked.connect(self._extendBelowClicked)
        self._ui.checkBoxExtendAbove.clicked.connect(self._extendAboveClicked)

        self._ui.comboBoxScale.currentIndexChanged.connect(self._scaleIndexChanged)
        self._ui.lineEditExaggeration.editingFinished.connect(self._exaggerationEntered)

        self._ui.sceneviewerWidgetPreview.graphicsInitialized.connect(self._graphicsInitialised)

    def _getCurrentSpectrum(self):
        active_item = self._ui.listWidgetSpectrums.selectedItems()[0]
        s = active_item.data(SPECTRUM_DATA_ROLE)
        return s

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
        spectrum_selected = (len(spectrum_items) > 0)

        self._ui.pushButtonDeleteSpectrum.setEnabled(spectrum_selected)
        self._ui.sceneviewerWidgetPreview.setEnabled(spectrum_selected)
        self._ui.groupBoxSpectrumProperties.setEnabled(spectrum_selected)
        self._ui.groupBoxComponents.setEnabled(spectrum_selected)
        self._ui.groupBoxComponentProperties.setEnabled(spectrum_selected)

        if spectrum_selected:
            # Only one spectrum can be selected at a time.
            active_item = spectrum_items[0]
            s = active_item.data(SPECTRUM_DATA_ROLE)
            sm = self._ui.sceneviewerWidgetPreview.getContext().getSpectrummodule()
            is_default_spectrum = (s == sm.getDefaultSpectrum())
            self._ui.pushButtonDeleteSpectrum.setEnabled(not is_default_spectrum)
            self._ui.checkBoxDefault.setChecked(is_default_spectrum)
            self._ui.checkBoxOverwrite.setChecked(s.isMaterialOverwrite())
            sc = s.getFirstSpectrumcomponent()
            while sc.isValid():
                count = self._ui.listWidgetSpectrumComponents.count() + 1
                self._ui.listWidgetSpectrumComponents.addItem(createItem(getComponentString(sc, count), sc))
                sc = s.getNextSpectrumcomponent(sc)

            if self._ui.listWidgetSpectrumComponents.count():
                self._ui.listWidgetSpectrumComponents.setCurrentRow(0)

        self._updateComponentUi()

    def _getCurrentSpectrumcomponent(self):
        spectrum_component_items = self._ui.listWidgetSpectrumComponents.selectedItems()
        if len(spectrum_component_items) > 0:
            active_item = spectrum_component_items[0]
            return active_item.data(SPECTRUM_DATA_ROLE)
        return None

    def _updateComponentUi(self):
        spectrum_component_items = self._ui.listWidgetSpectrumComponents.selectedItems()
        spectrum_component_selected = (len(spectrum_component_items) > 0)

        self._ui.pushButtonDeleteSpectrumComponent.setEnabled(spectrum_component_selected)
        self._ui.comboBoxColourMap.setEnabled(spectrum_component_selected)
        self._ui.pushButtonAutorange.setEnabled(spectrum_component_selected)
        self._ui.comboBoxScale.setEnabled(spectrum_component_selected)
        self._ui.spinBoxDataFieldComponent.setEnabled(spectrum_component_selected)
        self._ui.checkBoxReverse.setEnabled(spectrum_component_selected)
        self._ui.lineEditDataRangeMin.setEnabled(spectrum_component_selected)
        self._ui.lineEditDataRangeMax.setEnabled(spectrum_component_selected)
        self._ui.lineEditColourRangeMin.setEnabled(spectrum_component_selected)
        self._ui.lineEditColourRangeMax.setEnabled(spectrum_component_selected)
        self._ui.checkBoxExtendBelow.setEnabled(spectrum_component_selected)
        self._ui.checkBoxExtendAbove.setEnabled(spectrum_component_selected)
        self._ui.pushButtonMoveDownSpectrumComponent.setEnabled(spectrum_component_selected)
        self._ui.pushButtonMoveUpSpectrumComponent.setEnabled(spectrum_component_selected)

        if spectrum_component_selected:
            active_spectrum_component = spectrum_component_items[0]
            sc = active_spectrum_component.data(SPECTRUM_DATA_ROLE)
            self._ui.comboBoxColourMap.setCurrentIndex(sc.getColourMappingType())
            self._ui.spinBoxDataFieldComponent.setValue(sc.getFieldComponent())
            self._ui.checkBoxReverse.setChecked(sc.isColourReverse())
            self._ui.lineEditDataRangeMin.setText(FLOAT_STRING_FORMAT.format(sc.getRangeMinimum()))
            self._ui.lineEditDataRangeMax.setText(FLOAT_STRING_FORMAT.format(sc.getRangeMaximum()))
            self._ui.lineEditColourRangeMin.setText(FLOAT_STRING_FORMAT.format(sc.getColourMinimum()))
            self._ui.lineEditColourRangeMax.setText(FLOAT_STRING_FORMAT.format(sc.getColourMaximum()))
            self._ui.checkBoxExtendBelow.setChecked(sc.isExtendBelow())
            self._ui.checkBoxExtendAbove.setChecked(sc.isExtendAbove())
            self._ui.comboBoxScale.setCurrentIndex(sc.getScaleType())
            self._ui.lineEditExaggeration.setText(FLOAT_STRING_FORMAT.format(sc.getExaggeration()))

            row = self._ui.listWidgetSpectrumComponents.row(active_spectrum_component)
            self._ui.pushButtonMoveUpSpectrumComponent.setEnabled(row > 0)
            self._ui.pushButtonMoveDownSpectrumComponent.setEnabled(row < (self._ui.listWidgetSpectrumComponents.count() - 1))

            active_spectrum_component.setText(getComponentString(sc, row + 1))

    def _spectrumChanged(self, item):
        s = item.data(SPECTRUM_DATA_ROLE)
        s.setName(str(item.text()))
        r = item.data(REGION_DATA_ROLE)
        scene = r.getScene()
        graphics = scene.getFirstGraphics()
        graphics.setName(SPECTRUM_GLYPH_NAME_FORMAT.format(s.getName()))

    def _spectrumItemClicked(self, item):
        lws = self._ui.listWidgetSpectrums
        selected_items = lws.selectedItems()
        if len(selected_items):
            if self._selected_spectrum_row == lws.row(item):
                self._ui.listWidgetSpectrums.clearSelection()
                self._selected_spectrum_row = -1
                self._ui.sceneviewerWidgetPreview.getSceneviewer().setScene(self._privateZincRegion.getScene())
            else:
                self._selected_spectrum_row = lws.row(item)
                region = item.data(REGION_DATA_ROLE)
                self._ui.sceneviewerWidgetPreview.getSceneviewer().setScene(region.getScene())

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
        context = self._ui.sceneviewerWidgetPreview.getContext()
        sm = context.getSpectrummodule()
        s = sm.createSpectrum()
        region = addPrivateSpectrumRegion(self._ui.sceneviewerWidgetPreview.getContext(), s)
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

    def _deleteSpectrumComponentClicked(self):
        selected_items = self._ui.listWidgetSpectrumComponents.selectedItems()
        if len(selected_items):
            row = self._ui.listWidgetSpectrumComponents.row(selected_items[0])
            item = self._ui.listWidgetSpectrumComponents.takeItem(row)
            sc = item.data(SPECTRUM_DATA_ROLE)
            selected_spectrums = self._ui.listWidgetSpectrums.selectedItems()
            if len(selected_spectrums):
                s = selected_spectrums[0].data(SPECTRUM_DATA_ROLE)
                s.removeSpectrumcomponent(sc)

        self._updateComponentUi()

    def _defaultClicked(self):
        if self._ui.checkBoxDefault.isChecked():
            s = self._getCurrentSpectrum()
            sm = self._ui.sceneviewerWidgetPreview.getContext().getSpectrummodule()
            sm.setDefaultSpectrum(s)
        else:
            # Can't un-set default; need to make another one default
            self._ui.checkBoxDefault.setChecked(True)

    def _overwriteClicked(self):
        s = self._getCurrentSpectrum()
        s.setMaterialOverwrite(self._ui.checkBoxOverwrite.isChecked())

    def _autorangeClicked(self):
        """
        Autorange all components of spectrum.
        Maintains proportions of minimums and miximums for spectrum components
        Future: support fixing of minimum or maximum data range in spectrum components
        """
        s = self._getCurrentSpectrum()
        maxDataComponent = 0
        oldComponentMinimums = {}
        oldComponentMaximums = {}
        sc = s.getFirstSpectrumcomponent()
        while sc.isValid():
            dataComponent = sc.getFieldComponent()
            if dataComponent > maxDataComponent:
                maxDataComponent = dataComponent
            thisMinimum = sc.getRangeMinimum()
            thisMaximum = sc.getRangeMaximum()
            if (dataComponent not in oldComponentMinimums) or (thisMinimum < oldComponentMinimums[dataComponent]):
                oldComponentMinimums[dataComponent] = thisMinimum
            if (dataComponent not in oldComponentMaximums) or (thisMaximum < oldComponentMaximums[dataComponent]):
                oldComponentMaximums[dataComponent] = thisMaximum
            sc = s.getNextSpectrumcomponent(sc)
        region = self._zincContext.getDefaultRegion()
        scene = region.getScene()
        scenefiltermodule = self._zincContext.getScenefiltermodule()
        scenefilter = scenefiltermodule.getDefaultScenefilter()
        foundMaxDataComponent, minimumValues, maximumValues = scene.getSpectrumDataRange(scenefilter, s, maxDataComponent)
        # print("Data range: " + str(foundMaxDataComponent) + " values, minimum = " + str(minimumValues) + ", maximum = " + str(maximumValues))
        if foundMaxDataComponent > 0:
            # work around Zinc SWIG bindings returning scalars if 1 value
            if not type(minimumValues) is list:
                minimumValues = [minimumValues]
                maximumValues = [maximumValues]
            sc = s.getFirstSpectrumcomponent()
            while sc.isValid():
                dataComponent = sc.getFieldComponent()
                if (0 < dataComponent) and (dataComponent <= foundMaxDataComponent):
                    oldComponentRange =  oldComponentMaximums[dataComponent] - oldComponentMinimums[dataComponent]
                    thisMinimum = sc.getRangeMinimum()
                    thisMaximum = sc.getRangeMaximum()
                    minimumRatio = (thisMinimum - oldComponentMinimums[dataComponent]) / oldComponentRange
                    maximumRatio = (thisMaximum - oldComponentMinimums[dataComponent]) / oldComponentRange
                    dataMinimum = minimumValues[dataComponent - 1]
                    dataMaximum = maximumValues[dataComponent - 1]
                    newComponentRange = dataMaximum - dataMinimum
                    newComponentMinimum = dataMinimum + minimumRatio*newComponentRange
                    newComponentMaximum = dataMinimum + maximumRatio*newComponentRange
                    sc.setRangeMinimum(newComponentMinimum)
                    sc.setRangeMaximum(newComponentMaximum)
                sc = s.getNextSpectrumcomponent(sc)
        self._updateComponentUi()

    def _reverseClicked(self):
        selected_items = self._ui.listWidgetSpectrumComponents.selectedItems()
        if len(selected_items):
            active_item = selected_items[0]
            sc = active_item.data(SPECTRUM_DATA_ROLE)
            sc.setColourReverse(self._ui.checkBoxReverse.isChecked())

            self._updateComponentUi()

    def _dataFieldComponentValueChanged(self, value):
        selected_items = self._ui.listWidgetSpectrumComponents.selectedItems()
        if len(selected_items):
            active_item = selected_items[0]
            sc = active_item.data(SPECTRUM_DATA_ROLE)
            sc.setFieldComponent(value)

            self._updateComponentUi()

    def _colourMapIndexChanged(self, index):
        selected_items = self._ui.listWidgetSpectrumComponents.selectedItems()
        if len(selected_items):
            active_item = selected_items[0]
            sc = active_item.data(SPECTRUM_DATA_ROLE)
            sc.setColourMappingType(index)

            self._updateComponentUi()

    def _dataRangeMinEntered(self):
        sc = self._getCurrentSpectrumcomponent()
        try:
            valueText = self._ui.lineEditDataRangeMin.text()
            value = float(valueText)
            result = sc.setRangeMinimum(value)
            if result != ZINC_OK:
                raise ValueError("")
        except ValueError:
            print("Error setting spectrum component data range minimum")
        self._ui.lineEditDataRangeMin.setText(FLOAT_STRING_FORMAT.format(sc.getRangeMinimum()))

    def _dataRangeMaxEntered(self):
        sc = self._getCurrentSpectrumcomponent()
        try:
            valueText = self._ui.lineEditDataRangeMax.text()
            value = float(valueText)
            result = sc.setRangeMaximum(value)
            if result != ZINC_OK:
                raise ValueError("")
        except ValueError:
            print("Error setting spectrum component data range maximum")
        self._ui.lineEditDataRangeMax.setText(FLOAT_STRING_FORMAT.format(sc.getRangeMaximum()))

    def _colourRangeMinEntered(self):
        sc = self._getCurrentSpectrumcomponent()
        try:
            valueText = self._ui.lineEditColourRangeMin.text()
            value = float(valueText)
            result = sc.setColourMinimum(value)
            if result != ZINC_OK:
                raise ValueError("")
        except ValueError:
            print("Error setting spectrum component colour range minimum")
        self._ui.lineEditColourRangeMin.setText(FLOAT_STRING_FORMAT.format(sc.getColourMinimum()))

    def _colourRangeMaxEntered(self):
        sc = self._getCurrentSpectrumcomponent()
        try:
            valueText = self._ui.lineEditColourRangeMax.text()
            value = float(valueText)
            result = sc.setColourMaximum(value)
            if result != ZINC_OK:
                raise ValueError("")
        except ValueError:
            print("Error setting spectrum component colour range maximum")
        self._ui.lineEditColourRangeMax.setText(FLOAT_STRING_FORMAT.format(sc.getColourMaximum()))

    def _extendBelowClicked(self):
        sc = self._getCurrentSpectrumcomponent()
        sc.setExtendBelow(self._ui.checkBoxExtendBelow.isChecked())

    def _extendAboveClicked(self):
        sc = self._getCurrentSpectrumcomponent()
        sc.setExtendAbove(self._ui.checkBoxExtendAbove.isChecked())

    def _scaleIndexChanged(self, index):
        selected_items = self._ui.listWidgetSpectrumComponents.selectedItems()
        if len(selected_items):
            active_item = selected_items[0]
            sc = active_item.data(SPECTRUM_DATA_ROLE)
            sc.setScaleType(index)

            self._updateComponentUi()

    def _exaggerationEntered(self):
        sc = self._getCurrentSpectrumcomponent()
        try:
            valueText = self._ui.lineEditExaggeration.text()
            value = float(valueText)
            result = sc.setExaggeration(value)
            if result != ZINC_OK:
                raise ValueError("")
        except ValueError:
            print("Error setting log scale exaggeration")
        self._ui.lineEditExaggeration.setText(FLOAT_STRING_FORMAT.format(sc.getExaggeration()))

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

    def setZincContext(self, zincContext):
        self._zincContext = zincContext
        self._ui.sceneviewerWidgetPreview.setContext(zincContext)
        self._privateZincRegion = zincContext.createRegion()
        self._privateZincRegion.setName("Spectrum editor private region")
        self._privateZincScene = self._privateZincRegion.getScene()

        sm = zincContext.getSpectrummodule()
        si = sm.createSpectrumiterator()
        self._ui.listWidgetSpectrums.clear()
        s = si.next()
        while s.isValid():
            region = addPrivateSpectrumRegion(zincContext, s)
            result = region.setName("Spectrum editor private region for spectrum " + s.getName())
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
