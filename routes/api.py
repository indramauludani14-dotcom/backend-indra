"""
API Routes
Define all API routes
"""
from flask import Blueprint
from app.controllers import (
    NewsController,
    CMSController,
    QuestionController,
    AuthController,
    FurnitureController
)
from app.controllers.FAQController import FAQController
from app.controllers.LayoutController import LayoutController
from app.controllers.ContactController import ContactController
from app.controllers.HouseLayoutController import HouseLayoutController
from app.controllers.SocialMediaController import SocialMediaController

# Create blueprint
api = Blueprint('api', __name__, url_prefix='/api')

# ===== STATUS =====
@api.route('/status', methods=['GET'])
def status():
    from flask import jsonify
    return jsonify({
        "status": "success",
        "service": "FurniLayout API",
        "version": "2.0.0"
    })

# ===== NEWS ROUTES =====
@api.route('/news', methods=['GET'])
def get_news():
    return NewsController.index()

@api.route('/news/<int:news_id>', methods=['GET'])
def get_news_detail(news_id):
    return NewsController.show(news_id)

@api.route('/news', methods=['POST'])
def create_news():
    return NewsController.store()

@api.route('/news/<int:news_id>', methods=['PUT'])
def update_news(news_id):
    return NewsController.update(news_id)

@api.route('/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    return NewsController.destroy(news_id)

# ===== FAQ ROUTES =====
@api.route('/faqs', methods=['GET'])
def get_faqs():
    """Get all FAQs (for admin)"""
    return FAQController.index()

@api.route('/faqs/active', methods=['GET'])
def get_active_faqs():
    """Get active FAQs (for public)"""
    return FAQController.get_active()

@api.route('/faqs/category/<category>', methods=['GET'])
def get_faqs_by_category(category):
    """Get FAQs by category"""
    return FAQController.get_by_category(category)

@api.route('/faqs/<int:faq_id>', methods=['GET'])
def get_faq_detail(faq_id):
    return FAQController.show(faq_id)

@api.route('/faqs', methods=['POST'])
def create_faq():
    return FAQController.store()

@api.route('/faqs/<int:faq_id>', methods=['PUT'])
def update_faq(faq_id):
    return FAQController.update(faq_id)

@api.route('/faqs/<int:faq_id>', methods=['DELETE'])
def delete_faq(faq_id):
    return FAQController.destroy(faq_id)

# ===== FURNITURE ROUTES =====
@api.route('/furniture', methods=['GET'])
def get_furniture():
    return FurnitureController.index()

@api.route('/furniture/<int:furniture_id>', methods=['GET'])
def get_furniture_detail(furniture_id):
    return FurnitureController.show(furniture_id)

# ===== CMS ROUTES =====
@api.route('/cms/content', methods=['GET'])
def get_cms_content():
    return CMSController.get_content()

@api.route('/cms/content', methods=['PUT'])
def update_cms_content():
    return CMSController.update_content()

@api.route('/cms/theme', methods=['GET'])
def get_theme():
    return CMSController.get_theme()

@api.route('/cms/theme', methods=['PUT'])
def update_theme():
    return CMSController.update_theme()

# ===== QUESTION ROUTES =====
@api.route('/questions', methods=['POST'])
def submit_question():
    return QuestionController.store()

@api.route('/questions/answered', methods=['GET'])
def get_answered_questions():
    return QuestionController.get_answered()

@api.route('/questions/all', methods=['GET'])
def get_all_questions():
    return QuestionController.index()

@api.route('/questions/<int:question_id>/answer', methods=['PUT'])
def answer_question(question_id):
    return QuestionController.answer(question_id)

@api.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    return QuestionController.destroy(question_id)

# ===== AUTH ROUTES =====
@api.route('/cms/login', methods=['POST'])
def admin_login():
    return AuthController.login()

# ===== LAYOUT ROUTES =====
@api.route('/layout/predict', methods=['POST'])
def predict_layout():
    return LayoutController.predict_batch()

@api.route('/layout/recommendations', methods=['POST'])
def get_recommendations():
    return LayoutController.get_floor_recommendations()

@api.route('/layout/reset', methods=['POST'])
def reset_layout():
    return LayoutController.reset_layout()

@api.route('/layout/auto-place', methods=['POST'])
def auto_place_furniture():
    return LayoutController.auto_place_furniture()

# ===== UPLOAD ROUTES =====
@api.route('/news/upload-image', methods=['POST'])
def upload_news_image():
    return NewsController.upload_image()

@api.route('/news/images/<filename>', methods=['GET'])
def serve_image(filename):
    return LayoutController.serve_news_image(filename)

# ===== CONTACT ROUTES =====
@api.route('/contact', methods=['POST'])
def submit_contact():
    """Submit contact form"""
    return ContactController.store()

@api.route('/contact/messages', methods=['GET'])
def get_contact_messages():
    """Get all contact messages (admin)"""
    return ContactController.index()

@api.route('/contact/messages/unread', methods=['GET'])
def get_unread_messages():
    """Get unread messages (admin)"""
    return ContactController.get_unread()

@api.route('/contact/messages/<int:message_id>/read', methods=['PUT'])
def mark_message_read(message_id):
    """Mark message as read"""
    return ContactController.mark_read(message_id)

@api.route('/contact/messages/<int:message_id>', methods=['DELETE'])
def delete_contact_message(message_id):
    """Delete contact message"""
    return ContactController.destroy(message_id)

# ===== HOUSE LAYOUT ROUTES =====
@api.route('/layouts', methods=['GET'])
def get_all_layouts():
    """Get all saved layouts (admin)"""
    return HouseLayoutController.index()

@api.route('/layouts/public', methods=['GET'])
def get_public_layouts():
    """Get public layouts"""
    return HouseLayoutController.get_public()

@api.route('/layouts/user/<int:user_id>', methods=['GET'])
def get_user_layouts(user_id):
    """Get layouts by user ID"""
    return HouseLayoutController.get_by_user(user_id)

@api.route('/layouts/<int:layout_id>', methods=['GET'])
def get_layout_detail(layout_id):
    """Get single layout detail"""
    return HouseLayoutController.show(layout_id)

@api.route('/layouts', methods=['POST'])
def save_layout():
    """Save new layout"""
    return HouseLayoutController.store()

@api.route('/layouts/<int:layout_id>', methods=['PUT'])
def update_saved_layout(layout_id):
    """Update saved layout"""
    return HouseLayoutController.update(layout_id)

@api.route('/layouts/<int:layout_id>/toggle-public', methods=['PUT'])
def toggle_layout_public(layout_id):
    """Toggle layout public status"""
    return HouseLayoutController.toggle_public(layout_id)

@api.route('/layouts/<int:layout_id>', methods=['DELETE'])
def delete_saved_layout(layout_id):
    """Delete saved layout"""
    return HouseLayoutController.destroy(layout_id)

# ===== ACTIVITY LOG ROUTES =====
@api.route('/activity-logs', methods=['GET'])
def get_all_activity_logs():
    """Get all activity logs (admin)"""
    from app.controllers.ActivityLogController import ActivityLogController
    return ActivityLogController.index()

@api.route('/activity-logs/user/<int:user_id>', methods=['GET'])
def get_user_activity_logs(user_id):
    """Get activity logs by user"""
    from app.controllers.ActivityLogController import ActivityLogController
    return ActivityLogController.get_by_user(user_id)

@api.route('/activity-logs/<entity_type>/<int:entity_id>', methods=['GET'])
def get_entity_activity_logs(entity_type, entity_id):
    """Get activity logs by entity"""
    from app.controllers.ActivityLogController import ActivityLogController
    return ActivityLogController.get_by_entity(entity_type, entity_id)

@api.route('/activity-logs/cleanup', methods=['DELETE'])
def cleanup_old_logs():
    """Delete old activity logs"""
    from app.controllers.ActivityLogController import ActivityLogController
    return ActivityLogController.cleanup()


# ===== SOCIAL MEDIA ROUTES =====
@api.route('/social-media', methods=['GET'])
def get_social_media():
    """Get all social media links (admin)"""
    return SocialMediaController.index()

@api.route('/social-media/active', methods=['GET'])
def get_active_social_media():
    """Get active social media links (public)"""
    return SocialMediaController.get_active()

@api.route('/social-media', methods=['POST'])
def create_social_media():
    """Create social media link"""
    return SocialMediaController.store()

@api.route('/social-media/<int:social_id>', methods=['PUT'])
def update_social_media(social_id):
    """Update social media link"""
    return SocialMediaController.update(social_id)

@api.route('/social-media/<int:social_id>', methods=['DELETE'])
def delete_social_media(social_id):
    """Delete social media link"""
    return SocialMediaController.destroy(social_id)

