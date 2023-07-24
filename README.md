# tf-aws-ingress-rules-checker
A script to determine if ingress rules are missing in code changes, based on a terraform plan json file

## Overview

Imagine that you are needing to do a refactor of your security groups code. Maybe because you have tons of ingress rules that can be grouped in one, or maybe you want to do a cleanup of them. These refactors are a critical task, because deleting an used rule can become in a outage of your applications. 
The idea of this script is to create reliability in the code refactor, showing the rules that are missing. This is achieved analizing a terraform plan file with the changes.

## The terraform plan file

This script works with terraform version >= 0.13.X.
To get the file needed follow this steps.

1. Run terraform plan and save it in a file: `terraform plan -out=out.plan`.
2. Convert the file to json format: `terraform show -json out.plan > out.json`.

## Using the script

Now you can use the script, passing it your terraform file:

```sh
python3 ingress_rules_checker.py out.json security_group
```

The script supports the check of `security_group` `network_acl` resources.