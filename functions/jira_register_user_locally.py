import json
from os import path
from .exceptions import WrongUsage


def registerJiraUser(username, args):
    """create a new register in the json file with the username as key and jira user id as value"""
    storage_path = "functions/storage/jira_id_storage.json"
    if len(args) != 1:
        raise WrongUsage("Usage: /jiraRegister <user_id>")

    jira_id = args[0]

    prev_registers = {}
    if path.exists(storage_path):
        with open(storage_path, "r") as file:
            prev_registers = json.load(file)

    prev_registers[username] = jira_id

    with open(storage_path, 'w') as outfile:
        json.dump(prev_registers, outfile)
