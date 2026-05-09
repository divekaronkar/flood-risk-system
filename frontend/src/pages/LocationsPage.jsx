import { useEffect, useState, useMemo } from 'react'
import { api } from '../lib/api.js'

function badgeDot(level) {
  return <span className={`dot ${String(level || 'low').toLowerCase()}`} />
}

export function LocationsPage() {
  const [locations, setLocations] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')

  useEffect(() => {
    async function load() {
      try {
        const res = await api.get('/locations')
        setLocations(res.data)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const filtered = useMemo(() => {
    const q = search.toLowerCase()
    return locations.filter(l => 
      l.name.toLowerCase().includes(q) || 
      (l.is_dam ? 'dam' : 'river').includes(q)
    )
  }, [locations, search])

  return (
    <>
      <div className="topbar">
        <div>
          <h1 className="pageTitle">Rivers & Dams</h1>
          <p className="subtitle">Detailed list of all monitored water bodies across India.</p>
        </div>
      </div>

      <div className="card panel">
        <div style={{ marginBottom: 20 }}>
          <input
            className="input"
            placeholder="Search by name or type (e.g. Pune, Dam, Ganga)..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        {loading ? (
          <div className="muted">Loading locations...</div>
        ) : (
          <div className="tableWrap">
            <table className="table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Type</th>
                  <th>Risk Level</th>
                  <th>Water Level</th>
                  <th>Rainfall</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map(l => (
                  <tr key={l.id}>
                    <td style={{ color: 'var(--heading)', fontWeight: 700 }}>{l.name}</td>
                    <td>
                      <span className="badge">
                        {l.is_dam ? '🏢 Dam' : '🌊 River'}
                      </span>
                    </td>
                    <td>
                      <span className="badge">
                        {badgeDot(l.risk_level)}
                        {l.risk_level} ({l.risk_percent.toFixed(1)}%)
                      </span>
                    </td>
                    <td>{l.river_level_m}m</td>
                    <td>{l.rainfall_mm}mm</td>
                  </tr>
                ))}
              </tbody>
            </table>
            {filtered.length === 0 && <div className="muted" style={{ padding: 20, textAlign: 'center' }}>No results found.</div>}
          </div>
        )}
      </div>
    </>
  )
}
