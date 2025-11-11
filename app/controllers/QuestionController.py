"""
Question Controller
Menangani Q&A system
"""
from flask import jsonify, request
from app.models.Question import Question

class QuestionController:
    """Controller untuk Q&A endpoints"""
    
    @staticmethod
    def index():
        """Get all questions (admin)"""
        questions = Question.get_all()
        
        pending = [q for q in questions if q['status'] == 'pending']
        answered = [q for q in questions if q['status'] == 'answered']
        
        return jsonify({
            "status": "success",
            "data": questions,
            "summary": {
                "total": len(questions),
                "pending": len(pending),
                "answered": len(answered)
            }
        })
    
    @staticmethod
    def get_answered():
        """Get answered questions (public)"""
        questions = Question.get_answered()
        return jsonify({
            "status": "success",
            "data": questions,
            "total": len(questions)
        })
    
    @staticmethod
    def store():
        """Submit new question"""
        data = request.json
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        question = data.get("question", "").strip()
        
        if not name or not email or not question:
            return jsonify({
                "status": "error",
                "message": "Name, email, and question are required"
            }), 400
        
        if "@" not in email or "." not in email:
            return jsonify({
                "status": "error",
                "message": "Invalid email format"
            }), 400
        
        try:
            question_id = Question.create({
                "name": name,
                "email": email,
                "question": question
            })
            return jsonify({
                "status": "success",
                "message": "Question submitted successfully! We'll answer it soon.",
                "id": question_id
            })
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
    
    @staticmethod
    def answer(question_id):
        """Answer a question (admin)"""
        data = request.json
        answer = data.get("answer", "").strip()
        answered_by = data.get("answered_by", "Admin").strip()
        
        if not answer:
            return jsonify({
                "status": "error",
                "message": "Answer is required"
            }), 400
        
        try:
            success = Question.answer(question_id, answer, answered_by)
            if success:
                return jsonify({
                    "status": "success",
                    "message": "Question answered successfully"
                })
            return jsonify({
                "status": "error",
                "message": "Question not found"
            }), 404
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
    
    @staticmethod
    def destroy(question_id):
        """Delete question"""
        success = Question.delete_by_id(question_id)
        if success:
            return jsonify({
                "status": "success",
                "message": "Question deleted successfully"
            })
        return jsonify({
            "status": "error",
            "message": "Question not found"
        }), 404
