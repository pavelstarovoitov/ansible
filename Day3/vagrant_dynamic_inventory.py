#!/usr/bin/python3
import argparse
import json
import paramiko
import subprocess
import sys
import os
import pprint

def parse_args():
    parser = argparse.ArgumentParser(description="Vagrant inventory script")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true')
    group.add_argument('--host')
    return parser.parse_args()


def list_hosts():
    cmd = "vagrant status"
    #print(os.getcwd())
    status = (subprocess.check_output(cmd.split()).rstrip())
    #print(status)
    hosts = []
    for line in status.split(b'\n'):
        if b'running' in line:
            line = str(line.split(b',')).split("'")[1] 
            hosts.append(line)
    return hosts


def get_host_details(host):
    print(host)
    cmd = "vagrant ssh-config {}".format(host)
    print(cmd)
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    config = paramiko.SSHConfig()
    print(p.stdout)
    config.parse(p.stdout)
    c = config.lookup(host)
    print(c)
    return {'ansible_host': c['hostname'],
            'ansible_port': c['port'],
            'ansible_user': c['user'],
            'ansible_private_key_file': c['identityfile'][0]}


def main():
    args = parse_args()
    if args.list:
        hosts = list_hosts()
        #json.dump({'vagrant': hosts}, sys.stdout)
        pprint.pprint(hosts)
    else:
        details = get_host_details(args.host)
        json.dump(details, sys.stdout)

if __name__ == '__main__':
    pass
    main()

#print(list_hosts())
#print(get_host_details('db_server'))