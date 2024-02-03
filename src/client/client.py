from api.api import TopTrackPyAPI
from client import Activity
from client.objects.project import Project


class TopTrackPyClient:
    def __init__(self):
        self.api = TopTrackPyAPI()

    def get_projects(self, archived=True):
        raw_projects = self.api.get_projects(archived)
        return Project.multiple_from_dict(raw_projects)

    def get_activities(self, project_id, worker_id, start_date, end_date):
        raw_activities = self.api.get_activities(project_id, worker_id, start_date, end_date)
        return Activity.multiple_from_dict(raw_activities)

