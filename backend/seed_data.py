import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/properties"

properties = [
    {
        "title": "Luxury Villa in Bandra",
        "location": "Bandra West, Mumbai",
        "price": "12,50,00,000",
        "bedrooms": 4,
        "bathrooms": 5,
        "area": 3500,
        "type": "For Sale",
        "description": "Experience the epitome of luxury in this stunning 4BHK villa located in the heart of Bandra. Featuring a private pool, terrace garden, and state-of-the-art amenities.",
        "imageUrl": "https://images.unsplash.com/photo-1613490493576-7fde63acd811?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "images": [
            "https://images.unsplash.com/photo-1613490493576-7fde63acd811?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1580587771525-78b9dba3b91d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80"
        ],
        "coordinates": {"lat": 19.0596, "lng": 72.8295}
    },
    {
        "title": "Modern Apartment in Andheri",
        "location": "Andheri East, Mumbai",
        "price": "2,50,00,000",
        "bedrooms": 2,
        "bathrooms": 2,
        "area": 1200,
        "type": "For Sale",
        "description": "Spacious 2BHK apartment with city views. Close to metro station and airport.",
        "imageUrl": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "images": [
            "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1484154218962-a1c002085d2f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80"
        ],
        "coordinates": {"lat": 19.1136, "lng": 72.8697}
    },
    {
        "title": "Sea View Penthouse",
        "location": "Worli, Mumbai",
        "price": "45,00,00,000",
        "bedrooms": 5,
        "bathrooms": 6,
        "area": 6000,
        "type": "For Sale",
        "description": "Ultra-luxury penthouse with panoramic sea views. Private elevator, concierge service, and world-class amenities.",
        "imageUrl": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "images": [
            "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80"
        ],
        "coordinates": {"lat": 19.0178, "lng": 72.8185}
    },
    {
        "title": "Cozy Studio in Powai",
        "location": "Powai, Mumbai",
        "price": "85,00,000",
        "bedrooms": 1,
        "bathrooms": 1,
        "area": 450,
        "type": "For Rent",
        "description": "Perfect for singles or couples. Fully furnished studio apartment in Hiranandani Gardens.",
        "imageUrl": "https://images.unsplash.com/photo-1554995207-c18c203602cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "images": [
            "https://images.unsplash.com/photo-1554995207-c18c203602cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80"
        ],
        "coordinates": {"lat": 19.1176, "lng": 72.9060}
    },
    {
        "title": "Commercial Office Space",
        "location": "BKC, Mumbai",
        "price": "15,00,00,000",
        "bedrooms": 0,
        "bathrooms": 2,
        "area": 2500,
        "type": "For Sale",
        "description": "Premium office space in Bandra Kurla Complex. Grade A building with ample parking.",
        "imageUrl": "https://images.unsplash.com/photo-1497366216548-37526070297c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
        "images": [
            "https://images.unsplash.com/photo-1497366216548-37526070297c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1497366811353-6870744d04b2?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80"
        ],
        "coordinates": {"lat": 19.0674, "lng": 72.8680}
    }
]

for prop in properties:
    try:
        response = requests.post(BASE_URL, json=prop)
        if response.status_code == 201:
            print(f"Created: {prop['title']}")
        else:
            print(f"Failed to create {prop['title']}: {response.text}")
    except Exception as e:
        print(f"Error creating {prop['title']}: {e}")
