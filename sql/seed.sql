-- Données de test pour EduPaie
-- 15 élèves avec des montants réalistes en FCFA
-- Paiements variés : soldés, partiels, non payés

INSERT INTO students (nom, prenom, classe, annee_scolaire, total_du) VALUES
('Kouassi', 'Jean-Yves', '6ème A', '2025-2026', 150000),
('Diop', 'Fatou', '6ème B', '2025-2026', 150000),
('Kone', 'Aminata', '5ème A', '2025-2026', 175000),
('Touré', 'Ibrahim', '5ème B', '2025-2026', 175000),
('N''Goran', 'Marie-Claire', '4ème A', '2025-2026', 200000),
('Sangaré', 'Ousmane', '4ème B', '2025-2026', 200000),
('Koffi', 'Christelle', '3ème A', '2025-2026', 225000),
('Diallo', 'Mamadou', '3ème B', '2025-2026', 225000),
('Bamba', 'Yao', '2nde A', '2025-2026', 300000),
('Coulibaly', 'Adama', '2nde B', '2025-2026', 300000),
('Ouattara', 'Aicha', '1ère A', '2025-2026', 350000),
('Sissoko', 'Cheick', '1ère B', '2025-2026', 350000),
('Traoré', 'Bintou', 'Terminale A', '2025-2026', 450000),
('Dramane', 'Sékou', 'Terminale B', '2025-2026', 450000),
('Koné', 'Sitan', 'Terminale C', '2025-2026', 450000);

-- Paiements
-- Eleve 1 (Kouassi) : Soldé
INSERT INTO payments (student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres) VALUES
(1, 75000, '2025-09-15', 'especes', 'REC-2025-000001', 75000),
(1, 75000, '2025-10-20', 'mobile_money', 'REC-2025-000002', 0);

-- Eleve 2 (Diop) : Partiellement paye
INSERT INTO payments (student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres) VALUES
(2, 50000, '2025-09-10', 'especes', 'REC-2025-000003', 100000),
(2, 50000, '2025-10-15', 'virement', 'REC-2025-000004', 50000);

-- Eleve 3 (Kone) : Non paye
-- (aucun paiement)

-- Eleve 4 (Toure) : Solde
INSERT INTO payments (student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres) VALUES
(4, 87500, '2025-09-05', 'cheque', 'REC-2025-000005', 87500),
(4, 87500, '2025-10-10', 'especes', 'REC-2025-000006', 0);

-- Eleve 5 (N''Goran) : Partiellement paye
INSERT INTO payments (student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres) VALUES
(5, 100000, '2025-09-12', 'especes', 'REC-2025-000007', 100000);

-- Eleve 6 (Sangare) : Solde
INSERT INTO payments (student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres) VALUES
(6, 200000, '2025-09-01', 'virement', 'REC-2025-000008', 0);

-- Eleve 7 (Koffi) : Partiellement paye
INSERT INTO payments (student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres) VALUES
(7, 75000, '2025-09-20', 'mobile_money', 'REC-2025-000009', 150000),
(7, 75000, '2025-10-25', 'especes', 'REC-2025-000010', 75000);

-- Eleve 8 (Diallo) : Non paye
-- (aucun paiement)

-- Eleve 9 (Bamba) : Solde
INSERT INTO payments (student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres) VALUES
(9, 150000, '2025-08-25', 'especes', 'REC-2025-000011', 150000),
(9, 150000, '2025-09-30', 'virement', 'REC-2025-000012', 0);

-- Eleve 10 (Coulibaly) : Partiellement paye
INSERT INTO payments (student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres) VALUES
(10, 100000, '2025-09-18', 'cheque', 'REC-2025-000013', 200000);

-- Eleve 11 (Ouattara) : Partiellement paye
INSERT INTO payments (student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres) VALUES
(11, 175000, '2025-09-15', 'especes', 'REC-2025-000014', 175000);

-- Eleve 12 (Sissoko) : Solde
INSERT INTO payments (student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres) VALUES
(12, 350000, '2025-08-20', 'virement', 'REC-2025-000015', 0);

-- Eleve 13 (Traore) : Partiellement paye
INSERT INTO payments (student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres) VALUES
(13, 150000, '2025-09-10', 'mobile_money', 'REC-2025-000016', 300000),
(13, 150000, '2025-10-15', 'especes', 'REC-2025-000017', 150000);

-- Eleve 14 (Dramane) : Non paye
-- (aucun paiement)

-- Eleve 15 (Kone) : Solde
INSERT INTO payments (student_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres) VALUES
(15, 225000, '2025-08-15', 'especes', 'REC-2025-000018', 225000),
(15, 225000, '2025-09-20', 'virement', 'REC-2025-000019', 0);
