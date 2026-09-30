import pytest
from pathlib import Path
from datetime import datetime

from src.utils.pdf_generator import PDFGenerator, montant_en_lettres
from src.models.payment import Payment
from src.models.student import Student


def test_montant_en_lettres():
    """Test la conversion en toutes lettres."""
    assert montant_en_lettres(1) == "Un francs CFA"
    assert montant_en_lettres(10) == "Dix francs CFA"
    assert montant_en_lettres(100) == "Cent francs CFA"
    assert montant_en_lettres(1000) == "Mille francs CFA"
    assert montant_en_lettres(50000) == "Cinquante mille francs CFA"
    assert montant_en_lettres(150000) == "Cent cinquante mille francs CFA"


def test_generate_receipt(tmp_path):
    """Test la génération d'un reçu PDF."""
    generator = PDFGenerator()
    
    # Créer des objets de test
    student = Student(
        id=1,
        nom="Kouassi",
        prenom="Jean-Yves",
        classe="6ème A",
        annee_scolaire="2025-2026",
        total_du=150000
    )
    
    payment = Payment(
        id=1,
        student_id=1,
        montant=50000,
        date_paiement="2025-09-15",
        mode_paiement="especes",
        numero_recu="REC-2025-000001",
        solde_apres=100000
    )
    
    # Générer le PDF
    output_path = tmp_path / "test_recu.pdf"
    result_path = generator.generate_receipt(payment, student, output_path)
    
    # Vérifier que le fichier existe
    assert result_path.exists()
    assert result_path.stat().st_size > 0  # Fichier non vide
    
    # Vérifier que c'est bien un PDF
    with open(result_path, 'rb') as f:
        content = f.read()
        assert content.startswith(b'%PDF')  # Les fichiers PDF commencent par %PDF
        assert b'%%EOF' in content  # Les fichiers PDF se terminent par %%EOF
