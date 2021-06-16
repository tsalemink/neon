import unittest

from opencmiss.zincwidgets.tessellationeditorwidget import processMultiFormatData


test_ex_01 = '1'
test_ex_02 = '1, 1'
test_ex_03 = '1*1'
test_ex_04 = 'the'
test_ex_05 = '1t'
test_ex_06 = '[1, 1, 4]'
test_ex_07 = '2*3*4'
test_ex_08 = '[1. 3. 5t]'


class EditorsTestCase(unittest.TestCase):

    def testProcessMultiFormatData(self):
        out_01 = processMultiFormatData(test_ex_01)
        self.assertEqual(1, out_01)

        out_02 = processMultiFormatData(test_ex_02)
        self.assertEqual([1, 1], out_02)

        out_03 = processMultiFormatData(test_ex_03)
        self.assertEqual([1, 1], out_03)

        out_04 = processMultiFormatData(test_ex_04)
        self.assertEqual(None, out_04)

        out_05 = processMultiFormatData(test_ex_05)
        self.assertEqual(None, out_05)

        out_06 = processMultiFormatData(test_ex_06)
        self.assertEqual([1, 1, 4], out_06)

        out_07 = processMultiFormatData(test_ex_07)
        self.assertEqual([2, 3, 4], out_07)

        out_08 = processMultiFormatData(test_ex_08)
        self.assertEqual(None, out_08)
