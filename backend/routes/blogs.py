from flask import Blueprint, request, jsonify
from firebase_config import initialize_firebase
from firebase_admin import firestore
import slugify
from routes.auth import verify_admin

blogs_bp = Blueprint('blogs', __name__)
db, bucket = initialize_firebase()

def get_slug(title):
    return slugify.slugify(title)

# --- Public Endpoints ---

@blogs_bp.route('/api/blogs', methods=['GET'])
def get_blogs():
    try:
        category = request.args.get('category')
        limit = int(request.args.get('limit', 10))
        
        query = db.collection('blogs').where('published', '==', True).order_by('created_at', direction=firestore.Query.DESCENDING)
        
        if category:
            query = query.where('category', '==', category)
            
        docs = query.limit(limit).stream()
        
        blogs = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            blogs.append(data)
            
        return jsonify(blogs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blogs_bp.route('/api/blogs/<slug>', methods=['GET'])
def get_blog_by_slug(slug):
    try:
        # Query by slug
        docs = db.collection('blogs').where('slug', '==', slug).limit(1).stream()
        blog_doc = next(docs, None)
        
        if not blog_doc:
            return jsonify({"error": "Blog not found"}), 404
            
        data = blog_doc.to_dict()
        data['id'] = blog_doc.id
        
        # Increment view count
        blog_doc.reference.update({'views': firestore.Increment(1)})
        
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blogs_bp.route('/api/blog-categories', methods=['GET'])
def get_categories():
    try:
        docs = db.collection('blog_categories').order_by('name').stream()
        categories = [{"id": doc.id, **doc.to_dict()} for doc in docs]
        return jsonify(categories), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Admin Endpoints ---

@blogs_bp.route('/api/admin/blogs', methods=['GET'])
@verify_admin
def get_all_blogs_admin():
    try:
        docs = db.collection('blogs').order_by('created_at', direction=firestore.Query.DESCENDING).stream()
        blogs = [{"id": doc.id, **doc.to_dict()} for doc in docs]
        return jsonify(blogs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blogs_bp.route('/api/admin/blogs', methods=['POST'])
@verify_admin
def create_blog():
    try:
        data = request.json
        title = data.get('title')
        content = data.get('content')
        excerpt = data.get('excerpt')
        image = data.get('image')
        category = data.get('category')
        published = data.get('published', False)
        featured = data.get('featured', False)
        
        if not title or not content:
            return jsonify({"error": "Title and Content are required"}), 400
            
        slug = get_slug(title)
        
        # Check for duplicate slug
        existing = db.collection('blogs').where('slug', '==', slug).limit(1).stream()
        if next(existing, None):
            slug = f"{slug}-{int(firestore.datetime.datetime.now().timestamp())}"

        blog_data = {
            'title': title,
            'slug': slug,
            'content': content,
            'excerpt': excerpt,
            'image': image,
            'category': category,
            'published': published,
            'featured': featured,
            'views': 0,
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP
        }
        
        db.collection('blogs').add(blog_data)
        
        return jsonify({"message": "Blog created successfully", "slug": slug}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blogs_bp.route('/api/admin/blogs/<blog_id>', methods=['PUT'])
@verify_admin
def update_blog(blog_id):
    try:
        data = request.json
        
        update_data = {
            'updated_at': firestore.SERVER_TIMESTAMP
        }
        
        fields = ['title', 'content', 'excerpt', 'image', 'category', 'published', 'featured']
        for field in fields:
            if field in data:
                update_data[field] = data[field]
                
        if 'title' in data:
            # Optionally update slug, but usually better to keep it stable for SEO
            # update_data['slug'] = get_slug(data['title'])
            pass

        db.collection('blogs').document(blog_id).update(update_data)
        
        return jsonify({"message": "Blog updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blogs_bp.route('/api/admin/blogs/<blog_id>', methods=['DELETE'])
@verify_admin
def delete_blog(blog_id):
    try:
        db.collection('blogs').document(blog_id).delete()
        return jsonify({"message": "Blog deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blogs_bp.route('/api/admin/blog-categories', methods=['POST'])
@verify_admin
def create_category():
    try:
        data = request.json
        name = data.get('name')
        
        if not name:
            return jsonify({"error": "Name is required"}), 400
            
        slug = get_slug(name)
        
        db.collection('blog_categories').add({
            'name': name,
            'slug': slug
        })
        
        return jsonify({"message": "Category created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
