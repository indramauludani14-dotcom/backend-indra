"""
Question Model
Mengelola Q&A/pertanyaan user
"""
from app.models.BaseModel import BaseModel

class Question(BaseModel):
    """Question model untuk Q&A system"""
    
    table_name = "questions"
    
    @classmethod
    def get_all(cls):
        """Get all questions with formatted dates"""
        conn = cls.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, name, email, question, answer, status,
                   DATE_FORMAT(created_at, '%Y-%m-%d %H:%i') as created_at,
                   DATE_FORMAT(answered_at, '%Y-%m-%d %H:%i') as answered_at,
                   answered_by
            FROM questions 
            ORDER BY 
                CASE WHEN status = 'pending' THEN 0 ELSE 1 END,
                created_at DESC
        """)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    
    @classmethod
    def get_answered(cls):
        """Get only answered questions"""
        conn = cls.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, name, question, answer, 
                   DATE_FORMAT(created_at, '%Y-%m-%d %H:%i') as created_at,
                   DATE_FORMAT(answered_at, '%Y-%m-%d %H:%i') as answered_at
            FROM questions 
            WHERE status = 'answered' AND answer IS NOT NULL
            ORDER BY answered_at DESC
        """)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    
    @classmethod
    def create(cls, data):
        """Create new question"""
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO questions (name, email, question, status) VALUES (%s, %s, %s, 'pending')",
            (data.get('name'), data.get('email'), data.get('question'))
        )
        question_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return question_id
    
    @classmethod
    def answer(cls, question_id, answer, answered_by='Admin'):
        """Answer a question"""
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE questions 
            SET answer = %s, status = 'answered', answered_at = NOW(), answered_by = %s
            WHERE id = %s
        """, (answer, answered_by, question_id))
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        return affected > 0
