import dataclasses

from client.objects.base import BaseObject


@dataclasses.dataclass
class Project(BaseObject):
    name: str
    currency: str
