class DailyActivity:
    def __init__(self, name, email, start_time, end_time, tracked_time, total_records):
        self.name = name
        self.email = email
        self.start_time = start_time
        self.end_time = end_time
        self.tracked_time = tracked_time
        self.total_records = total_records

class Project:
    def __init__(self, name, tracked_time):
        self.name = name
        self.tracked_time = tracked_time

def parse_daily_activity_report(file_path):
    daily_activities = []
    projects = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            if lines[i].startswith('Name:'):
                name = lines[i].split(': ')[1].strip()
                email = lines[i+1].split(': ')[1].strip()
                start_time = lines[i+2].split(': ')[1].strip()
                end_time = lines[i+3].split(': ')[1].strip()
                tracked_time = lines[i+4].split(': ')[1].strip()
                total_records = int(lines[i+5].split(': ')[1].strip())
                daily_activity = DailyActivity(name, email, start_time, end_time, tracked_time, total_records)
                daily_activities.append(daily_activity)
                i += 7
            elif lines[i].startswith('Project Name :'):
                name = lines[i].split(': ')[1].strip()
                tracked_time = lines[i+1].split(': ')[1].strip()
                project = Project(name, tracked_time)
                projects.append(project)
                i += 3
            else:
                i += 1
    return daily_activities, projects

def write_daily_activity_report(daily_activities, projects, output_file):
    with open(output_file, 'w') as file:
        file.write("Daily Activity Report:\n\n")

        for activity in daily_activities:
            file.write(f"Name: {activity.name}\n")
            file.write(f"Email: {activity.email}\n")
            file.write(f"Start Time: {activity.start_time}\n")
            file.write(f"End Time: {activity.end_time}\n")
            file.write(f"Total Tracked Time: {activity.tracked_time}\n")
            file.write(f"Total Records: {activity.total_records}\n\n")

        file.write("Projects:\n\n")

        for project in projects:
            file.write(f"Project Name: {project.name}\n")
            file.write(f"Project Tracked Time: {project.tracked_time}\n\n")


def generate_html_report(daily_activities, projects, output_file):
    with open(output_file, 'w') as file:
        file.write("<!DOCTYPE html>\n")
        file.write("<html>\n<head>\n")
        file.write("<title>Daily Activity Report</title>\n")
        file.write("<style>\n")
        file.write("body {font-family: Arial, sans-serif;}\n")
        file.write("h1 {text-align: center;}\n")
        file.write("table {width: 100%; border-collapse: collapse;}\n")
        file.write("th, td {border: 1px solid #dddddd; text-align: left; padding: 8px;}\n")
        file.write("th {background-color: #f2f2f2;}\n")
        file.write("</style>\n")
        file.write("</head>\n<body>\n")
        file.write("<h1>Daily Activity Report</h1>\n\n")
        file.write("<h2>Daily Activities</h2>\n")
        file.write("<table>\n<tr><th>Name</th><th>Email</th><th>Start Time</th><th>End Time</th><th>Total Tracked Time</th><th>Total Records</th></tr>\n")

        for activity in daily_activities:
            file.write(f"<tr><td>{activity.name}</td><td>{activity.email}</td><td>{activity.start_time}</td><td>{activity.end_time}</td><td>{activity.tracked_time}</td><td>{activity.total_records}</td></tr>\n")

        file.write("</table>\n\n")
        file.write("<h2>Projects</h2>\n")
        file.write("<table>\n<tr><th>Project Name</th><th>Project Tracked Time</th></tr>\n")

        for project in projects:
            file.write(f"<tr><td>{project.name}</td><td>{project.tracked_time}</td></tr>\n")

        file.write("</table>\n")
        file.write("</body>\n</html>")


# daily_activities, projects = parse_daily_activity_report('month.txt')
# generate_html_report(daily_activities, projects, 'formatted_report.html')
