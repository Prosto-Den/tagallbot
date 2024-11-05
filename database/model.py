from dataclasses import dataclass


@dataclass
class Meme:
    id: str
    name: str
    tags: str = '#общий'
