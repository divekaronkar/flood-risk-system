# 🌊 Flood-Risk Detection System

## Description / Overview
The **Flood-Risk Detection System** is an advanced full-stack platform designed to mitigate the impact of floods through real-time monitoring, predictive analytics, and proactive alerting. By integrating meteorological data with geographical information, the system provides a comprehensive "bird's-eye view" of flood risks across various water bodies (rivers and dams) in India, with a specific focus on areas like Pune.

The system serves two primary audiences:
- **Public Users**: Can monitor live risk maps, search for specific rivers/dams, and manage their profile to receive automated alerts.
- **Admins**: Have the power to manually update river metrics, broadcast emergency alerts via SMS/Email, and oversee system-wide statistics.

## Features
- **1. Real-Time Risk Mapping**: An interactive map interface that visualizes flood risk levels (Low, Medium, High) using color-coded markers.
- **2. Predictive AI Analysis**: Uses a Random Forest ML model to predict flood probability based on rainfall, humidity, and water levels.
- **3. Multi-Channel Alerting**: Automated SMS notifications via **Twilio API** and Email alerts via **Brevo (free, no domain needed)** when risk thresholds are exceeded.
- **4. Admin Control Center**: A dedicated panel for managing location data and broadcasting manual emergency messages.
- **5. Historical Data Visualization**: Charts and graphs showing historical flood trends for better urban planning and preparation.
- **6. Live Weather Integration**: Pulls real-time meteorological data using the **Open-Meteo API**.
- **7. User Profile Management**: Users can update their contact details to ensure they receive critical safety alerts.

## Tech Stack
The project is built using a modern, scalable tech stack:

### **Frontend**
- **React.js (Vite)**: For a fast, responsive, and dynamic User Interface.
- **Leaflet.js**: The mapping engine used to render the interactive risk map.
- **Lucide React**: For a consistent and modern iconography system.
- **CSS3 (Custom)**: A dark-themed, high-contrast UI designed for clarity during emergency monitoring.

### **Backend**
- **FastAPI (Python)**: A high-performance web framework for building the RESTful API and WebSocket connections.
- **SQLAlchemy**: ORM for database management and type-safe queries.
- **Pydantic**: For strict data validation and schema management.
- **JWT (JSON Web Tokens)**: For secure, stateless user authentication and role-based access control.
- **Gunicorn**: Production WSGI server for serving the FastAPI app.

### **Machine Learning & Data**
- **Scikit-Learn**: Used to implement the **Random Forest Classifier** for risk prediction.
- **Joblib**: For model serialization and efficient loading.
- **NumPy & Pandas**: For data manipulation and preprocessing.

### **Database & Services**
- **Neon (Free PostgreSQL)**: Cloud database for production.
- **MySQL (local, XAMPP)**: For local development.
- **Brevo API**: For free email alerts without needing a custom domain.
- **Open-Meteo API**: For fetching live weather metrics (Rainfall, Humidity) without requiring a private API key.

## Future Scope
- **1. Satellite Imagery Integration**: Incorporating real-time satellite data for even more accurate flood boundary detection.
- **2. Mobile Application**: Developing native Android/iOS apps with push notifications for instant user reach.
- **3. Crowdsourced Reporting**: Allowing users to report localized flooding or water logging directly through the app.
- **4. AI Chatbot Support**: An AI-driven assistant to provide immediate safety instructions and evacuation routes during emergencies.
- **5. IoT Sensor Integration**: Connecting physical water level sensors directly to the API for 100% automated data collection.
- **6. Predictive Evacuation Routing**: Using GIS data to suggest the safest routes to high-ground during a flood event.

---

## 🏗️ Project Structure

```text
flood-risk-system/
├── backend/                # FastAPI Application
│   ├── app/
│   │   ├── api/           # Endpoints & Routes
│   │   ├── core/          # Config & Security
│   │   ├── db/            # Database Session & Base
│   │   ├── ml/            # ML Model & Prediction Logic
│   │   ├── models/        # SQLAlchemy Database Models
│   │   ├── schemas/       # Pydantic Data Schemas
│   │   └── services/      # Business Logic (Alerts)
│   ├── scripts/           # DB Init, Seeding, & Training
│   └── .env               # Environment Variables
└── frontend/               # React (Vite) Application
    ├── src/
    │   ├── components/    # Reusable UI Components
    │   ├── lib/           # API & Auth Utilities
    │   └── pages/         # Application Views
    └── index.html
```

---

## 📊 Database Structure

The system uses three primary tables:

1.  **`users`**: Stores user credentials, contact info (phone/email), and roles (`admin`, `user`).
2.  **`risk_locations`**: Stores geographical data (lat/lng), current weather/water metrics, and calculated risk percentages for rivers and dams.
3.  **`historical_flood_records`**: Stores historical data for analytics and trend visualization.

---

## 🤖 ML Algorithm

The risk assessment is powered by a **Random Forest Classifier** trained on historical environmental data.
- **Input Features**: Rainfall (mm), Humidity (%), River Level (m), Drainage Capacity (%).
- **Output**: Probability percentage (0-100%) and Risk Level (Low, Medium, High).
- **Fallback**: Includes a robust heuristic fallback mechanism to ensure the system remains functional even if the ML model file is unavailable.

---

## 🔗 API Endpoints

| Category | Endpoint | Method | Description |
| :--- | :--- | :--- | :--- |
| **Auth** | `/auth/register` | POST | Create new account |
| | `/auth/login` | POST | Get JWT token and user details |
| | `/auth/me` | GET | Get current authenticated profile |
| **Locations**| `/locations` | GET | List all rivers and dams |
| | `/locations/{id}` | PATCH | (Admin) Update metrics for a location |
| | `/locations/broadcast-alert` | POST | (Admin) Send manual SMS/Email to all |
| **Users** | `/users` | GET | (Admin) List all registered users |
| | `/users/me` | PATCH | Update own profile (name/phone) |
| **Stats** | `/stats/dashboard` | GET | Overview counts for the dashboard |
| **Real-time**| `/ws` | WS | WebSocket for live risk updates |

---

## 🛠️ Local Setup & Run

### 1. Database Setup
- **Local MySQL (XAMPP)**:
  - Install **XAMPP** and start the **MySQL** service.
  - Create a database named `flood_risk`.
  - Ensure your `backend/.env` has: `DATABASE_URL=mysql+pymysql://root:@localhost:3306/flood_risk` (Assuming no password).
- **Neon (Production)**: See "Neon Database Setup" below.

### 2. Backend Setup
```bash
cd backend
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database, train model, and seed data
python scripts/init_db.py
python scripts/train_model.py
python scripts/seed_data.py

# Run the server
uvicorn app.main:app --reload --app-dir backend
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🛠️ Configuration (.env)
Key settings in `backend/.env`:
- `DATABASE_URL`: Connection string for MySQL (local) or Neon PostgreSQL (production).
- `JWT_SECRET_KEY`: Random secure string for token signing.
- `ALERT_SIMULATION_MODE`: Set to `False` to send real SMS/Emails.
- `BREVO_API_KEY` & `BREVO_FROM_EMAIL`: For free email alerts.
- `TWILIO_*`: Credentials for SMS alerts.

---

## 🚀 Deployment & Live Updates

### **How to Deploy**
1. **Frontend (Vercel)**: 
   - Push your code to GitHub.
   - Connect your repo to Vercel, set `Root Directory` to `frontend`.
   - Add environment variable `VITE_API_URL` to your Render backend URL.

2. **Backend (Render)**:
   - Push your code to GitHub.
   - Create a new **Web Service** on Render, set `Root Directory` to `backend`.
   - Set **Build Command** to `pip install -r requirements.txt`.
   - Set **Start Command** to `gunicorn -w 1 -k uvicorn.workers.UvicornWorker app.main:app`.
   - Add **Environment Variables** (DATABASE_URL, JWT_SECRET_KEY, etc.).

3. **Database (Neon - Free Tier)**:
   - Sign up for free at [Neon.tech](https://neon.tech).
   - Create a new project and copy your PostgreSQL connection string.
   - Add this connection string as `DATABASE_URL` in your Render backend environment variables.

### **How to Update the Site Live**
The best way to update your site after deployment is using a **CI/CD Pipeline**:
1. **Push to GitHub**: Every time you push a change to your GitHub repository, Render and Vercel will automatically detect it.
2. **Auto-Build**: Vercel will run `npm run build` (frontend) and Render will restart your backend server.
3. **Zero Downtime**: The new version goes live automatically in minutes without the site going offline.

---

## 📧 Brevo Email Setup (Free, No Domain Needed)
1. Sign up for a free account at [Brevo.com](https://www.brevo.com).
2. Go to **SMTP & API** → **Create a new API key**.
3. Add your Gmail (or any email) as a verified sender (Brevo will send a confirmation email).
4. Add your API key and sender email to `BREVO_API_KEY` and `BREVO_FROM_EMAIL` in your `.env` file.

---

## 🗄️ Neon Database Setup (Free Tier)
1. Sign up for free at [Neon.tech](https://neon.tech).
2. Create a new project (choose a region closest to you).
3. Copy the PostgreSQL connection string Neon provides you.
4. Add this connection string as `DATABASE_URL` in your Render backend environment variables.
5. Initialize your database by running `python scripts/init_db.py`, `python scripts/train_model.py`, and `python scripts/seed_data.py` (either locally with Neon connection string or via Render's shell).

---

## 🏁 Conclusion
This system is now production-ready, highly optimized, and includes professional features like real-time WebSocket monitoring and asynchronous background alerting.
