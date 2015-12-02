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
from PySide import QtGui


class GlyphChooserWidget(QtGui.QComboBox):

    def __init__(self, parent=None):
        '''
        Call the super class init functions
        '''
        QtGui.QComboBox.__init__(self, parent)
        self._nullObjectName = None
        self._glyphmodule = None
        self._glyph = None

    def _buildGlyphList(self):
        '''
        Rebuilds the list of items in the ComboBox from the glyph module
        '''
        self.blockSignals(True)
        self.clear()
        if self._glyphmodule:
            if self._nullObjectName:
                self.addItem(self._nullObjectName)
            glyphiter = self._glyphmodule.createGlyphiterator()
            glyph = glyphiter.next()
            while glyph.isValid():
                name = glyph.getName()
                self.addItem(name)
                glyph = glyphiter.next()
        self.blockSignals(False)
        self._displayGlyph()

    def _displayGlyph(self):
        '''
        Display the currently chosen glyph in the ComboBox
        '''
        self.blockSignals(True)
        if self._glyph:
            glyphName = self._glyph.getName()
            # following doesn't handle glyph name matching _nullObjectName
            index = self.findText(glyphName)
        else:
            index = 0
        self.setCurrentIndex(index)
        self.blockSignals(False)

    def setNullObjectName(self, nullObjectName):
        '''
        Enable a null object option with the supplied name e.g. '-' or '<select>'
        Default is None
        '''
        self._nullObjectName = nullObjectName

    def setGlyphmodule(self, glyphmodule):
        '''
        Sets the region that this widget chooses glyphs from
        '''
        self._glyphmodule = glyphmodule
        self._buildGlyphList()

    def getGlyph(self):
        '''
        Must call this from currentIndexChanged() slot to get/update current glyph
        '''
        glyphName = str(self.currentText())
        if self._nullObjectName and (glyphName == self._nullObjectName):
            self._glyph = None
        else:
            self._glyph = self._glyphmodule.findGlyphByName(glyphName)
        return self._glyph

    def setGlyph(self, glyph):
        '''
        Set the currently selected glyph
        '''
        if not glyph or not glyph.isValid():
            self._glyph = None
        else:
            self._glyph = glyph
        self._displayGlyph()
