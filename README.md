# Citrix Extension VDA Load Generator

This projects simulates a running VDA.

It generates the needed WMI namespace, classes and instances.
It also generates the needed registry entries.

It **MUST** be run as administrator

## Usage

```powershell
# on an elevated powershell/cmd prompt
pip install -r requirements.txt
python load.py <optional_number_of_sessions>
```
