import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/properties"

def replace_listing():
    # 1. Find the listing to delete
    try:
        response = requests.get(BASE_URL, params={"search": "High-rise luxury condo in Navi Mumbai", "limit": 100})
        data = response.json()
        properties = data.get("properties", [])
        
        target_id = None
        for prop in properties:
            if "High-rise luxury condo in Navi Mumbai" in prop["title"]:
                target_id = prop["id"]
                break
        
        if target_id:
            print(f"Found listing to delete with ID: {target_id}")
            # 2. Delete it
            del_res = requests.delete(f"{BASE_URL}/{target_id}")
            if del_res.status_code == 200:
                print("Deleted listing.")
            else:
                print(f"Failed to delete: {del_res.text}")
        else:
            print("Listing not found, skipping delete.")

        # 3. Add replacement
        new_prop = {
            "title": "Premium Apartment in Navi Mumbai",
            "location": "Vashi, Navi Mumbai",
            "price": "1,85,00,000",
            "bedrooms": 2,
            "bathrooms": 2,
            "area": 1100,
            "type": "For Sale",
            "description": "A modern apartment in a prime location. Close to station and malls.",
            "imageUrl": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
            "images": [
                "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
                "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
                "https://images.unsplash.com/photo-1484154218962-a1c002085d2f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80"
            ],
            "coordinates": {"lat": 19.0330, "lng": 73.0297}
        }
        
        create_res = requests.post(BASE_URL, json=new_prop)
        if create_res.status_code == 201:
            print("Created replacement listing.")
        else:
            print(f"Failed to create replacement: {create_res.text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    replace_listing()
