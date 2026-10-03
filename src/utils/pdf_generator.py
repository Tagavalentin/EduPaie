import os
import platform
import subprocess
from reportlab.lib.pagesizes import A6
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas
from pathlib import Path
from typing import Optional

from src.utils.formatters import format_fcfa, format_payment_mode
from src.utils.paths import get_base_path, get_data_path


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
        self.page_width, self.page_height = A6
        self.margin = 0.8 * cm
        self.content_width = self.page_width - 2 * self.margin
    
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
        
        c = canvas.Canvas(str(output_path), pagesize=A6)
        
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
        """Dessine le logo et la marque EduPaie."""
        top = self.page_height - self.margin
        icon_path = get_base_path() / "assets" / "edupaie.png"
        icon_size = 1.15 * cm
        c.drawImage(
            str(icon_path), self.margin, top - icon_size,
            width=icon_size, height=icon_size, mask="auto",
        )

        brand_x = self.margin + icon_size + 0.25 * cm
        c.setFillColor(colors.HexColor("#173d43"))
        c.setFont("Helvetica-Bold", 14)
        c.drawString(brand_x, top - 0.45 * cm, "EduPaie")
        c.setFont("Helvetica", 7)
        c.drawString(brand_x, top - 0.85 * cm, "GESTION DES PAIEMENTS SCOLAIRES")

        c.setStrokeColor(colors.HexColor("#83c4a5"))
        c.setLineWidth(1.2)
        c.line(self.margin, top - 1.4 * cm, self.page_width - self.margin, top - 1.4 * cm)
    
    def _draw_title(self, c: canvas.Canvas, receipt_number: str):
        """Dessine le titre du reçu."""
        top = self.page_height - self.margin
        c.setFillColor(colors.darkblue)
        c.setFont("Helvetica-Bold", 15)
        c.drawCentredString(self.page_width / 2, top - 1.85 * cm, "REÇU DE PAIEMENT")
        
        c.setFont("Helvetica", 8.5)
        c.setFillColor(colors.black)
        c.drawCentredString(self.page_width / 2, top - 2.35 * cm, f"N° {receipt_number}")
    
    def _draw_school_info(self, c: canvas.Canvas):
        """Dessine les informations de l'école."""
        y = self.page_height - self.margin - 3.15 * cm
        
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(colors.black)
        c.drawString(self.margin, y, "ÉCOLE - GESTION SCOLAIRE")
        
        c.setFont("Helvetica", 7.5)
        c.drawString(self.margin, y - 0.4 * cm, "Reçu de paiement scolaire")
    
    def _draw_student_info(self, c: canvas.Canvas, student):
        """Dessine les informations de l'élève."""
        y = self.page_height - self.margin - 4.15 * cm
        c.setFont("Helvetica-Bold", 8.5)
        c.setFillColor(colors.black)
        c.drawString(self.margin, y, "ÉLÈVE")

        y -= 0.5 * cm
        y = self._draw_labeled_value(c, "Nom :", f"{student.nom} {student.prenom}", y)
        y = self._draw_labeled_value(c, "Classe :", student.classe, y - 0.12 * cm)
        y = self._draw_labeled_value(c, "Année :", student.annee_scolaire, y - 0.12 * cm)
        self._payment_box_top = y - 0.25 * cm

    def _draw_labeled_value(self, c: canvas.Canvas, label: str, value: str, y: float) -> float:
        label_width = 2.2 * cm
        c.setFont("Helvetica-Bold", 8)
        c.drawString(self.margin, y, label)
        c.setFont("Helvetica", 8)
        lines = simpleSplit(str(value), "Helvetica", 8, self.content_width - label_width)
        for index, line in enumerate(lines):
            c.drawString(self.margin + label_width, y - index * 9.5, line)
        return y - max(1, len(lines)) * 9.5
    
    def _draw_payment_details(self, c: canvas.Canvas, payment):
        """Dessine les détails du paiement dans un encadré au format A6."""
        box_height = 3.35 * cm
        box_bottom = self._payment_box_top - box_height
        c.setFillColor(colors.HexColor("#f4f8f5"))
        c.setStrokeColor(colors.HexColor("#83c4a5"))
        c.setLineWidth(0.8)
        c.roundRect(self.margin, box_bottom, self.content_width, box_height, 4, fill=1, stroke=1)

        x = self.margin + 0.3 * cm
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(x, self._payment_box_top - 0.55 * cm, "DÉTAILS DU PAIEMENT")

        c.setFont("Helvetica", 8)
        c.drawString(x, self._payment_box_top - 1.2 * cm, f"Date : {payment.date_paiement}")
        c.drawString(x, self._payment_box_top - 1.8 * cm, f"Mode : {format_payment_mode(payment.mode_paiement)}")

        c.setFillColor(colors.HexColor("#173d43"))
        c.setFont("Helvetica-Bold", 11)
        c.drawString(x, box_bottom + 0.45 * cm, f"Montant : {format_fcfa(payment.montant)}")
        self._amount_words_y = box_bottom - 0.55 * cm
    
    def _draw_amount_in_words(self, c: canvas.Canvas, amount: int):
        """Dessine le montant en toutes lettres."""
        y = self._amount_words_y
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(colors.black)
        c.drawString(self.margin, y, "Arrêté la présente somme à :")
        
        c.setFont("Helvetica-Oblique", 7.5)
        lines = simpleSplit(montant_en_lettres(amount), "Helvetica-Oblique", 7.5, self.content_width)
        for index, line in enumerate(lines):
            c.drawString(self.margin, y - 0.42 * cm - index * 9, line)
    
    def _draw_footer(self, c: canvas.Canvas, payment):
        """Dessine le pied de page."""
        y = 1.75 * cm
        
        c.setStrokeColor(colors.HexColor("#83c4a5"))
        c.setLineWidth(0.8)
        c.line(self.margin, y + 0.35 * cm, self.page_width - self.margin, y + 0.35 * cm)

        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.black)
        c.drawString(self.margin, y, f"Solde après ce paiement : {format_fcfa(payment.solde_apres)}")
        
        # Date d'émission
        from datetime import datetime
        c.setFont("Helvetica", 6.5)
        c.drawCentredString(self.page_width / 2, 0.75 * cm,
                           f"Reçu généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
