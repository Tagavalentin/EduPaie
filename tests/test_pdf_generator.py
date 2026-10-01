import pytest
from pathlib import Path
from datetime import datetime
import os
import platform

from src.utils.pdf_generator import PDFGenerator, montant_en_lettres, print_pdf_file
from src.ui.receipt_viewer import ReceiptViewerDialog
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


def test_generate_receipt_creates_default_output_directory(tmp_path, monkeypatch):
    from src.utils import pdf_generator
    monkeypatch.setattr(pdf_generator, "get_data_path", lambda: tmp_path / "data")
    student = Student(1, "Kouassi", "Jean-Yves", "6ème A", "2025-2026", 150000)
    payment = Payment(1, 1, 50000, "2025-09-15", "carte_bancaire", "REC-2025-000002", 100000)

    result_path = PDFGenerator().generate_receipt(payment, student)

    assert result_path == tmp_path / "data" / "recus_pdf" / "recu_REC-2025-000002.pdf"
    assert result_path.is_file()


def test_receipt_viewer_displays_and_prints_pdf(tmp_path, qtbot, monkeypatch):
    student = Student(1, "Kouassi", "Jean-Yves", "6ème A", "2025-2026", 150000)
    payment = Payment(1, 1, 50000, "2025-09-15", "especes", "REC-2025-000003", 100000)
    receipt_path = PDFGenerator().generate_receipt(payment, student, tmp_path / "receipt.pdf")
    viewer = ReceiptViewerDialog(receipt_path)
    qtbot.addWidget(viewer)

    print_calls = []
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(os, "startfile", lambda path, operation: print_calls.append((path, operation)))
    viewer._print_receipt()

    assert viewer.document.pageCount() == 1
    assert viewer.print_button.text() == "Imprimer le reçu"
    assert print_calls == [(str(receipt_path.resolve()), "print")]


def test_print_pdf_file_sends_to_default_windows_printer(tmp_path, monkeypatch):
    receipt_path = tmp_path / "receipt.pdf"
    receipt_path.write_bytes(b"%PDF-1.4")
    print_calls = []
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(os, "startfile", lambda path, operation: print_calls.append((path, operation)), raising=False)

    print_pdf_file(receipt_path)

    assert print_calls == [(str(receipt_path.resolve()), "print")]
