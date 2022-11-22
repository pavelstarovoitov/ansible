#!/usr/bin/python3
import json
import vagrant
from jinja2 import Template
import os
import argparse

def main(): 

    parser = argparse.ArgumentParser(description='Ansible Inventory System')
    parser.add_argument('--list', help='List all inventory groups', action="store_true")
    parser.add_argument('--host', help='List vars for a host')
    parser.add_argument('--file', help='File to open, default inventory.yml', 
            default='inventory.yml')
    args = parser.parse_args()

    inventory = (args.file)
    v = vagrant.Vagrant(os.getcwd())
    current = v.conf()

    #print(current)
    os_env = os.environ.copy()
    os_env['USE_NFS'] = '1'

    status = v.status()  # will pass env to the vagrant subprocess
    #print(v.status())
    res = v.ssh('db_server', 'hostname -I')
    db_ip = res.strip().split(' ')[1]
    res = v.ssh('app_server', 'hostname -I')
    app_ip = res.strip().split(' ')[1]
    ip = {'app_server':app_ip, 'db_server':db_ip}
    #return {'ansible_host': l}
    with open('inventory') as template_file:
        template = template_file.read()
    t = Template(template)
    inventory_conf = t.render(ip)
    #print(inventory_conf)

    with open('inventory.yml', 'w') as inventory_file:
        inventory_file.write(inventory_conf)
    
    with open('inventory.yml') as inventory_file:
        pass

    return {
            'group': {
                'hosts': [db_ip, app_ip],
                'vars': {
                    'ansible_user': 'vagrant',
                    'ansible_ssh_private_key_file':
                        "/home/starik/.vagrant.d/insecure_private_key",
                    'ansible_python_interpreter':
                        '/usr/bin/python3',
                    'example_variable': 'value'
                }
            },
            '_meta': {
                'hostvars': {
                    '192.168.60.4': {
                        'host_specific_var': 'foo'
                    },
                    '192.168.60.5': {
                        'host_specific_var': 'bar'
                    }
                }
            }
        }



if __name__ == '__main__':
   print(json.dumps(main()))
