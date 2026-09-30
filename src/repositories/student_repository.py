import sqlite3
from typing import List, Optional
from datetime import datetime

from src.database.connection import get_connection, close_connection
from src.models.student import Student


class StudentRepository:
    """Repository pour les opérations CRUD sur les élèves."""
    
    def create(self, student: Student) -> Student:
        """
        Crée un nouvel élève dans la base de données.
        
        Args:
            student: L'élève à créer (id doit être None)
            
        Returns:
            L'élève créé avec son id généré
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """
                INSERT INTO students (nom, prenom, classe, annee_scolaire, total_du)
                VALUES (?, ?, ?, ?, ?)
                """,
                (student.nom, student.prenom, student.classe, 
                 student.annee_scolaire, student.total_du)
            )
            conn.commit()
            student.id = cursor.lastrowid
            return student
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            close_connection(conn)
    
    def get_by_id(self, student_id: int) -> Optional[Student]:
        """
        Récupère un élève par son id.
        
        Args:
            student_id: L'id de l'élève
            
        Returns:
            L'élève trouvé ou None
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT id, nom, prenom, classe, annee_scolaire, total_du, created_at FROM students WHERE id = ?",
                (student_id,)
            )
            row = cursor.fetchone()
            
            if row:
                return Student(
                    id=row['id'],
                    nom=row['nom'],
                    prenom=row['prenom'],
                    classe=row['classe'],
                    annee_scolaire=row['annee_scolaire'],
                    total_du=row['total_du'],
                    created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
                )
            return None
        finally:
            close_connection(conn)
    
    def get_all(self) -> List[Student]:
        """
        Récupère tous les élèves.
        
        Returns:
            La liste de tous les élèves
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT id, nom, prenom, classe, annee_scolaire, total_du, created_at FROM students ORDER BY nom, prenom"
            )
            rows = cursor.fetchall()
            
            students = []
            for row in rows:
                students.append(Student(
                    id=row['id'],
                    nom=row['nom'],
                    prenom=row['prenom'],
                    classe=row['classe'],
                    annee_scolaire=row['annee_scolaire'],
                    total_du=row['total_du'],
                    created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
                ))
            return students
        finally:
            close_connection(conn)
    
    def search_by_name(self, search: str) -> List[Student]:
        """
        Recherche des élèves par nom ou prénom.
        
        Args:
            search: La chaîne de recherche (insensible à la casse)
            
        Returns:
            La liste des élèves correspondants
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """
                SELECT id, nom, prenom, classe, annee_scolaire, total_du, created_at 
                FROM students 
                WHERE nom LIKE ? OR prenom LIKE ?
                ORDER BY nom, prenom
                """,
                (f"%{search}%", f"%{search}%")
            )
            rows = cursor.fetchall()
            
            students = []
            for row in rows:
                students.append(Student(
                    id=row['id'],
                    nom=row['nom'],
                    prenom=row['prenom'],
                    classe=row['classe'],
                    annee_scolaire=row['annee_scolaire'],
                    total_du=row['total_du'],
                    created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
                ))
            return students
        finally:
            close_connection(conn)
    
    def filter_by_class(self, classe: str) -> List[Student]:
        """
        Filtre les élèves par classe.
        
        Args:
            classe: La classe
            
        Returns:
            La liste des élèves de cette classe
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """
                SELECT id, nom, prenom, classe, annee_scolaire, total_du, created_at 
                FROM students 
                WHERE classe = ?
                ORDER BY nom, prenom
                """,
                (classe,)
            )
            rows = cursor.fetchall()
            
            students = []
            for row in rows:
                students.append(Student(
                    id=row['id'],
                    nom=row['nom'],
                    prenom=row['prenom'],
                    classe=row['classe'],
                    annee_scolaire=row['annee_scolaire'],
                    total_du=row['total_du'],
                    created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
                ))
            return students
        finally:
            close_connection(conn)
    
    def update(self, student: Student) -> Student:
        """
        Met à jour un élève.
        
        Args:
            student: L'élève à mettre à jour (id doit être défini)
            
        Returns:
            L'élève mis à jour
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """
                UPDATE students 
                SET nom = ?, prenom = ?, classe = ?, annee_scolaire = ?, total_du = ?
                WHERE id = ?
                """,
                (student.nom, student.prenom, student.classe, 
                 student.annee_scolaire, student.total_du, student.id)
            )
            conn.commit()
            return student
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            close_connection(conn)
    
    def delete(self, student_id: int) -> bool:
        """
        Supprime un élève.
        
        Args:
            student_id: L'id de l'élève à supprimer
            
        Returns:
            True si supprimé, False si l'élève n'existe pas
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            close_connection(conn)
    
    def has_payments(self, student_id: int) -> bool:
        """
        Vérifie si un élève a des paiements.
        
        Args:
            student_id: L'id de l'élève
            
        Returns:
            True si l'élève a des paiements
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT COUNT(*) FROM payments WHERE student_id = ?",
                (student_id,)
            )
            return cursor.fetchone()[0] > 0
        finally:
            close_connection(conn)
