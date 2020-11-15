import os
import json
import requests
from   jira     import JIRA
from   datetime import date


API_TOKEN_BOT = os.getenv('API_TOKEN_BOT')


OPTIONS = {
    'server': "https://treen.atlassian.net",
    'headers': {
        'Authorization': f'Basic {API_TOKEN_BOT}',
        'Content-Type': 'application/json',
    },
}

auth_jira = JIRA(options=OPTIONS)

def getInfoStatus(array, id, total, name):
    """
    Return dictionary about status e.g(To_DO: [total, average])
    params:
        array = contain the names status
        id    = id sprint
        total = total issue
        name  = name of project
    """
    status  = {}

    for value in array:
        key = "_".join(value.split())

        status_val = len(auth_jira.search_issues(f"project = {name} AND issuetype = Story AND status = '{value}' AND Sprint = {id} order by created DESC"))

        status[key] = [status_val, round((status_val / int(total)) * 100, 1)]

    return status

def dataSprint(text):
    """
    Get basic data about sprint
    params:
        text = name of project
    """
    try:
        name_project = text.split(' ')[1]
        board        = auth_jira.sprints(1)
        sprint_info  = auth_jira.sprint(board.total).raw

        # Days left to finish the sprint
        now_day      = date.fromisoformat(date.today().strftime('%Y-%m-%d'))
        end_day      = date.fromisoformat(sprint_info['isoEndDate'].split('T')[0])
        day_left     = abs(end_day-now_day).days

        data = auth_jira.search_issues(f'project={name_project} AND SPRINT not in closedSprints()')
        if not data:
            return "error: no sprint activated"
        
        status_names = ["In Progress","Blocked", "Done", "Review", "To Do"]

        values_status = getInfoStatus(status_names, board.total, data.total, name_project)
        
        message = f"""
        &#128204 Sprint: <b>{sprint_info['name']}</b>
        Days left:  {day_left}
        Total task: {data.total}

        &#128640; Done: [<b>{values_status['Done'][0]}</b>] = {values_status['Done'][1]}%
        &#129328; In Progress: [<b>{values_status['In_Progress'][0]}</b>] = {values_status['In_Progress'][1]}%
        &#x270D;  Review: [<b>{values_status['Review'][0]}</b>] = {values_status['Review'][1]}%
        &#x1F595; To Do: [<b>{values_status['To_Do'][0]}</b>] = {values_status['In_Progress'][1]}%
        &#128683; Blocked: [<b>{values_status['Blocked'][0]}</b>] = {values_status['Blocked'][1]}%
        """

        return message
    except Exception:
        return "Usage: /sprintDaily@TatiSoftBot [KEY-PROJECT]"
