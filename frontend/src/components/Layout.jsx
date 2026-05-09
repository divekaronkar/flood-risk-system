import { useEffect, useState } from 'react'
import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { clearToken, getUser } from '../lib/auth.js'

export function Layout() {
  const navigate = useNavigate()
  const user = getUser()
  const isAdmin = user?.is_admin || user?.role === 'admin'
  const [highRiskLocations, setHighRiskLocations] = useState([])

  useEffect(() => {
    const ws = new WebSocket('ws://127.0.0.1:8000/api/ws')
    ws.onmessage = (evt) => {
      try {
        const msg = JSON.parse(evt.data)
        if (msg.type === 'locations_update' && Array.isArray(msg.locations)) {
          const high = msg.locations.filter((l) => l.risk_level === 'High')
          setHighRiskLocations(high)
        }
      } catch {
        // ignore
      }
    }
    return () => ws.close()
  }, [])

  function logout() {
    clearToken()
    navigate('/login')
  }

  return (
    <div className="appShell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brandIcon" />
          <div>
            <h1>Flood-Risk System</h1>
            <p>Detection + Analytics</p>
          </div>
        </div>

        <nav className="nav" aria-label="Primary">
          <NavLink end to="/">
            Dashboard
          </NavLink>
          <NavLink to="/map">Risk Map</NavLink>
          <NavLink to="/rivers">Rivers & Dams</NavLink>
          <NavLink to="/analytics">Historical Analytics</NavLink>
          <NavLink to="/profile">My Profile</NavLink>
          {isAdmin && <NavLink to="/admin">Admin Panel</NavLink>}
        </nav>

        <div style={{ marginTop: 14, display: 'grid', gap: 10 }}>
          <button className="btn secondary" onClick={logout} type="button">
            Logout
          </button>
          {!user && (
            <div className="muted">
              Tip: The first registered user becomes <b>Admin</b>.
            </div>
          )}
        </div>
      </aside>

      <main className="content">
        <div className="container">
          {highRiskLocations.length > 0 && (
            <div className="emergencyBanner">
              <span>
                ⚠️ EMERGENCY: High flood risk detected at {highRiskLocations.map(l => l.name).join(', ')}!
              </span>
              <button className="btn" onClick={() => navigate('/map')} style={{ padding: '4px 12px', background: 'white', color: 'var(--red)' }}>
                View Map
              </button>
            </div>
          )}
          <Outlet />
        </div>
      </main>
    </div>
  )
}

