import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/properties"

def fix_listing():
    # 1. Find the broken listing
    try:
        response = requests.get(BASE_URL, params={"search": "Modern Sea View Apartment in Andheri East", "limit": 100})
        data = response.json()
        properties = data.get("properties", [])
        
        target_id = None
        for prop in properties:
            if "Modern Sea View Apartment in Andheri East" in prop["title"]:
                target_id = prop["id"]
                break
        
        if target_id:
            print(f"Found broken listing with ID: {target_id}")
            # 2. Delete it
            del_res = requests.delete(f"{BASE_URL}/{target_id}")
            if del_res.status_code == 200:
                print("Deleted broken listing.")
            else:
                print(f"Failed to delete: {del_res.text}")
        else:
            print("Listing not found, skipping delete.")

        # 3. Add replacement
        new_prop = {
            "title": "Stunning Sea View Apartment in Andheri East",
            "location": "Andheri East, Mumbai",
            "price": "3,50,00,000",
            "bedrooms": 3,
            "bathrooms": 3,
            "area": 1800,
            "type": "For Sale",
            "description": "A beautifully designed apartment with panoramic sea views. Features modern amenities, spacious rooms, and excellent connectivity.",
            "imageUrl": "https://images.unsplash.com/photo-1493809842364-78817add7ffb?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
            "images": [
                "https://images.unsplash.com/photo-1493809842364-78817add7ffb?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
                "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
                "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80"
            ],
            "coordinates": {"lat": 19.1136, "lng": 72.8697}
        }
        
        create_res = requests.post(BASE_URL, json=new_prop)
        if create_res.status_code == 201:
            print("Created replacement listing.")
        else:
            print(f"Failed to create replacement: {create_res.text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_listing()
