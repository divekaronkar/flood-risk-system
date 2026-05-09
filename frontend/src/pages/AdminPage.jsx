import { useEffect, useMemo, useState } from 'react'
import { api } from '../lib/api.js'

function badgeDot(level) {
  return <span className={`dot ${String(level || 'low').toLowerCase()}`} />
}

export function AdminPage() {
  const [rows, setRows] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [broadcastMsg, setBroadcastMsg] = useState('')
  const [broadcastLoading, setBroadcastLoading] = useState(false)

  const [selectedId, setSelectedId] = useState('')
  const selected = useMemo(() => rows.find((r) => String(r.id) === String(selectedId)), [rows, selectedId])

  const [form, setForm] = useState({
    rainfall_mm: '',
    humidity: '',
    river_level_m: '',
    drainage_capacity: '',
  })

  useEffect(() => {
    let mounted = true
    async function load() {
      setLoading(true)
      setError(null)
      try {
        const res = await api.get('/locations')
        if (mounted) setRows(res.data)
      } catch (err) {
        if (mounted) setError(err?.response?.data?.detail || 'Failed to load locations')
      } finally {
        if (mounted) setLoading(false)
      }
    }
    load()
    return () => {
      mounted = false
    }
  }, [])

  useEffect(() => {
    if (!selected) return
    setForm({
      rainfall_mm: String(selected.rainfall_mm ?? ''),
      humidity: String(selected.humidity ?? ''),
      river_level_m: String(selected.river_level_m ?? ''),
      drainage_capacity: String(selected.drainage_capacity ?? ''),
    })
  }, [selected])

  async function save() {
    if (!selected) return
    setError(null)
    try {
      const res = await api.patch(`/locations/${selected.id}`, {
        rainfall_mm: Number(form.rainfall_mm),
        humidity: Number(form.humidity),
        river_level_m: Number(form.river_level_m),
        drainage_capacity: Number(form.drainage_capacity),
      })

      setRows((prev) => prev.map((p) => (p.id === res.data.id ? res.data : p)))
    } catch (err) {
      setError(err?.response?.data?.detail || 'Update failed (requires admin)')
    }
  }

  async function broadcastAlert() {
    if (!broadcastMsg) return
    setBroadcastLoading(true)
    setError(null)
    try {
      await api.post('/locations/broadcast-alert', { message: broadcastMsg })
      setBroadcastMsg('')
      alert('Alert broadcasted successfully!')
    } catch (err) {
      setError(err?.response?.data?.detail || 'Broadcast failed')
    } finally {
      setBroadcastLoading(false)
    }
  }

  function exportToCSV() {
    if (!rows.length) return
    const headers = ['ID', 'Name', 'Risk Level', 'Risk %', 'Rainfall (mm)', 'River Level (m)', 'Drainage Capacity (%)']
    const csvRows = [
      headers.join(','),
      ...rows.map((r) =>
        [
          r.id,
          `"${r.name}"`,
          r.risk_level,
          r.risk_percent.toFixed(1),
          r.rainfall_mm,
          r.river_level_m,
          r.drainage_capacity,
        ].join(',')
      ),
    ]

    const blob = new Blob([csvRows.join('\n')], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.setAttribute('hidden', '')
    a.setAttribute('href', url)
    a.setAttribute('download', 'flood_risk_data.csv')
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
  }

  return (
    <>
      <div className="topbar">
        <div>
          <h1 className="pageTitle">Admin Panel</h1>
          <p className="subtitle">Update water level / drainage data and watch risk change.</p>
        </div>
        <button className="btn secondary" onClick={exportToCSV} disabled={loading || !rows.length}>
          Export to CSV
        </button>
      </div>

      <div className="twoCol">
        <div className="card panel">
          <h2>Locations</h2>
          {loading ? (
            <div className="muted">Loading…</div>
          ) : (
            <table className="table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Risk</th>
                  <th>%</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((r) => (
                  <tr
                    key={r.id}
                    onClick={() => setSelectedId(String(r.id))}
                    style={{
                      cursor: 'pointer',
                      background:
                        String(r.id) === String(selectedId) ? 'rgba(124,58,237,0.12)' : 'transparent',
                    }}
                  >
                    <td style={{ color: 'var(--heading)', fontWeight: 700 }}>{r.name}</td>
                    <td>
                      <span className="badge">
                        {badgeDot(r.risk_level)}
                        {r.risk_level}
                      </span>
                    </td>
                    <td>{Number(r.risk_percent || 0).toFixed(1)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
          {error ? (
            <div className="badge" style={{ marginTop: 10, borderColor: 'rgba(239,68,68,.5)' }}>
              {error}
            </div>
          ) : null}
        </div>

        <div className="card panel">
          <h2>Edit location</h2>
          {!selected ? (
            <div className="muted">Select a location from the list.</div>
          ) : (
            <>
              <div className="muted" style={{ marginBottom: 10 }}>
                Editing <b style={{ color: 'var(--heading)' }}>{selected.name}</b>
              </div>
              <div className="formGrid">
                <div>
                  <div className="muted">Rainfall (mm)</div>
                  <input
                    className="input"
                    type="number"
                    value={form.rainfall_mm}
                    onChange={(e) => setForm((f) => ({ ...f, rainfall_mm: e.target.value }))}
                  />
                </div>
                <div>
                  <div className="muted">Humidity (%)</div>
                  <input
                    className="input"
                    type="number"
                    value={form.humidity}
                    onChange={(e) => setForm((f) => ({ ...f, humidity: e.target.value }))}
                  />
                </div>
                <div>
                  <div className="muted">River level (m)</div>
                  <input
                    className="input"
                    type="number"
                    step="0.1"
                    value={form.river_level_m}
                    onChange={(e) => setForm((f) => ({ ...f, river_level_m: e.target.value }))}
                  />
                </div>
                <div>
                  <div className="muted">Drainage capacity (0–100)</div>
                  <input
                    className="input"
                    type="number"
                    value={form.drainage_capacity}
                    onChange={(e) => setForm((f) => ({ ...f, drainage_capacity: e.target.value }))}
                  />
                </div>
              </div>

              <div className="formActions">
                <button className="btn" type="button" onClick={save}>
                  Save + Recompute risk
                </button>
                <span className="badge">
                  {badgeDot(selected.risk_level)} {selected.risk_level} • {Number(selected.risk_percent || 0).toFixed(1)}%
                </span>
              </div>
              <div className="muted" style={{ marginTop: 10 }}>
                If the computed risk crosses 80%, the backend prints a simulated “SMS alert”.
              </div>
            </>
          )}

          <hr style={{ margin: '24px 0', border: 'none', borderTop: '1px solid var(--border)' }} />

          <h2>Broadcast manual alert</h2>
          <div className="muted" style={{ marginBottom: 10 }}>
            Send a custom alert message to all registered users.
          </div>
          <div style={{ display: 'grid', gap: 10 }}>
            <textarea
              className="input"
              rows={3}
              placeholder="Enter alert message (e.g. Evacuate Pune Mula river areas immediately!)"
              value={broadcastMsg}
              onChange={(e) => setBroadcastMsg(e.target.value)}
              style={{ resize: 'vertical' }}
            />
            <button
              className="btn"
              type="button"
              onClick={broadcastAlert}
              disabled={broadcastLoading || !broadcastMsg}
              style={{ background: 'var(--red)', borderColor: 'var(--red)' }}
            >
              {broadcastLoading ? 'Broadcasting...' : 'Broadcast Alert to All'}
            </button>
          </div>
        </div>
      </div>
    </>
  )
}

