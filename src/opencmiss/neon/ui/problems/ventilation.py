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
import os.path

from PySide import QtGui

from opencmiss.neon.ui.problems.base import BaseProblem
from opencmiss.neon.core.problems.constants import RespirationConstants
from opencmiss.neon.ui.problems.ui_ventilationwidget import Ui_VentilationWidget
from opencmiss.neon.core.problems.ventilation import getExecutableForPlatform


class Ventilation(BaseProblem):

    def __init__(self, parent=None):
        super(Ventilation, self).__init__(parent)
        self._ui = Ui_VentilationWidget()
        self._ui.setupUi(self)
        self._setupUi()

        self._location = None

        self._createMaps()

        self._makeConnections()

    def _setupUi(self):
        enums = []
        self._ui.tabWidget.setCurrentIndex(2)
        self._ui.comboBoxExpirationType.clear()
        class_attributes = RespirationConstants.ExpirationType.__dict__
        for a in class_attributes:
            if not a.startswith('__'):
                enums.append((class_attributes[a], a))

        enums = sorted(enums)
        self._map_expiration_index_to_string = {e[0]: e[1].lower() for e in enums}
        self._map_string_to_expiration_index = {e[1].lower(): e[0] for e in enums}
        self._ui.comboBoxExpirationType.addItems([e[1] for e in enums])

    def _createMaps(self):
        self._map_keys_to_ui = {}
        self._map_ui_to_keys = {}
        self._map_chooser_to_line_edit = {}

        # The executable ui is not added to the map, it is dealt with separately
        # File input outputs
        self._map_keys_to_ui['tree_inbuilt'] = self._ui.checkBoxInBuiltTree
        self._map_ui_to_keys[self._ui.checkBoxInBuiltTree] = 'tree_inbuilt'
        self._map_keys_to_ui['tree_ipelem'] = self._ui.lineEditIpElem
        self._map_ui_to_keys[self._ui.lineEditIpElem] = 'tree_ipelem'
        self._map_keys_to_ui['tree_ipnode'] = self._ui.lineEditIpNode
        self._map_ui_to_keys[self._ui.lineEditIpNode] = 'tree_ipnode'
        self._map_keys_to_ui['tree_ipfield'] = self._ui.lineEditIpField
        self._map_ui_to_keys[self._ui.lineEditIpField] = 'tree_ipfield'
        self._map_keys_to_ui['tree_ipmesh'] = self._ui.lineEditIpMesh
        self._map_ui_to_keys[self._ui.lineEditIpMesh] = 'tree_ipmesh'
        self._map_keys_to_ui['flow_inbuilt'] = self._ui.checkBoxInBuiltFlow
        self._map_ui_to_keys[self._ui.checkBoxInBuiltFlow] = 'flow_inbuilt'
        self._map_keys_to_ui['flow_exelem'] = self._ui.lineEditFlow
        self._map_ui_to_keys[self._ui.lineEditFlow] = 'flow_exelem'
        self._map_keys_to_ui['terminal_exnode'] = self._ui.lineEditTerminalExNode
        self._map_ui_to_keys[self._ui.lineEditTerminalExNode] = 'terminal_exnode'
        self._map_keys_to_ui['tree_exnode'] = self._ui.lineEditTreeExNode
        self._map_ui_to_keys[self._ui.lineEditTreeExNode] = 'tree_exnode'
        self._map_keys_to_ui['tree_exelem'] = self._ui.lineEditTreeExElem
        self._map_ui_to_keys[self._ui.lineEditTreeExElem] = 'tree_exelem'
        self._map_keys_to_ui['ventilation_exelem'] = self._ui.lineEditVentilationExElem
        self._map_ui_to_keys[self._ui.lineEditVentilationExElem] = 'ventilation_exelem'
        self._map_keys_to_ui['radius_exelem'] = self._ui.lineEditRadiusExElem
        self._map_ui_to_keys[self._ui.lineEditRadiusExElem] = 'radius_exelem'

        # Main parameters
        self._map_keys_to_ui['dt'] = self._ui.doubleSpinBoxTimeStep
        self._map_ui_to_keys[self._ui.doubleSpinBoxTimeStep] = 'dt'
        self._map_keys_to_ui['num_itns'] = self._ui.spinBoxNumberOfIterations
        self._map_ui_to_keys[self._ui.spinBoxNumberOfIterations] = 'num_itns'
        self._map_keys_to_ui['num_brths'] = self._ui.spinBoxNumberOfBreaths
        self._map_ui_to_keys[self._ui.spinBoxNumberOfBreaths] = 'num_brths'
        self._map_keys_to_ui['err_tol'] = self._ui.doubleSpinBoxErrorTolerance
        self._map_ui_to_keys[self._ui.doubleSpinBoxErrorTolerance] = 'err_tol'

        # Flow parameters
        self._map_keys_to_ui['FRC'] = self._ui.doubleSpinBoxFRC
        self._map_ui_to_keys[self._ui.doubleSpinBoxFRC] = 'FRC'
        self._map_keys_to_ui['constrict'] = self._ui.doubleSpinBoxConstrict
        self._map_ui_to_keys[self._ui.doubleSpinBoxConstrict] = 'constrict'
        self._map_keys_to_ui['T_interval'] = self._ui.doubleSpinBoxTInterval
        self._map_ui_to_keys[self._ui.doubleSpinBoxTInterval] = 'T_interval'
        self._map_keys_to_ui['Gdirn'] = self._ui.spinBoxGdirn
        self._map_ui_to_keys[self._ui.spinBoxGdirn] = 'Gdirn'
        self._map_keys_to_ui['press_in'] = self._ui.doubleSpinBoxPressIn
        self._map_ui_to_keys[self._ui.doubleSpinBoxPressIn] = 'press_in'
        self._map_keys_to_ui['COV'] = self._ui.doubleSpinBoxCOV
        self._map_ui_to_keys[self._ui.doubleSpinBoxCOV] = 'COV'
        self._map_keys_to_ui['RMaxMean'] = self._ui.doubleSpinBoxRMaxMean
        self._map_ui_to_keys[self._ui.doubleSpinBoxRMaxMean] = 'RMaxMean'
        self._map_keys_to_ui['RMinMean'] = self._ui.doubleSpinBoxRMinMean
        self._map_ui_to_keys[self._ui.doubleSpinBoxRMinMean] = 'RMinMean'
        self._map_keys_to_ui['i_to_e_ratio'] = self._ui.doubleSpinBoxIERatio
        self._map_ui_to_keys[self._ui.doubleSpinBoxIERatio] = 'i_to_e_ratio'
        self._map_keys_to_ui['refvol'] = self._ui.doubleSpinBoxRefVolume
        self._map_ui_to_keys[self._ui.doubleSpinBoxRefVolume] = 'refvol'
        self._map_keys_to_ui['volume_target'] = self._ui.doubleSpinBoxVolumeTarget
        self._map_ui_to_keys[self._ui.doubleSpinBoxVolumeTarget] = 'volume_target'
        self._map_keys_to_ui['pmus_step'] = self._ui.doubleSpinBoxPMusStep
        self._map_ui_to_keys[self._ui.doubleSpinBoxPMusStep] = 'pmus_step'
        self._map_keys_to_ui['expiration_type'] = self._ui.comboBoxExpirationType
        self._map_ui_to_keys[self._ui.comboBoxExpirationType] = 'expiration_type'
        self._map_keys_to_ui['chest_wall_compliance'] = self._ui.doubleSpinBoxChestWallCompliance
        self._map_ui_to_keys[self._ui.doubleSpinBoxChestWallCompliance] = 'chest_wall_compliance'

        # Chooser button buddies
        self._map_chooser_to_line_edit[self._ui.pushButtonChooseExecutable] = self._ui.lineEditExecutable
        self._map_chooser_to_line_edit[self._ui.pushButtonChooseTreeExElem] = self._ui.lineEditTreeExElem
        self._map_chooser_to_line_edit[self._ui.pushButtonChooseTreeExNode] = self._ui.lineEditTreeExNode
        self._map_chooser_to_line_edit[self._ui.pushButtonChooseFlow] = self._ui.lineEditFlow
        self._map_chooser_to_line_edit[self._ui.pushButtonChooseIpElem] = self._ui.lineEditIpElem
        self._map_chooser_to_line_edit[self._ui.pushButtonChooseIpField] = self._ui.lineEditIpField
        self._map_chooser_to_line_edit[self._ui.pushButtonChooseIpNode] = self._ui.lineEditIpNode
        self._map_chooser_to_line_edit[self._ui.pushButtonChooseIpMesh] = self._ui.lineEditIpMesh
        self._map_chooser_to_line_edit[self._ui.pushButtonChooseTerminalExNode] = self._ui.lineEditTerminalExNode
        self._map_chooser_to_line_edit[self._ui.pushButtonChooseVentilationExElem] = self._ui.lineEditVentilationExElem
        self._map_chooser_to_line_edit[self._ui.pushButtonChooseRadiusExElem] = self._ui.lineEditRadiusExElem

    def _makeConnections(self):
        self._ui.pushButtonChooseExecutable.clicked.connect(self._executableChooserClicked)

        self._ui.pushButtonChooseTreeExElem.clicked.connect(self._chooserClicked)
        self._ui.pushButtonChooseTreeExNode.clicked.connect(self._chooserClicked)
        self._ui.pushButtonChooseFlow.clicked.connect(self._chooserClicked)
        self._ui.pushButtonChooseIpElem.clicked.connect(self._chooserClicked)
        self._ui.pushButtonChooseIpField.clicked.connect(self._chooserClicked)
        self._ui.pushButtonChooseIpNode.clicked.connect(self._chooserClicked)
        self._ui.pushButtonChooseIpMesh.clicked.connect(self._chooserClicked)
        self._ui.pushButtonChooseTerminalExNode.clicked.connect(self._chooserClicked)
        self._ui.pushButtonChooseVentilationExElem.clicked.connect(self._chooserClicked)
        self._ui.pushButtonChooseRadiusExElem.clicked.connect(self._chooserClicked)

        self._ui.checkBoxInBuiltExecutable.clicked.connect(self._inBuiltExecutableClicked)
        self._ui.lineEditExecutable.editingFinished.connect(self._executableLocationChanged)
        self._ui.checkBoxInBuiltFlow.clicked.connect(self._inBuiltFlowClicked)
        self._ui.checkBoxInBuiltTree.clicked.connect(self._inBuiltTreeClicked)

        # Main parameters
        self._ui.doubleSpinBoxTimeStep.valueChanged.connect(self._updateMainParameterValue)
        self._ui.spinBoxNumberOfIterations.valueChanged.connect(self._updateMainParameterValue)
        self._ui.spinBoxNumberOfBreaths.valueChanged.connect(self._updateMainParameterValue)
        self._ui.doubleSpinBoxErrorTolerance.valueChanged.connect(self._updateMainParameterValue)

        # Flow parameters
        self._ui.doubleSpinBoxFRC.valueChanged.connect(self._updateFlowParameterValue)
        self._ui.doubleSpinBoxConstrict.valueChanged.connect(self._updateFlowParameterValue)
        self._ui.doubleSpinBoxTInterval.valueChanged.connect(self._updateFlowParameterValue)
        self._ui.spinBoxGdirn.valueChanged.connect(self._updateFlowParameterValue)
        self._ui.doubleSpinBoxPressIn.valueChanged.connect(self._updateFlowParameterValue)
        self._ui.doubleSpinBoxCOV.valueChanged.connect(self._updateFlowParameterValue)
        self._ui.doubleSpinBoxRMaxMean.valueChanged.connect(self._updateFlowParameterValue)
        self._ui.doubleSpinBoxRMinMean.valueChanged.connect(self._updateFlowParameterValue)
        self._ui.doubleSpinBoxIERatio.valueChanged.connect(self._updateFlowParameterValue)
        self._ui.doubleSpinBoxRefVolume.valueChanged.connect(self._updateFlowParameterValue)
        self._ui.doubleSpinBoxVolumeTarget.valueChanged.connect(self._updateFlowParameterValue)
        self._ui.doubleSpinBoxPMusStep.valueChanged.connect(self._updateFlowParameterValue)
        self._ui.comboBoxExpirationType.currentIndexChanged.connect(self._updateFlowParameterValue)
        self._ui.doubleSpinBoxChestWallCompliance.valueChanged.connect(self._updateFlowParameterValue)

    def _inBuiltExecutableClicked(self):
        state = self._ui.checkBoxInBuiltExecutable.isChecked()
        self._ui.lineEditExecutable.setEnabled(not state)
        self._ui.pushButtonChooseExecutable.setEnabled(not state)
        if state:
            self._ui.lineEditExecutable.clear()
            self._problem.setInBuiltExecutable(getExecutableForPlatform())

    def _inBuiltFlowClicked(self):
        state = self._ui.checkBoxInBuiltFlow.isChecked()
        key = self._map_ui_to_keys[self._ui.checkBoxInBuiltFlow]
        self._problem.updateFileInputOutputs({key: state})
        self._ui.lineEditFlow.setEnabled(not state)
        self._ui.pushButtonChooseFlow.setEnabled(not state)

    def _inBuiltTreeClicked(self):
        state = self._ui.checkBoxInBuiltTree.isChecked()
        key = self._map_ui_to_keys[self._ui.checkBoxInBuiltTree]
        self._problem.updateFileInputOutputs({key: state})
        self._ui.lineEditIpElem.setEnabled(not state)
        self._ui.pushButtonChooseIpElem.setEnabled(not state)
        self._ui.lineEditIpField.setEnabled(not state)
        self._ui.pushButtonChooseIpField.setEnabled(not state)
        self._ui.lineEditIpNode.setEnabled(not state)
        self._ui.pushButtonChooseIpNode.setEnabled(not state)

    def _isEnumParameter(self, parameter):
        enum_parameters = ['expiration_type']

        return parameter in enum_parameters

    def _isCheckBox(self, key):
        check_boxes = ['tree_inbuilt', 'flow_inbuilt']

        return key in check_boxes

    def _isOutputFile(self, key):
        output_files = ['terminal_exnode', 'tree_exnode', 'tree_exelem', 'ventilation_exelem', 'radius_exelem']

        return key in output_files

    def _updateExecutableParameters(self):
        state = self._problem.isInBuiltExecutable()
        self._ui.checkBoxInBuiltExecutable.setChecked(state)
        self._inBuiltExecutableClicked()
        if not state:
            self._ui.lineEditExecutable.setText(self._problem.getExecutable())

    def _updateFileInputOutputs(self):
        p = self._problem.getFileInputOutputs()
        for k in p:
            ui = self._map_keys_to_ui[k]
            if self._isCheckBox(k):
                ui.setChecked(p[k])
            else:
                ui.setText(p[k])

        self._inBuiltFlowClicked()
        self._inBuiltTreeClicked()

    def _updateMainParameters(self):
        p = self._problem.getMainParameters()
        for k in p:
            ui = self._map_keys_to_ui[k]
            ui.setValue(p[k])

    def _updateFlowParameters(self):
        p = self._problem.getFlowParameters()
        for k in p:
            ui = self._map_keys_to_ui[k]
            if self._isEnumParameter(k):
                ui.setCurrentIndex(self._map_string_to_expiration_index[p[k]])
            else:
                ui.setValue(p[k])

    def _executableLocationChanged(self):
        self._problem.setExecutable(self._ui.lineEditExecutable.text())

    def _executableChooserClicked(self):
        sender = self.sender()
        line_edit = self._map_chooser_to_line_edit[sender]
        text = line_edit.text()
        location = os.path.dirname(text) if text else self._location if self._location is not None else os.path.expanduser("~")
        filename, _ = QtGui.QFileDialog.getOpenFileName(self, caption='Choose executable ...', dir=location,
                                                        filter="Executable (*.exe *);;All (*.* *)")
        if filename:
            self._location = os.path.dirname(filename)
            self._problem.setExecutable(filename)
            line_edit.setText(filename)

    def _chooserClicked(self):
        sender = self.sender()
        line_edit = self._map_chooser_to_line_edit[sender]
        key = self._map_ui_to_keys[line_edit]
        text = line_edit.text()
        location = os.path.dirname(text) if text else self._location if self._location is not None else os.path.expanduser("~")
        if self._isOutputFile(key):
            filename, _ = QtGui.QFileDialog.getSaveFileName(self, caption='Choose file ...', dir=location,
                                                            filter="Iron, Zinc Files (*.exnode *.exelem);;All (*.* *)")
        else:
            filename, _ = QtGui.QFileDialog.getOpenFileName(self, caption='Choose file ...', dir=location,
                                                            filter="Iron, Zinc Files (*.exnode *.exelem *.ipelem *.ipnode *.ipfiel);;All (*.* *)")
        if filename:
            self._location = os.path.dirname(filename)
            self._problem.updateFileInputOutputs({key: filename})
            line_edit.setText(filename)

    def _updateMainParameterValue(self):
        sender = self.sender()

        key = self._map_ui_to_keys[sender]
        self._problem.updateMainParameters({key: sender.value()})

    def _updateFlowParameterValue(self):
        sender = self.sender()
        key = self._map_ui_to_keys[sender]
        if self._isEnumParameter(key):
            self._problem.updateFlowParameters({key: self._map_expiration_index_to_string[sender.currentIndex()]})
        else:
            self._problem.updateFlowParameters({key: sender.value()})

    def serialise(self):
        d = {}
        d['location'] = self._location
        d['active_tab'] = self._ui.tabWidget.currentIndex()
        d['problem'] = self._problem.serialise()

        return json.dumps(d)

    def deserialise(self, string):
        d = json.loads(string)
        self._location = d['location'] if 'location' in d else None
        self._ui.tabWidget.setCurrentIndex(d['active_tab'] if 'active_tab' in d else 2)
        if 'problem' in d:
            self._problem.deserialise(d['problem'])

        self.updateUi()

    def updateUi(self):
        self._updateExecutableParameters()
        self._updateFileInputOutputs()
        self._updateMainParameters()
        self._updateFlowParameters()
