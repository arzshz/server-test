import requests
from timesetting import normal2clockify, clockify2normal, utc2Teh, daily_interval, duration_to_time
import json
import datetime
import os
from dotenv import load_dotenv
import text_html
import semail

load_dotenv()

api_key = os.getenv('X_Api_Key')
workspace_id = os.getenv('workspace_id')

start_time, end_time = normal2clockify(daily_interval()[0]), normal2clockify(daily_interval()[1])
params = {'start': start_time, 'end': end_time}
headers = {'x-api-key': api_key}

# times in normal in Tehran tz.
startteh = clockify2normal(start_time)
endingteh = clockify2normal(end_time)

projects = {}
projects_name = {}
prjct_response = json.loads(
    requests.get(f'https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects', headers=headers).text)
for project in prjct_response:
    projects[project['id']] = datetime.timedelta()
    projects_name[project['id']] = project['name']

url = f'https://api.clockify.me/api/v1/workspaces/{workspace_id}/users'

response = requests.get(url, headers=headers)
users_response_json = json.loads(response.text)
users = [{'username': member['name'], 'id': member['id'], 'email': member['email']} for member in users_response_json]

absent_users = []
daily_report = []

for user in users:
    user_url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/user/{user['id']}/time-entries"
    records_response_json = json.loads(requests.get(user_url, headers=headers, params=params).text)

    if not records_response_json:
        absent_users.append(user)

    else:
        start_time = utc2Teh(clockify2normal(records_response_json[-1]['timeInterval']['start']))
        end_time = utc2Teh(clockify2normal(records_response_json[0]['timeInterval']['end']))
        total_time = datetime.timedelta(hours=0, minutes=0, seconds=0)

        for record in records_response_json:
            duration = duration_to_time(record['timeInterval']['duration'])
            delta = datetime.timedelta(hours=duration.hour, minutes=duration.minute, seconds=duration.second)
            total_time += delta

            if record['projectId']:
                projects[record['projectId']] += delta

        total_records = len(records_response_json)

        daily_report.append({
            'name': user['username'],
            'email': user['email'],
            'start_time': start_time.time(),
            'end_time': end_time.time(),
            'Total_time': str(total_time),
            'Total_records': total_records
        })

day_proj_report = [{'project_id': key, 'project_time': str(value), 'project_name': projects_name[key]} for key, value in
                   projects.items()]

# Path to save the JSON file
file_path = "./Flask_app/daily_projrcts_report.json"

# Writing the list of dictionaries to a JSON file
# with open(file_path, 'w') as json_file:
#     json.dump(day_proj_report, json_file, indent=4)  # Indent is optional, for readability


# file_path = "./Flask_app/daily_report.json"

# # Writing the list of dictionaries to a JSON file
# with open(file_path, 'w') as json_file:
#     json.dump(daily_report, json_file, indent=4)  # Indent is optional, for readability

proreport = day_proj_report

with open("daily_report.txt", "w") as wfile:
    wfile.write(
        f'Daily Activity Report:\n\n{startteh.date()} - {endingteh.date()}\n\n--------------------------------------\n\n')

    for report in daily_report:
        wfile.write(f"\nName: {report['name']}\n")
        wfile.write(f"Email: {report['email']}\n")
        wfile.write(f"Start Time: {report['start_time']}\n")
        wfile.write(f"End Time: {report['end_time']}\n")
        wfile.write(f"Total Tracked Time: {report['Total_time']}\n")
        wfile.write(f"Total Records: {report['Total_records']}\n")
        wfile.write('------------------------------------------\n')

    wfile.write(f'\n\n\nProjects:\n\n\n---------------------------------\n\n')

    for project in proreport:
        if project['project_time'] != '0:00:00':
            wfile.write(f"Project Name :   {project['project_name']}\n")
            # wfile.write(f"Project ID :   {project['project_id']}\n")
            wfile.write(f"Project Tracked Time :   {project['project_time']}\n")
            wfile.write('-----------------------------------------\n\n')

wfile.close()

daily_activities, projects = text_html.parse_daily_activity_report('daily_report.txt')
text_html.generate_html_report(daily_activities, projects, 'formatted_report.html')

semail.send_email('formatted_report.html', os.getenv('SENDER_EMAIL'), os.getenv('SENDER_APP_PASSWORD'), os.getenv('RECIEVER_EMAIL'), "Daily Activity Report")
