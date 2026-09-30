-- Schéma de la base de données EduPaie
-- Devise : FCFA (entiers, pas de décimales)

-- Table des élèves
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    classe TEXT NOT NULL,
    annee_scolaire TEXT NOT NULL,
    total_du INTEGER NOT NULL CHECK (total_du >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des paiements
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    montant INTEGER NOT NULL CHECK (montant > 0),
    date_paiement TEXT NOT NULL,
    mode_paiement TEXT NOT NULL CHECK (mode_paiement IN ('especes', 'cheque', 'virement', 'mobile_money')),
    numero_recu TEXT UNIQUE NOT NULL,
    solde_apres INTEGER NOT NULL CHECK (solde_apres >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE RESTRICT
);

-- Index pour optimiser les requêtes
CREATE INDEX IF NOT EXISTS idx_payments_student_id ON payments(student_id);
CREATE INDEX IF NOT EXISTS idx_payments_numero_recu ON payments(numero_recu);
CREATE INDEX IF NOT EXISTS idx_students_classe ON students(classe);
