import requests
import json
import random

BASE_URL = "http://127.0.0.1:5000/api/properties"

# Real-world locations in Mumbai
locations = [
    {"name": "Bandra West", "lat": 19.0596, "lng": 72.8295},
    {"name": "Andheri East", "lat": 19.1136, "lng": 72.8697},
    {"name": "Worli", "lat": 19.0178, "lng": 72.8185},
    {"name": "Powai", "lat": 19.1176, "lng": 72.9060},
    {"name": "BKC", "lat": 19.0674, "lng": 72.8680},
    {"name": "Juhu", "lat": 19.1075, "lng": 72.8263},
    {"name": "Colaba", "lat": 18.9067, "lng": 72.8147},
    {"name": "Malad West", "lat": 19.1828, "lng": 72.8402},
    {"name": "Thane West", "lat": 19.2183, "lng": 72.9781},
    {"name": "Navi Mumbai", "lat": 19.0330, "lng": 73.0297}
]

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
    "Modern Sea View Apartment",
    "Spacious Penthouse Suite",
    "Cozy Studio near Metro",
    "Premium Office Space",
    "Elegant Family Home",
    "Contemporary Urban Loft",
    "Beachfront Holiday Home",
    "Garden Facing Residence",
    "High-Rise Luxury Condo"
]

descriptions = [
    "Experience the epitome of luxury in this stunning property. Featuring state-of-the-art amenities and breathtaking views.",
    "Perfect for modern living, this property offers spacious interiors, premium finishes, and a prime location.",
    "A masterpiece of design and comfort. Enjoy world-class facilities including a gym, pool, and 24/7 security.",
    "Ideally located near major business hubs and entertainment centers. This property is perfect for professionals and families alike.",
    "Step into a world of elegance. This home features high ceilings, large windows, and a beautiful private garden."
]

properties = []

for i in range(12):
    loc = locations[i % len(locations)]
    imgs = image_sets[i % len(image_sets)]
    title = titles[i % len(titles)]
    desc = descriptions[i % len(descriptions)]
    
    price_val = random.randint(50, 2000) * 100000
    price_formatted = f"{price_val:,}"
    
    prop = {
        "title": f"{title} in {loc['name']}",
        "location": f"{loc['name']}, Mumbai",
        "price": price_formatted,
        "bedrooms": random.randint(1, 5),
        "bathrooms": random.randint(1, 6),
        "area": random.randint(500, 5000),
        "type": random.choice(["For Sale", "For Rent"]),
        "description": desc,
        "imageUrl": imgs[0],
        "images": imgs,
        "coordinates": {"lat": loc["lat"], "lng": loc["lng"]}
    }
    properties.append(prop)

print(f"Seeding {len(properties)} properties...")

for prop in properties:
    try:
        response = requests.post(BASE_URL, json=prop)
        if response.status_code == 201:
            print(f"Created: {prop['title']}")
        else:
            print(f"Failed to create {prop['title']}: {response.text}")
    except Exception as e:
        print(f"Error creating {prop['title']}: {e}")
