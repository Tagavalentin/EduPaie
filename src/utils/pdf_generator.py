import os
import platform
import subprocess
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
from typing import Optional

from src.utils.formatters import format_fcfa, format_payment_mode
from src.utils.paths import get_data_path


def montant_en_lettres(n: int) -> str:
    """
    Convertit un montant en toutes lettres en français.
    
    Args:
        n: Le montant entier en FCFA
        
    Returns:
        Le montant en toutes lettres (ex: "Cinquante mille francs CFA")
    """
    from num2words import num2words
    return num2words(n, lang='fr').capitalize() + " francs CFA"


def print_pdf_file(pdf_path: Path) -> None:
    """Envoie un PDF à l'imprimante par défaut du système."""
    pdf_path = Path(pdf_path).resolve()
    if not pdf_path.is_file():
        raise FileNotFoundError(f"Fichier PDF introuvable : {pdf_path}")

    if platform.system() == "Windows":
        os.startfile(str(pdf_path), "print")
    else:
        subprocess.run(["lp", str(pdf_path)], check=True)


class PDFGenerator:
    """Générateur de reçus PDF."""
    
    def __init__(self):
        self.page_width, self.page_height = A4
        self.margin = 2 * cm
    
    def generate_receipt(self, payment, student, output_path: Optional[Path] = None) -> Path:
        """
        Génère un reçu PDF pour un paiement.
        
        Args:
            payment: L'objet Payment
            student: L'objet Student
            output_path: Le chemin de sortie (optionnel)
            
        Returns:
            Le chemin du fichier PDF généré
        """
        if output_path is None:
            output_path = get_data_path() / "recus_pdf" / f"recu_{payment.numero_recu}.pdf"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        c = canvas.Canvas(str(output_path), pagesize=A4)
        
        # En-tête
        self._draw_header(c)
        
        # Titre
        self._draw_title(c, payment.numero_recu)
        
        # Informations de l'école
        self._draw_school_info(c)
        
        # Informations de l'élève
        self._draw_student_info(c, student)
        
        # Détails du paiement
        self._draw_payment_details(c, payment)
        
        # Montant en toutes lettres
        self._draw_amount_in_words(c, payment.montant)
        
        # Pied de page
        self._draw_footer(c, payment)
        
        c.save()
        
        return output_path
    
    def _draw_header(self, c: canvas.Canvas):
        """Dessine l'en-tête du reçu."""
        # Ligne supérieure
        c.setStrokeColor(colors.darkblue)
        c.setLineWidth(2)
        c.line(self.margin, self.page_height - self.margin, 
               self.page_width - self.margin, self.page_height - self.margin)
    
    def _draw_title(self, c: canvas.Canvas, receipt_number: str):
        """Dessine le titre du reçu."""
        c.setFillColor(colors.darkblue)
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(self.page_width / 2, self.page_height - 3 * cm, "REÇU DE PAIEMENT")
        
        c.setFont("Helvetica", 14)
        c.setFillColor(colors.black)
        c.drawCentredString(self.page_width / 2, self.page_height - 3.5 * cm, f"N° {receipt_number}")
    
    def _draw_school_info(self, c: canvas.Canvas):
        """Dessine les informations de l'école."""
        y = self.page_height - 5 * cm
        
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(colors.black)
        c.drawString(self.margin, y, "ÉCOLE - GESTION SCOLAIRE")
        
        c.setFont("Helvetica", 12)
        c.drawString(self.margin, y - 0.7 * cm, "Reçu de paiement scolaire")
    
    def _draw_student_info(self, c: canvas.Canvas, student):
        """Dessine les informations de l'élève."""
        y = self.page_height - 7 * cm
        
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.black)
        c.drawString(self.margin, y, "Élève :")
        
        c.setFont("Helvetica", 12)
        c.drawString(self.margin + 2 * cm, y, f"{student.nom} {student.prenom}")
        c.drawString(self.margin, y - 0.7 * cm, f"Classe : {student.classe}")
        c.drawString(self.margin, y - 1.4 * cm, f"Année scolaire : {student.annee_scolaire}")
    
    def _draw_payment_details(self, c: canvas.Canvas, payment):
        """Dessine les détails du paiement."""
        y = self.page_height - 10 * cm
        
        # Encadré pour les détails
        c.setStrokeColor(colors.gray)
        c.setLineWidth(1)
        c.rect(self.margin, y - 3 * cm, self.page_width - 2 * self.margin, 3 * cm)
        
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.black)
        c.drawString(self.margin + 0.5 * cm, y - 0.5 * cm, "Détails du paiement :")
        
        c.setFont("Helvetica", 12)
        c.drawString(self.margin + 0.5 * cm, y - 1.2 * cm, f"Date : {payment.date_paiement}")
        c.drawString(self.margin + 0.5 * cm, y - 1.9 * cm, f"Mode de paiement : {format_payment_mode(payment.mode_paiement)}")
        
        # Montant
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(colors.darkblue)
        c.drawString(self.margin + 0.5 * cm, y - 2.6 * cm, f"Montant : {format_fcfa(payment.montant)}")
    
    def _draw_amount_in_words(self, c: canvas.Canvas, amount: int):
        """Dessine le montant en toutes lettres."""
        y = self.page_height - 14 * cm
        
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.black)
        c.drawString(self.margin, y, "Arrêté la présente somme à :")
        
        c.setFont("Helvetica-Oblique", 12)
        c.drawString(self.margin, y - 0.7 * cm, montant_en_lettres(amount))
    
    def _draw_footer(self, c: canvas.Canvas, payment):
        """Dessine le pied de page."""
        y = 2 * cm
        
        # Solde après (lu depuis le paiement, figé au moment du paiement)
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.black)
        c.drawString(self.margin, y, f"Solde après ce paiement : {format_fcfa(payment.solde_apres)}")
        
        # Ligne inférieure
        c.setStrokeColor(colors.darkblue)
        c.setLineWidth(2)
        c.line(self.margin, 1 * cm, self.page_width - self.margin, 1 * cm)
        
        # Date d'émission
        from datetime import datetime
        c.setFont("Helvetica", 10)
        c.drawCentredString(self.page_width / 2, 0.5 * cm, 
                           f"Reçu généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
