# 1. Project Title: 
🌊 Flood-Risk Detection System

## 2. Description / Overview
The **Flood-Risk Detection System** is an advanced full-stack platform designed to mitigate the impact of floods through real-time monitoring, predictive analytics, and proactive alerting. By integrating meteorological data with geographical information, the system provides a comprehensive "bird's-eye view" of flood risks across various water bodies (rivers and dams) in India, with a specific focus on areas like Pune.

The system serves two primary audiences:
- **Public Users**: Can monitor live risk maps, search for specific rivers/dams, and manage their profile to receive automated alerts.
- **Admins**: Have the power to manually update river metrics, broadcast emergency alerts via SMS/Email, and oversee system-wide statistics.

## 3. Features
- **1. Real-Time Risk Mapping**: An interactive map interface that visualizes flood risk levels (Low, Medium, High) using color-coded markers.
- **2. Predictive AI Analysis**: Uses a Random Forest ML model to predict flood probability based on rainfall, humidity, and water levels.
- **3. Multi-Channel Alerting**: Automated SMS notifications via **Twilio API** and Email alerts via **SMTP** when risk thresholds are exceeded.
- **4. Admin Control Center**: A dedicated panel for managing location data and broadcasting manual emergency messages.
- **5. Historical Data Visualization**: Charts and graphs showing historical flood trends for better urban planning and preparation.
- **6. Live Weather Integration**: Pulls real-time meteorological data using the **Open-Meteo API**.
- **7. User Profile Management**: Users can update their contact details to ensure they receive critical safety alerts.

## 4. Tech Stack
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

### **Machine Learning & Data**
- **Scikit-Learn**: Used to implement the **Random Forest Classifier** for risk prediction.
- **Joblib**: For model serialization and efficient loading.
- **NumPy & Pandas**: For data manipulation and preprocessing.

### **Database & Services**
- **MySQL (via XAMPP)**: The primary relational database for storing users, locations, and history.
- **Twilio API**: For sending real-time SMS alerts to mobile devices.
- **Open-Meteo API**: For fetching live weather metrics (Rainfall, Humidity) without requiring a private API key.
- **SMTP**: For reliable email delivery.

## 5. Future Scope
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

## 📊 Database Structure (MySQL)

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
- Install **XAMPP** and start the **MySQL** service.
- Create a database named `flood_risk`.
- Ensure your `backend/.env` has: `DATABASE_URL=mysql+pymysql://root:@localhost:3306/flood_risk` (Assuming no password).

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
- `ALERT_SIMULATION_MODE`: Set to `False` to send real SMS/Emails.
- `TWILIO_*`: Credentials for SMS alerts.
- `SMTP_*`: Credentials for Email alerts.

---

## 🚀 6. Deployment & Live Updates

### **How to Deploy**
1. **Frontend**: 
   - Build the project: `cd frontend && npm run build`.
   - Upload the `dist` folder to **Vercel**, **Netlify**, or **GitHub Pages**.
2. **Backend**:
   - Host on **Render**, **Railway**, or **AWS EC2**.
   - Use a production server like Gunicorn: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app`.
3. **Database**:
   - Move from local XAMPP to a cloud provider like **Aiven**, **PlanetScale**, or **AWS RDS**.

### **How to Update the Site Live**
The best way to update your site after deployment is using a **CI/CD Pipeline** (Continuous Integration/Continuous Deployment):
1. **Push to GitHub**: Every time you push a change to your GitHub repository, the hosting service (like Vercel or Render) will automatically detect it.
2. **Auto-Build**: The service will run `npm run build` (frontend) or restart the server (backend).
3. **Zero Downtime**: The new version goes live automatically in minutes without the site going offline.

---

## 🏁 Conclusion
This system is now production-ready, highly optimized, and includes professional features like real-time WebSocket monitoring and asynchronous background alerting.

#   f l o o d - r i s k - s y s t e m  
 