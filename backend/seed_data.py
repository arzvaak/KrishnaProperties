import json
import random
from datetime import datetime

# Specific Address requested by user
SPECIFIC_ADDRESS = "Sec 16B, Greater Noida West"
SPECIFIC_COORDS = {"lat": 28.5961, "lng": 77.4583} # Approx coords for Greater Noida West

# High-quality real estate images from Unsplash
image_sets = [
    [
        "https://images.unsplash.com/photo-1613490493576-7fde63acd811?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1580587771525-78b9dba3b91d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80"
    ],
    [
        "https://images.unsplash.com/photo-1600596542815-27b88e35eabd?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80"
    ],
    [
        "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80"
    ],
    [
        "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1600566752355-35792bedcfe1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1600585154526-990dced4db0d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80"
    ],
    [
        "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1484154218962-a1c002085d2f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1556912172-45b7abe8b7e1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80"
    ],
    [
        "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1560185127-6ed189bf02f4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80"
    ],
    [
        "https://images.unsplash.com/photo-1554995207-c18c203602cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1505691938895-1758d7feb511?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80"
    ],
    [
        "https://images.unsplash.com/photo-1497366216548-37526070297c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1497366811353-6870744d04b2?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1524758631624-e2822e304c36?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80"
    ]
]

titles = [
    "Luxury Villa with Private Pool",
    "Modern Apartment with Park View",
    "Spacious Penthouse Suite",
    "Cozy Studio near Market",
    "Premium Commercial Space",
    "Elegant Family Home",
    "Contemporary Urban Loft",
    "Corner Plot for Sale",
    "Garden Facing Residence",
    "Industrial Plot in Prime Location"
]

descriptions = [
    "Experience the epitome of luxury in this stunning property. Featuring state-of-the-art amenities and breathtaking views.",
    "Perfect for modern living, this property offers spacious interiors, premium finishes, and a prime location.",
    "A masterpiece of design and comfort. Enjoy world-class facilities including a gym, pool, and 24/7 security.",
    "Ideally located near major business hubs and entertainment centers. This property is perfect for professionals and families alike.",
    "Step into a world of elegance. This home features high ceilings, large windows, and a beautiful private garden."
]

property_types = [
    "Authority plots", 
    "Free Hold plots", 
    "Commercial Plots", 
    "Industrial or Factory Plots", 
    "Villa's"
]

def seed_properties(db):
    print("Seeding properties...")
    properties = []
    
    for i in range(15):
        imgs = image_sets[i % len(image_sets)]
        title = titles[i % len(titles)]
        desc = descriptions[i % len(descriptions)]
        prop_type = property_types[i % len(property_types)]
        
        price_val = random.randint(50, 2000) * 100000
        price_formatted = f"{price_val:,}"
        
        prop = {
            "title": f"{title}",
            "location": SPECIFIC_ADDRESS,
            "price": price_formatted,
            "bedrooms": random.randint(1, 5),
            "bathrooms": random.randint(1, 6),
            "area": random.randint(500, 5000),
            "type": prop_type,
            "description": desc,
            "imageUrl": imgs[0],
            "images": imgs,
            "coordinates": SPECIFIC_COORDS,
            "createdAt": firestore.SERVER_TIMESTAMP,
            "status": "available"
        }
        properties.append(prop)

    for prop in properties:
        try:
            db.collection('properties').add(prop)
            print(f"Created Property: {prop['title']}")
        except Exception as e:
            print(f"Error creating property {prop['title']}: {e}")

def seed_blogs(db):
    print("\nSeeding blogs...")
    # Import slugify
    try:
        from slugify import slugify
    except ImportError:
        # Fallback if python-slugify not installed in this env, though it should be
        def slugify(text):
            return text.lower().replace(' ', '-')

    blog_titles = [
        "Top 5 Investment Tips for Greater Noida West",
        "Why Sec 16B is the Next Big Thing",
        "Interior Design Trends for 2025",
        "Understanding Property Taxes in India",
        "The Benefits of Living in a Gated Community"
    ]
    
    blog_contents = [
        "Investing in real estate is a journey. Here are the top 5 tips to make sure you get the best ROI...",
        "Sec 16B in Greater Noida West is witnessing rapid infrastructure development...",
        "Minimalism is out, maximalism is in! Discover the vibrant trends taking over homes this year...",
        "Navigating the complex world of property taxes can be daunting. We break it down for you...",
        "Safety, community, and amenities. Explore why gated communities are the preferred choice for families..."
    ]
    
    blog_images = [
        "https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80"
    ]

    for i in range(5):
        title = blog_titles[i]
        slug = slugify(title)
        
        blog = {
            "title": title,
            "slug": slug,
            "excerpt": blog_contents[i][:100] + "...",
            "content": blog_contents[i] * 5, # Make it longer
            "image": blog_images[i], # Changed from imageUrl to image
            "author": "Krishna Properties Team",
            "createdAt": firestore.SERVER_TIMESTAMP,
            "created_at": firestore.SERVER_TIMESTAMP, # Add snake_case for consistency with backend
            "tags": ["Real Estate", "Tips", "Greater Noida"],
            "published": True, # CRITICAL: Must be true to show up
            "views": random.randint(10, 500)
        }
        
        try:
            # Check if exists to avoid duplicates (optional but good)
            existing = db.collection('blogs').where('slug', '==', slug).limit(1).stream()
            if not next(existing, None):
                db.collection('blogs').add(blog)
                print(f"Created Blog: {blog['title']}")
            else:
                print(f"Skipped (Exists): {blog['title']}")
        except Exception as e:
            print(f"Error creating blog {blog['title']}: {e}")

from firebase_config import initialize_firebase
from firebase_admin import firestore

if __name__ == "__main__":
    # Initialize Firebase
    db, _ = initialize_firebase()
    
    seed_properties(db)
    seed_blogs(db)
