# Krishna Properties - Real Estate Platform

A modern, full-stack real estate application built with **SvelteKit** (Frontend) and **Flask** (Backend), powered by **Firebase** for data and authentication.

## 🚀 Features

- **Property Listings**: Browse properties with details like price, location, bedrooms, and amenities.
- **Interactive Maps**: View property locations on an interactive map (Leaflet/OpenStreetMap).
- **Admin Dashboard**: Secure admin interface to add and manage property listings.
- **User Authentication**: Sign up and login functionality using Firebase Auth.
- **Responsive Design**: Beautiful, mobile-first UI built with TailwindCSS and Shadcn-Svelte.
- **Image Carousel**: View multiple images for each property.

## 🛠️ Tech Stack

### Frontend
- **Framework**: SvelteKit (Svelte 5)
- **Styling**: TailwindCSS, Shadcn-Svelte
- **Maps**: Leaflet.js
- **State Management**: Svelte Stores
- **Build Tool**: Vite

### Backend
- **Framework**: Flask (Python)
- **Database**: Firebase Firestore
- **Storage**: Firebase Storage
- **Authentication**: Firebase Auth

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- **Node.js** (v18 or higher)
- **Python** (v3.10 or higher)
- **Git**

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/arzvaak/KrishnaProperties.git
cd KrishnaProperties
```

### 2. Backend Setup
The backend is a Flask application that serves the API.

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```

2.  Create a virtual environment:
    ```bash
    python -m venv venv
    ```

3.  Activate the virtual environment:
    - **Windows**:
        ```bash
        venv\Scripts\activate
        ```
    - **macOS/Linux**:
        ```bash
        source venv/bin/activate
        ```

4.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure Firebase Credentials**:
    - Go to your [Firebase Console](https://console.firebase.google.com/).
    - Navigate to **Project Settings** > **Service accounts**.
    - Click **Generate new private key**.
    - Save the downloaded JSON file as `serviceAccountKey.json` inside the `backend/` directory.
    - **Note**: This file is sensitive and is ignored by git. DO NOT commit it.

6.  (Optional) Seed Database:
    If you want to populate the database with dummy data:
    ```bash
    python seed_data.py
    ```

7.  Run the backend server:
    ```bash
    python app.py
    ```
    The server will start at `http://localhost:5000`.

### 3. Frontend Setup
The frontend is a SvelteKit application.

1.  Open a new terminal and navigate to the frontend directory:
    ```bash
    cd frontend
    ```

2.  Install dependencies:
    ```bash
    npm install
    ```

3.  **Configure Environment Variables**:
    - Create a file named `.env` in the `frontend/` directory.
    - Add your Firebase configuration keys (found in Firebase Console > Project Settings > General > Your apps > SDK setup and configuration > Config).
    
    **Example `.env` file:**
    ```env
    VITE_FIREBASE_API_KEY=your_api_key
    VITE_FIREBASE_AUTH_DOMAIN=your_project_id.firebaseapp.com
    VITE_FIREBASE_PROJECT_ID=your_project_id
    VITE_FIREBASE_STORAGE_BUCKET=your_project_id.appspot.com
    VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
    VITE_FIREBASE_APP_ID=your_app_id
    ```
    - **Note**: This file is ignored by git. DO NOT commit it.

4.  Run the development server:
    ```bash
    npm run dev
    ```
    The app will be available at `http://localhost:5173`.

## 📂 Project Structure

```
KrishnaProperties/
├── backend/                # Flask Backend
│   ├── routes/             # API Routes (properties, users)
│   ├── app.py              # Main application entry point
│   ├── firebase_config.py  # Firebase initialization logic
│   ├── seed_data.py        # Script to seed dummy data
│   ├── requirements.txt    # Python dependencies
│   └── serviceAccountKey.json # (Ignored) Firebase Admin SDK key
│
├── frontend/               # SvelteKit Frontend
│   ├── src/
│   │   ├── lib/            # Shared components and utilities
│   │   │   ├── components/ # UI Components (Map, Navbar, etc.)
│   │   │   └── firebase.js # Firebase client initialization
│   │   └── routes/         # Application pages (File-based routing)
│   ├── static/             # Static assets
│   ├── .env                # (Ignored) Environment variables
│   └── package.json        # Node.js dependencies
│
├── .gitignore              # Root gitignore
└── README.md               # Project documentation
```

## 🔧 Troubleshooting

- **CORS Errors**: Ensure the backend is running and `flask-cors` is installed and configured in `app.py`.
- **Firebase Errors**:
    - **Backend**: Ensure `serviceAccountKey.json` is present in `backend/` and has correct permissions.
    - **Frontend**: Ensure `.env` file exists in `frontend/` and contains valid keys. Restart the Vite server after changing `.env`.
- **Map Not Loading**: Ensure you have an internet connection as Leaflet loads tiles from OpenStreetMap.

## 🛡️ Security Note

This repository is configured to exclude sensitive files (`.env`, `serviceAccountKey.json`) from version control. **Never force push these files to GitHub.**

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
