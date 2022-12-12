#!/usr/bin/env python3
import requests
import json
import re
import os
# https://google.github.io/python-fire/guide/#introduction
import fire 

"""
Using the webui: There is no way to select multiple hosts by
regex, or add multiple hosts to a hostgroup. This script allows
you to do that. You either use this as a python library, or
run the functions as subcommands.
"""

core_site_proxmox_pattern = r'proxmox.*\..*(atl2|ord1|lax1|lax2|fll1|sea1|tpa1|tpa2|fra1).*'


def less(method, params, output="extend"):
    response = requests.post(
        "https://zabbix.hivelocity.net/api_jsonrpc.php",
        json={ "jsonrpc": "2.0",
               "method": method,
               "params": params,
               "output": output,
               "auth": os.environ.get('ZABBIX_API_TOKEN', default=""),
               "id": 1})
    return response.json().get("result")


def login(api_url, un, pw):
    return less("user.login", { "user": un, "password": pw})


def get_hosts(api_url, token):
    # less("hostgroup.get", {"filter": { "name": ["core_site_proxmox"]}})
    # [{'groupid': '133', 'name': 'core_site_proxmox', 'internal': '0', 'flags': '0'}]
    return less("host.get", {})


def filter_hostname_by_regex(pattern, hosts):
    """Filter a list of host objects based on the whether their
       hostname matches the regex :pattern:"""
    return [e for e in hosts if re.match(re.compile(pattern), e.get("host"))]


def deconstruct_hostids(hosts):
    return [e.get("hostid") for e in hosts]


def get_hostgroups(api_url, hostids):
    return less("hostgroup.get", {"hostids": hostids})


def add_to_core_site_proxmox(api_url, token, hostids):
    return less("method": "hostgroup.massadd",
                {"groups": ["core_site_proxmox"], "hostids": hostids })


def get_host_by_hostid(hostid):
    return less("host.get", {"filter": {"hostid": "10865"}})


def add_hostids_to_hostgroup(groupids, hostids):
    """ Add list of hostids to the list of hostgroups."""
    return less("hostgroup.massadd", {"groups": ["133"], "hosts": hostids})


if __name__ == '__main__':
    fire.Fire()
