import dataclasses

from client.objects.base import BaseObject


@dataclasses.dataclass
class Worker(BaseObject):
    name: str
