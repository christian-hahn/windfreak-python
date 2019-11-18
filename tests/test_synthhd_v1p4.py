"""Tests for SynthHD object.

This module contains unit-tests for the SynthHD object specific to SynthHD v1.4.
"""

import sys
import unittest
from test_synthhd_base import SynthHDBaseTestCase
from windfreak import SynthHD


class SynthHDv1p4TestCase(unittest.TestCase, SynthHDBaseTestCase):

    def setUp(self):
        self._dut = SynthHD(self.DEVPATH)
        self._dut.init()

    def tearDown(self):
        self._dut.init()
        self._dut.close()
        del self._dut

    def test_model(self):
        model = self._dut.model
        self.assertIsInstance(model, str)
        self.assertEqual(model, 'SynthHD v1.4')

    def test_frequency_range(self):
        expected = {'start': 53.e6, 'stop': 13999.999999e6, 'step': 0.1}
        for channel in self._dut:
            f_range = channel.frequency_range
            self.assertIsInstance(f_range, dict)
            self.assertEqual(f_range, expected)

    def test_power_range(self):
        expected = {'start': -80., 'stop': 20., 'step': 0.01}
        for channel in self._dut:
            p_range = channel.power_range
            self.assertIsInstance(p_range, dict)
            self.assertEqual(p_range, expected)

    def test_vga_dac_range(self):
        expected = {'start': 0, 'stop': 45000, 'step': 1}
        for channel in self._dut:
            vga_range = channel.vga_dac_range
            self.assertIsInstance(vga_range, dict)
            self.assertEqual(vga_range, expected)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        SynthHDv1p4TestCase.DEVPATH = sys.argv.pop()
    unittest.main()
