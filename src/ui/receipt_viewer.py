from pathlib import Path

from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import QDialog, QHBoxLayout, QMessageBox, QPushButton, QVBoxLayout
from src.utils.pdf_generator import print_pdf_file


class ReceiptViewerDialog(QDialog):
    """Affiche un reçu PDF et permet de l'imprimer."""

    def __init__(self, pdf_path: Path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Reçu de paiement")
        self.setMinimumSize(800, 600)

        self.document = QPdfDocument(self)
        self.pdf_path = Path(pdf_path).resolve()
        load_error = self.document.load(str(self.pdf_path))
        if load_error != QPdfDocument.Error.None_:
            raise RuntimeError(f"Impossible d'ouvrir le reçu PDF : {pdf_path}")

        self.pdf_view = QPdfView(self)
        self.pdf_view.setDocument(self.document)
        self.pdf_view.setZoomMode(QPdfView.ZoomMode.FitInView)

        self.print_button = QPushButton("Imprimer le reçu")
        self.print_button.clicked.connect(self._print_receipt)
        close_button = QPushButton("Fermer")
        close_button.clicked.connect(self.accept)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.print_button)
        buttons_layout.addWidget(close_button)

        layout = QVBoxLayout(self)
        layout.addWidget(self.pdf_view, stretch=1)
        layout.addLayout(buttons_layout)

    def _print_receipt(self):
        try:
            print_pdf_file(self.pdf_path)
        except Exception as error:
            QMessageBox.warning(self, "Impression impossible", str(error))
