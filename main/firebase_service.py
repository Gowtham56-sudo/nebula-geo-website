from .firebase_config import db
from google.cloud.firestore_v1.base_query import FieldFilter
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class GenericDoc:
    def __init__(self, doc_id, data):
        self.id = doc_id
        for key, val in data.items():
            setattr(self, key, val)

class ServiceDoc(GenericDoc):
    pass

class TeamMemberDoc(GenericDoc):
    pass

class TestimonialDoc(GenericDoc):
    pass

class PortfolioProjectDoc:
    def __init__(self, doc_id, data):
        self.id = doc_id
        self.title = data.get('title', '')
        self.description = data.get('description', '')
        self.category = data.get('category', 'web')
        self.tech_stack = data.get('tech_stack', '')
        self.image_url = data.get('image_url', '')
        self.project_url = data.get('project_url', '')
        self.is_featured = data.get('is_featured', False)
        self.order = data.get('order', 0)
        self.created_at = data.get('created_at', None)

    def get_tech_list(self):
        if not self.tech_stack:
            return []
        return [t.strip() for t in self.tech_stack.split(',') if t.strip()]

class InternshipProgramDoc:
    def __init__(self, doc_id, data):
        self.id = doc_id
        self.title = data.get('title', '')
        self.description = data.get('description', '')
        self.duration = data.get('duration', '')
        self.stipend = data.get('stipend', 'Performance Based')
        self.skills = data.get('skills', '')
        self.is_active = data.get('is_active', True)
        self.order = data.get('order', 0)

    def get_skills_list(self):
        if not self.skills:
            return []
        return [s.strip() for s in self.skills.split(',') if s.strip()]


def get_active_services(limit=None):
    if db is None:
        logger.error("Firestore database connection is not initialized.")
        return []
    try:
        docs = db.collection('services').order_by('order').stream()
        active_services = []
        for doc in docs:
            d = doc.to_dict()
            if d.get('is_active', True):
                active_services.append(ServiceDoc(doc.id, d))
                if limit and len(active_services) == limit:
                    break
        return active_services
    except Exception as e:
        logger.error(f"Error fetching active services: {e}")
        return []

def get_all_services():
    if db is None:
        return []
    try:
        docs = db.collection('services').order_by('order').stream()
        return [ServiceDoc(doc.id, doc.to_dict()) for doc in docs]
    except Exception as e:
        logger.error(f"Error fetching all services: {e}")
        return []

def get_featured_projects(limit=None):
    if db is None:
        return []
    try:
        docs = db.collection('portfolio_projects').order_by('order').stream()
        featured_projects = []
        for doc in docs:
            d = doc.to_dict()
            if d.get('is_featured', False):
                featured_projects.append(PortfolioProjectDoc(doc.id, d))
                if limit and len(featured_projects) == limit:
                    break
        return featured_projects
    except Exception as e:
        logger.error(f"Error fetching featured projects: {e}")
        return []

def get_all_projects(category=None):
    if db is None:
        return []
    try:
        docs = db.collection('portfolio_projects').order_by('order').stream()
        projects = []
        for doc in docs:
            d = doc.to_dict()
            if not category or category == 'all' or d.get('category') == category:
                projects.append(PortfolioProjectDoc(doc.id, d))
        return projects
    except Exception as e:
        logger.error(f"Error fetching all projects: {e}")
        return []

def get_active_testimonials(limit=None):
    if db is None:
        return []
    try:
        docs = db.collection('testimonials').order_by('created_at', direction='DESCENDING').stream()
        active_testimonials = []
        for doc in docs:
            d = doc.to_dict()
            if d.get('is_active', True):
                active_testimonials.append(TestimonialDoc(doc.id, d))
                if limit and len(active_testimonials) == limit:
                    break
        return active_testimonials
    except Exception as e:
        logger.error(f"Error fetching active testimonials: {e}")
        return []

def get_active_team_members():
    if db is None:
        return []
    try:
        docs = db.collection('team_members').order_by('order').stream()
        return [TeamMemberDoc(doc.id, doc.to_dict()) for doc in docs if doc.to_dict().get('is_active', True)]
    except Exception as e:
        logger.error(f"Error fetching active team members: {e}")
        return []

def get_active_internship_programs():
    if db is None:
        return []
    try:
        docs = db.collection('internship_programs').order_by('order').stream()
        return [InternshipProgramDoc(doc.id, doc.to_dict()) for doc in docs if doc.to_dict().get('is_active', True)]
    except Exception as e:
        logger.error(f"Error fetching active internship programs: {e}")
        return []

def create_contact_message(data):
    if db is None:
        logger.error("Firestore database connection is not initialized.")
        return None
    try:
        data['created_at'] = datetime.utcnow().isoformat()
        data['status'] = 'new'
        doc_ref = db.collection('contact_messages').document()
        doc_ref.set(data)
        return doc_ref.id
    except Exception as e:
        logger.error(f"Error writing contact message to Firestore: {e}")
        return None

def create_internship_application(data):
    if db is None:
        logger.error("Firestore database connection is not initialized.")
        return None
    try:
        data['created_at'] = datetime.utcnow().isoformat()
        doc_ref = db.collection('internship_applications').document()
        doc_ref.set(data)
        return doc_ref.id
    except Exception as e:
        logger.error(f"Error writing internship application to Firestore: {e}")
        return None
