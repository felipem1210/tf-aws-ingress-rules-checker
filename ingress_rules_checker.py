import json
import argparse

parser = argparse.ArgumentParser(description='Script to detect changes in ingress rules of security groups or network ACLs.')
parser.add_argument('json_file', type=str, help='JSON file to parse')
parser.add_argument('resource', type=str, help='The type of resource to check the ingress rules. Only accepts "security_group" or "network_acl"')
args = parser.parse_args()

json_file = args.json_file
resource_type = args.resource

def parse_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"The file '{file_path}' wasn't found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON file '{file_path}'. Verify file format.")

def remove_description(map):
    return {key: value for key, value in map.items() if key != "description"}

def process_data(resource):
    print(f"Resource: {resource['address']}")
    ingress_before = resource['change']['before']['ingress']
    ingress_after = resource['change']['after']['ingress']
    if resource_type == 'network_acl':
        result_before_list = return_nacls_lists(ingress_before)
        result_after_list = return_nacls_lists(ingress_after)
    elif resource_type == 'security_group':
        result_before_list = return_secgp_lists(ingress_before)
        result_after_list = return_secgp_lists(ingress_after)

    return result_before_list, result_after_list
        

def return_nacls_lists(ingress_data):   
    result_list = []         
    for ingress in ingress_data:
        result = {
            'cidr': ingress['cidr_block'],
            'from_port': ingress['from_port'],
            'to_port': ingress['to_port'],
            'rule_no': ingress['rule_no'],
            'action': ingress['action'],
        }
        result_list.append(result)
    return result_list

def return_secgp_lists(ingress_data):   
    result_list = []         
    for ingress in ingress_data:
        for cidr_block in ingress['cidr_blocks']:
            result = {
                'cidr': cidr_block,
                'from_port': ingress['from_port'],
                'to_port': ingress['to_port'],
                'description': ingress['description'],
            }
            result_list.append(result)
    return result_list

def return_missing_rules(result_before_list, result_after_list):
    missing_rules = []
    for item_before in result_before_list:
        if remove_description(item_before) not in map(remove_description, result_after_list):
            missing_rules.append(item_before)
    return missing_rules

def print_missing_rules(missing_rules):
    pretty_print = json.dumps(missing_rules, indent=2)
    print(f"Missing rules: {pretty_print}")


if __name__ == "__main__":
    data = parse_json_file(json_file)
    resource_changes = data['resource_changes']
    for resource in resource_changes:
        if resource_type in resource['address']:
            if len(resource['change']['before']['ingress']) != len(resource['change']['after']['ingress']):
                result_before_list, result_after_list = process_data(resource)
                missing_rules = return_missing_rules(result_before_list, result_after_list)
                print_missing_rules(missing_rules)
                

