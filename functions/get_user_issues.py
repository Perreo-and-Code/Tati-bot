from jira import JIRA
import os
import json
from .exceptions import *


def getUserIssues(args, username):
    """get issues by user

    Args:
        args (list): list that contains the project id
        username (string): telegram username of the user

    Returns:
        issue: issue object with all the info from the issues by an specific user
    """

    # it must only receive the project id as argument
    if len(args) != 1:
        raise WrongUsage("Usage: /getMyIssues <project_id>")

    JIRA_TOKEN = os.environ.get("JIRA_TOKEN", None)
    if JIRA_TOKEN is None:
        raise MissingToken("Insert a JIRA_TOKEN")

    # if the is an invalid token it will fail so the try cath handle raising an exception
    try:
        jira = JIRA(basic_auth=("stevenbrand@treenapp.com", JIRA_TOKEN),
                    options={"server": "https://treen.atlassian.net"})
    except Exception:
        raise InvalidToken("Invalid JIRA_TOKEN")

    storage_path = "functions/storage/jira_id_storage.json"
    # read the data storage to get the jira id from this
    with open(storage_path, "r") as file:
        registers = json.load(file)

    if username not in registers:
        raise MissingRegister("you must run first: /jiraRegister <user_id>")

    project = args[0]
    assignee = registers[username]
    query = f"project = {project} AND issuetype = Story AND assignee in ({assignee}) order by created DESC"
    # execute the query to get the data from jira
    issues_in_project = jira.search_issues(query)
    return issues_in_project


def formatIssuesByUser(issues):
    """give html format to the issue data

    Args:
        issues (issue object): contain all the info from the issues of a user

    Returns:
        string: html formatter data from issue
    """    
    issues_status = {}
    html_format = ""
    for issue in issues:
        issue_data = {}
        status = str(issue.fields.status)
        summary = issue.fields.summary
        key = issue.key
        issue_data["key"] = key
        issue_data["summary"] = summary

        if status in issues_status.keys():
            issues_status[status].append(issue_data)
        else:
            issues_status[status] = [issue_data]
            
    for status in issues_status.keys():
        html_format += str(status) + ":\n"
        for issue in issues_status[status]:
            template = "\t\t<b>{}</b> - {}\n".format(issue["key"], issue["summary"])
            html_format += template

    return html_format