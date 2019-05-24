#!/usr/bin/python
"""Ansible module to transfer files to Cisco IOS devices."""
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.ios.ios import get_connection
from ansible.module_utils.network.ios.ios import ios_argument_spec
import re

def run_commands(module, commands, check_rc=False):
    connection = get_connection(module)

    return connection.run_commands(commands=commands, check_rc=check_rc)

def main():
    argument_spec = dict(
        state=dict(default='present',
                   choices=['present', 'absent',
                            'enabled', 'disabled'])
    )

    argument_spec.update(ios_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)    
    warnings = list()
    result = {'changed': False, 'warnings': warnings}
    filefact = {}	
    output = run_commands(module, ['show flash1:'])
    output += run_commands(module, ['show flash2:'])
    output += run_commands(module, ['show flash3:'])
    output += run_commands(module, ['show flash4:'])
    output += run_commands(module, ['show flash5:'])
    output += run_commands(module, ['show flash6:'])
    output += run_commands(module, ['show flash7:'])
    output += run_commands(module, ['show flash8:'])
    output += run_commands(module, ['show flash9:'])
    output += run_commands(module, ['dir flash-1:'])
    output += run_commands(module, ['dir flash-2:'])
    output += run_commands(module, ['dir flash-3:'])
    output += run_commands(module, ['dir flash-4:'])
    output += run_commands(module, ['dir flash-5:'])
    output += run_commands(module, ['dir flash-6:'])
    output += run_commands(module, ['dir flash-7:'])
    output += run_commands(module, ['dir flash-8:'])
    output += run_commands(module, ['dir flash-9:'])
    facts = dict()
    filesys = list()
    for data in output:
    	 match = re.search(r'Directory of (\S+):/',data)
    	 if match:
    	   fs = match.group(1)
    	   facts[fs] = dict()
    	 match1 = re.search(r'(\d+) bytes total \((\d+) bytes free\)',data)
    	 if match1:
    	   facts[fs]['spacetotal_kb'] = int(match1.group(1))
    	   facts[fs]['spacefree_kb'] = int(match1.group(2))
    for data in output:
  		match = re.search(r'Directory of (\S+):/', data)
  		if match:
  			filesys.append(match.group(1))
	

    filefact['filesystem'] = filesys
    filefact['filesystem_info'] = facts	

    module.exit_json(ansible_facts=filefact)

if __name__ == "__main__":
    main()
