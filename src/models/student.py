from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Student:
    """Modèle représentant un élève."""
    id: Optional[int]
    nom: str
    prenom: str
    classe: str
    annee_scolaire: str
    total_du: int
    created_at: Optional[datetime] = None
