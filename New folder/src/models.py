from dataclasses import dataclass
from typing import Optional


@dataclass
class Activity:

    application: str
    title: str

    path: Optional[str]

    root: Optional[str]

    project: Optional[str]

    is_folder: bool