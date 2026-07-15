from dataclasses import dataclass
from typing import Dict

@dataclass
class Chunk:
    id: str
    document_id: str
    text: str
    metadata: Dict
