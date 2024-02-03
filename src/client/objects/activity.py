import dataclasses

from dateutil.parser import parse

from client import Project, Worker
from client.objects.base import BaseObject


@dataclasses.dataclass
class Activity(BaseObject):
    description: str
    end_time: str
    start_time: str
    seconds: int
    project: Project
    worker: Worker
    amount: float
    last_shot: dict
    shots_count: int

    @classmethod
    def parse_start_time(cls, value):
        return parse(value)

    @classmethod
    def parse_end_time(cls, value):
        return parse(value)

    @classmethod
    def parse_project(cls, value):
        return Project.from_dict(value)

    @classmethod
    def parse_worker(cls, value):
        return Worker.from_dict(value)