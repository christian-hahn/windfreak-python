"""Base tests for SynthHD object.

This module contains common unit-tests for the SynthHD object.
"""

from math import floor
from time import sleep


class SynthHDBaseTestCase:

    DEVPATH = '/dev/ttyACM0'
    NOMINAL_FREQUENCY = 1.e9
    NOMINAL_POWER = -10.

    ## Device

    def test_model_type(self):
        model = self._dut.model_type
        self.assertIsInstance(model, str)
        self.assertIn('WFT SynthHD', model)

    def test_serial_number(self):
        serial = self._dut.serial_number
        self.assertIsInstance(serial, int)
        self.assertGreaterEqual(serial, 0)

    def test_version(self):
        version = self._dut.firmware_version
        self.assertIsInstance(version, str)
        self.assertIn('Firmware Version', version)
        version = self._dut.hardware_version
        self.assertIsInstance(version, str)
        self.assertIn('Hardware Version', version)

    def test_save(self):
        self._dut.save()

    def test_reference_mode(self):
        modes = self._dut.reference_modes
        self.assertIsInstance(modes, tuple)
        for mode in modes:
            self.assertIsInstance(mode, str)
            self._dut.reference_mode = mode
            read = self._dut.reference_mode
            self.assertIsInstance(read, str)
            self.assertEqual(read, mode)

    def test_trigger_mode(self):
        modes = self._dut.trigger_modes
        self.assertIsInstance(modes, tuple)
        for mode in modes:
            self.assertIsInstance(mode, str)
            self._dut.trigger_mode = mode
            read = self._dut.trigger_mode
            self.assertIsInstance(read, str)
            self.assertEqual(read, mode)

    def test_temperature(self):
        value = self._dut.temperature
        self.assertIsInstance(value, float)

    def test_reference_frequency(self):
        self._dut.reference_mode = 'external'
        f_range = self._dut.reference_frequency_range
        self.assertIsInstance(f_range, dict)
        for key in ('start', 'stop', 'step'):
            self.assertIsInstance(f_range[key], float)
        self.assertLessEqual(f_range['start'], f_range['stop'])
        f_start = f_range['start']
        f_stop = f_range['stop']
        f_step = f_range['step']
        coarse_step = (f_stop - f_start) / 17
        freq = f_start
        while freq <= f_stop:
            self._dut.reference_frequency = freq
            read = self._dut.reference_frequency
            self.assertIsInstance(read, float)
            error = abs(freq - read)
            print('Set reference frequency to {} Hz (error = {})'
                  .format(freq, error))
            self.assertLess(error, 0.1)
            freq = floor((freq + coarse_step - f_start) / f_step) * f_step + f_start

    ## Channel

    def test_frequency(self):
        for index, channel in enumerate(self._dut):
            others = [ch for ch in self._dut if not ch is channel]
            f_range = channel.frequency_range
            self.assertIsInstance(f_range, dict)
            for key in ('start', 'stop', 'step'):
                self.assertIsInstance(f_range[key], float)
            self.assertLessEqual(f_range['start'], f_range['stop'])
            f_start = f_range['start']
            f_stop = f_range['stop']
            f_step = f_range['step']
            coarse_step = (f_stop - f_start) / 17
            freq = f_start
            while freq <= f_stop:
                before = [ch.frequency for ch in others]
                channel.frequency = freq
                read = channel.frequency
                after = [ch.frequency for ch in others]
                self.assertEqual(before, after)
                self.assertIsInstance(read, float)
                error = abs(freq - read)
                print('Set channel {} frequency to {} Hz (error = {})'
                      .format(index, freq, error))
                self.assertLess(error, 1.e-5)
                freq = floor((freq + coarse_step - f_start) / f_step) * f_step + f_start

    def test_power(self):
        for index, channel in enumerate(self._dut):
            others = [ch for ch in self._dut if not ch is channel]
            channel.frequency = self.NOMINAL_FREQUENCY
            p_range = channel.power_range
            self.assertIsInstance(p_range, dict)
            for key in ('start', 'stop', 'step'):
                self.assertIsInstance(p_range[key], float)
            self.assertLessEqual(p_range['start'], p_range['stop'])
            start = max(p_range['start'], -40.)
            stop = p_range['stop']
            step = p_range['step']
            coarse_step = (stop - start) / 17
            power = start
            while power <= stop:
                before = [ch.frequency for ch in others]
                channel.power = power
                read = channel.power
                after = [ch.frequency for ch in others]
                self.assertEqual(before, after)
                self.assertIsInstance(read, float)
                error = abs(power - read)
                print('Set channel {} power to {} dBm (error = {})'
                      .format(index, power, error))
                self.assertLess(error, 1.e-14)
                power = floor((power + coarse_step - start) / step) * step + start

    def test_calibrated(self):
        for channel in self._dut:
            channel.frequency = self.NOMINAL_FREQUENCY
            channel.power = self.NOMINAL_POWER
            channel.enable = True
            value = channel.calibrated
            self.assertIsInstance(value, bool)
            self.assertTrue(value)

    def test_temp_compensation_mode(self):
        for channel in self._dut:
            others = [ch for ch in self._dut if not ch is channel]
            modes = channel.temp_compensation_modes
            self.assertIsInstance(modes, tuple)
            for mode in modes:
                self.assertIsInstance(mode, str)
                before = [ch.temp_compensation_mode for ch in others]
                channel.temp_compensation_mode = mode
                read = channel.temp_compensation_mode
                after = [ch.temp_compensation_mode for ch in others]
                self.assertIsInstance(read, str)
                self.assertIn(read, modes)
                self.assertEqual(before, after)
                self.assertEqual(mode, read)

    def test_vga_dac(self):
        for channel in self._dut:
            channel.temp_compensation_mode = 'none'
        for index, channel in enumerate(self._dut):
            others = [ch for ch in self._dut if not ch is channel]
            dac_range = channel.vga_dac_range
            self.assertIsInstance(dac_range, dict)
            for key in ('start', 'stop', 'step'):
                self.assertIsInstance(dac_range[key], int)
            self.assertLessEqual(dac_range['start'], dac_range['stop'])
            start = dac_range['start']
            stop = dac_range['stop']
            step = dac_range['step']
            coarse_step = (stop - start) / 33
            value = start
            while value <= stop:
                before = [ch.vga_dac for ch in others]
                channel.vga_dac = value
                read = channel.vga_dac
                after = [ch.vga_dac for ch in others]
                self.assertEqual(before, after)
                self.assertIsInstance(read, int)
                print('Set channel {} VGA DAC to {} (read = {})'
                      .format(index, value, read))
                self.assertEqual(value, read)
                value = floor((value + coarse_step - start) / step) * step + start

    def test_phase(self):
        for index, channel in enumerate(self._dut):
            others = [ch for ch in self._dut if not ch is channel]
            p_range = channel.phase_range
            self.assertIsInstance(p_range, dict)
            for key in ('start', 'stop', 'step'):
                self.assertIsInstance(p_range[key], float)
            self.assertLessEqual(p_range['start'], p_range['stop'])
            start = p_range['start']
            stop = p_range['stop']
            step = p_range['step']
            coarse_step = (stop - start) / 33
            phase = start
            while phase <= stop:
                before = [ch.frequency for ch in others]
                channel.phase = phase
                read = channel.phase
                after = [ch.frequency for ch in others]
                self.assertEqual(before, after)
                self.assertIsInstance(read, float)
                error = abs(phase - read)
                print('Set channel {} phase to {} degrees (error = {})'
                      .format(index, phase, error))
                self.assertLess(error, .006)
                phase = floor((phase + coarse_step - start) / step) * step + start

    def channel_enable_helper(self, attr):
        for channel in self._dut:
            others = [ch for ch in self._dut if not ch is channel]
            for value in (False, True, False):
                before = [getattr(ch, attr) for ch in others]
                setattr(channel, attr, value)
                read = getattr(channel, attr)
                after = [getattr(ch, attr) for ch in others]
                self.assertIsInstance(read, bool)
                self.assertEqual(before, after)
                self.assertEqual(value, read)

    def test_rf_enable(self):
        self.channel_enable_helper('rf_enable')

    def test_pa_enable(self):
        self.channel_enable_helper('pa_enable')

    def test_pll_enable(self):
        self.channel_enable_helper('pll_enable')

    def test_enable(self):
        self.channel_enable_helper('enable')

    def test_lock_status(self):
        for channel in self._dut:
            channel.frequency = self.NOMINAL_FREQUENCY
            channel.power = self.NOMINAL_POWER
            channel.enable = True
            sleep(1.)
            value = channel.lock_status
            self.assertIsInstance(value, bool)
            self.assertTrue(value)

    def test_modulation_enables(self):
        enables = ('sweep_enable', 'am_enable', 'pulse_mod_enable',
                   'dual_pulse_mod_enable', 'fm_enable')
        for enable in enables:
            others = [en for en in enables if not en == enable]
            for value in (False, True, False):
                before = [getattr(self._dut, en) for en in others]
                setattr(self._dut, enable, value)
                read = getattr(self._dut, enable)
                after = [getattr(self._dut, en) for en in others]
                self.assertIsInstance(read, bool)
                self.assertEqual(before, after)
                self.assertEqual(value, read)
