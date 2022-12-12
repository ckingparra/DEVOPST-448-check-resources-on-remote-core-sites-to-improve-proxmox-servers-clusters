#!/usr/bin/env python3
import requests
import json
import re
import os
import fire # https://google.github.io/python-fire/guide/#introduction


def login(api_url, un, pw):
    response = requests.post(api_url,
        json={ "jsonrpc": "2.0",
               "method": "user.login",
               "params": { "user": un, "password": pw},
               "id": 1})
    return response.json().get("result")


def get_hosts(api_url, token):
    response = requests.post(api_url,
        json={ "jsonrpc": "2.0",
               "method": "host.get",
               "params": {},
               "auth": token,
               "id": 1
             })
    return response.json().get("result")


def filter_by_hostname(pattern, hosts):
    """Filter a list of host objects based on the whether their hostname matches the regex :pattern:"""
    return [ e for e in hosts
             if re.match(re.compile(pattern), e.get("host"))]


def deconstruct_hostids(hosts):
    return [e.get("hostid") for e in hosts]


def get_hostgroups(api_url, hostids):
    response = requests.post(api_url,
        json={ "jsonrpc": "2.0",
               "method": "hostgroup.get",
               "params": {"hostids": json.dumps(hostids)},
               "output": "extend",
               "id": 1})
    return response.json().get("result")


def add_to_core_site_proxmox(api_url, token, hostids):
    response = requests.post(api_url,
        json={ "jsonrpc": "2.0",
               "method": "hostgroup.massadd",
               "params": {
                   "groups": ["core_site_proxmox"],
                   "hostids": hostids
                   },
               "output": "extend",
               "auth": token,
               "id": 1})
    return response.json().get("result")


def less(method, params, output="extend"):
    response = requests.post(api_url,
        json={ "jsonrpc": "2.0",
               "method": method,
               "params": params,
               "output": output,
               "auth": token,
               "id": 1})
    return response.json().get("result")


def get_host_by_hostid(hostid):
    return less("host.get", {"filter": {"hostid": "10865"}})

# less("hostgroup.get", {"filter": { "name": ["core_site_proxmox"]}})
# [{'groupid': '133', 'name': 'core_site_proxmox', 'internal': '0', 'flags': '0'}]


# Add list of host ids to the hostgroup.
# >>> less("hostgroup.massadd", {"groups": ["133"], "hosts": hostids})

api_url    = "https://zabbix.hivelocity.net/api_jsonrpc.php"
token      = os.environ.get('ZABBIX_API_TOKEN', default="")
core_sites = ["atl2", "ord1", "dal1", "lax1", "lax2", "fll1", "sea1", "tpa1", "tpa2", "fra1"]
pattern    = r'proxmox.*\..*(atl2|ord1|lax1|lax2|fll1|sea1|tpa1|tpa2|fra1).*'
# hosts = get_hosts(api_url, token)


if __name__ == '__main__':
    fire.Fire()
