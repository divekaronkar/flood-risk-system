import { Navigate, Route, Routes } from 'react-router-dom'
import 'leaflet/dist/leaflet.css'
import './App.css'
import { Layout } from './components/Layout.jsx'
import { RequireAuth } from './components/RequireAuth.jsx'
import { LoginPage } from './pages/LoginPage.jsx'
import { RegisterPage } from './pages/RegisterPage.jsx'
import { DashboardPage } from './pages/DashboardPage.jsx'
import { RiskMapPage } from './pages/RiskMapPage.jsx'
import { AnalyticsPage } from './pages/AnalyticsPage.jsx'
import { AdminPage } from './pages/AdminPage.jsx'
import { ProfilePage } from './pages/ProfilePage.jsx'
import { LocationsPage } from './pages/LocationsPage.jsx'

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      <Route
        path="/"
        element={
          <RequireAuth>
            <Layout />
          </RequireAuth>
        }
      >
        <Route index element={<DashboardPage />} />
        <Route path="map" element={<RiskMapPage />} />
        <Route path="rivers" element={<LocationsPage />} />
        <Route path="analytics" element={<AnalyticsPage />} />
        <Route path="profile" element={<ProfilePage />} />
        <Route path="admin" element={<AdminPage />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
