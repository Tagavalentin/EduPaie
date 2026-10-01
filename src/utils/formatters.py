def format_fcfa(montant: int) -> str:
    """
    Formate un montant en FCFA avec séparateur de milliers par espace.
    
    Args:
        montant: Le montant entier en FCFA
        
    Returns:
        Le montant formaté (ex: "150 000 FCFA")
    """
    return f"{montant:,} FCFA".replace(",", " ")


def format_payment_mode(mode: str) -> str:
    """Affiche un mode de paiement lisiblement, y compris les modes personnalisés."""
    labels = {
        "especes": "Espèces",
        "cheque": "Chèque",
        "virement": "Virement bancaire",
        "virement_bancaire": "Virement bancaire",
        "mobile_money": "Mobile Money",
        "carte_bancaire": "Carte bancaire",
        "prelevement_bancaire": "Prélèvement bancaire",
        "paiement_en_ligne": "Paiement en ligne",
    }
    normalized_mode = mode.strip().lower()
    return labels.get(normalized_mode, normalized_mode.replace("_", " ").capitalize())
