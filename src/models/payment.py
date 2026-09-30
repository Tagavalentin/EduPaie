from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Payment:
    """Modèle représentant un paiement."""
    id: Optional[int]
    student_id: int
    montant: int
    date_paiement: str
    mode_paiement: str
    numero_recu: str
    solde_apres: int
    created_at: Optional[datetime] = None
