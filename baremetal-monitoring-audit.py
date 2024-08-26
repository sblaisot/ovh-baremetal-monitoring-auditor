#!/usr/bin/env python3

import ovh
import re
import sys
from config import Config

# regexp list of server names to ignore
SERVER_IGNORE = [
    "^valid\d+$",
    "^backupit-01$",
    ".*-old$",
]
config = Config()
ovh_config = config.get("ovh")

client = ovh.Client(**ovh_config)
servers = client.get("/dedicated/server")

warnings = []
ignore_reg_list = list(map(re.compile, SERVER_IGNORE))
for server in servers:
    server_details = client.get(f"/dedicated/server/{server}")
    reverse = server_details.get("reverse")
    if reverse is None:
        reverse = server_details.get("name")
    name = reverse.split(".")[0]
    if any(regex.match(name) for regex in ignore_reg_list):
        continue
    monitoring = server_details.get("monitoring", False)
    nointer = server_details.get("noIntervention", False)
    if not monitoring or nointer:
        warnings.append(name)

if warnings:
    print("Servers with monitoring or intervention disabled:")
    for name in sorted(warnings):
        print(f"  - {name}")
    sys.exit(1)
