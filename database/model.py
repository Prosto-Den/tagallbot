from dataclasses import dataclass


@dataclass(slots = True)
class Meme:
    id: str
    name: str
    tags: str = '#общий'
