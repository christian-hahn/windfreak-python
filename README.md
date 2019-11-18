# windfreak-python [![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/christian-hahn/windfreak-python/blob/master/LICENSE)

## Abstract

windfreak is a pure Python package to facilitate use of Windfreak Technologies devices from Python.

windfreak is Python 3 compatible.

## Supported devices
* SynthHD v1.4
* SynthHD PRO v1.4
* SynthHD v2
* SynthHD PRO v2

## Installation

Using `pip`:
```text
pip install windfreak
```

Using `setup.py`:
```text
git clone https://github.com/christian-hahn/windfreak-python.git
cd windfreak-python
python setup.py install
```

## Example

### SynthHD

```python
from windfreak import SynthHD

synth = SynthHD('/dev/ttyACM0')
synth.init()

# Set channel 0 power and frequency
synth[0].power = -10.
synth[0].frequency = 2.e9

# Enable channel 0
synth[0].enable = True
```

## License
windfreak-python is covered under the MIT licensed.
