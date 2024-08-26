# OVH Baremetal Monitoring Auditor

Audit OVH baremetal monitoring to ensure it is enabled on al baremetal servers

## Requirements

This script requires python 3.10+

## Install

```bash
python3 -m venv venv
./venv/bin/pip install wheel
./venv/bin/pip install -r requirements.txt
```

## Configuration

Copy `config-template.yml`to `config.yml` and update to add your credentials

## Execution

```bash
./venv/bin/python baremetal-monitoring-audit.py
```
