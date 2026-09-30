def format_fcfa(montant: int) -> str:
    """
    Formate un montant en FCFA avec séparateur de milliers par espace.
    
    Args:
        montant: Le montant entier en FCFA
        
    Returns:
        Le montant formaté (ex: "150 000 FCFA")
    """
    return f"{montant:,} FCFA".replace(",", " ")
