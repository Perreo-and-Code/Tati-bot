import os
import json
import requests
from datetime import date

URL_SPRINT = "https://treen.atlassian.net/rest/agile/1.0/"

API_TOKEN_BOT = os.getenv('API_TOKEN_BOT')

HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Basic {API_TOKEN_BOT}"
}

class Board():
    """ class that represent the name board """
    total = 0
    total_percent = 0

    def __init__(self, total_task):
        """ constructor """
        self.total_task = int(total_task)

    def func_data_total(self):
        """ setting the attributes class """
        self.total += 1
        self.total_percent = round((self.total / self.total_task) * 100, 1)


def responseDataApi(content):
    """ Return data json of api JIRA """
    response = requests.request(
        "GET",
        URL_SPRINT + content,
        headers=HEADERS
    )

    return response.json()

def dataSprint():
    """ Get basic data about sprint """
    data = responseDataApi("sprint/1/issue")

    total_task   = data.get('total')
    name_sprint  = data.get('issues')[0].get('fields').get('sprint').get('name')
    end_day_data = data.get('issues')[0].get('fields').get('sprint').get('endDate')

    now_day  = date.fromisoformat(date.today().strftime('%Y-%m-%d'))
    end_day  = date.fromisoformat(end_day_data.split('T')[0])
    day_left = abs(end_day-now_day).days

    progress    = Board(total_task)
    done        = Board(total_task)
    to_do       = Board(total_task)
    review      = Board(total_task)
    blocked     = Board(total_task)
    

    for value in data.get('issues'):
        name_column = value.get('fields').get('status').get('name')
        
        if name_column == "Done":
            done.func_data_total()
        elif name_column == "In Progress":
            progress.func_data_total()
        elif name_column == "To Do":
            to_do.func_data_total()
        elif name_column == "Review":
            review.func_data_total()
        elif name_column == "Blocked":
            blocked.func_data_total()

    message = f"""
    &#128204 Sprint: <b>{name_sprint}</b>
    Days left: {day_left}
    Total task: {total_task}

    &#128640; Done: [<b>{done.total}</b>] = {done.total_percent}%
    &#129328; In Progress: [<b>{progress.total}</b>] = {progress.total_percent}%
    &#x270D; Review: [<b>{review.total}</b>] = {review.total_percent}%
    &#x1F595; To Do: [<b>{to_do.total}</b>] = {to_do.total_percent}%
    &#128683; Blocked: [<b>{blocked.total}</b>] = {blocked.total_percent}%
    """

    return message
