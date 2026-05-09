import { useEffect, useMemo, useState } from 'react'
import { api } from '../lib/api.js'

function fmtPct(n) {
  if (Number.isFinite(n)) return `${n.toFixed(1)}%`
  return '—'
}

export function DashboardPage() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [predictLoading, setPredictLoading] = useState(false)
  const [predictRes, setPredictRes] = useState(null)
  const [predictErr, setPredictErr] = useState(null)

  const [form, setForm] = useState({
    rainfall_mm: 55,
    humidity: 75,
    river_level_m: 3.2,
    drainage_capacity: 55,
  })

  const education = useMemo(
    () => [
      {
        t: 'Flood drivers',
        d: 'Heavy rainfall + high river levels + poor drainage raise the probability of urban flooding.',
      },
      {
        t: 'Risk levels',
        d: 'Low < 50%, Medium 50–79%, High ≥ 80%. Alerts trigger when the model predicts > 80% risk.',
      },
      {
        t: 'How this project works',
        d: 'This is a software-only system using simulated/historical-like data (no sensors).',
      },
    ],
    [],
  )

  useEffect(() => {
    let mounted = true
    async function load() {
      setLoading(true)
      try {
        const res = await api.get('/stats')
        if (mounted) setStats(res.data)
      } finally {
        if (mounted) setLoading(false)
      }
    }
    load()
    return () => {
      mounted = false
    }
  }, [])

  async function runPredict(e) {
    e.preventDefault()
    setPredictErr(null)
    setPredictRes(null)
    setPredictLoading(true)
    try {
      const res = await api.post('/predict', {
        rainfall_mm: Number(form.rainfall_mm),
        humidity: Number(form.humidity),
        river_level_m: Number(form.river_level_m),
        drainage_capacity: Number(form.drainage_capacity),
      })
      setPredictRes(res.data)
    } catch (err) {
      setPredictErr(err?.response?.data?.detail || 'Prediction failed')
    } finally {
      setPredictLoading(false)
    }
  }

  return (
    <>
      <div className="topbar">
        <div>
          <h1 className="pageTitle">Dashboard</h1>
          <p className="subtitle">Live stats + quick ML prediction.</p>
        </div>
      </div>

      <div className="kpiGrid">
        <div className="card kpi">
          <div className="label">Locations</div>
          <div className="value">{loading ? '…' : stats?.total_locations ?? 0}</div>
        </div>
        <div className="card kpi">
          <div className="label">High risk</div>
          <div className="value" style={{ color: 'var(--red)' }}>{loading ? '…' : stats?.high ?? 0}</div>
        </div>
        <div className="card kpi">
          <div className="label">Medium risk</div>
          <div className="value" style={{ color: 'var(--yellow)' }}>{loading ? '…' : stats?.medium ?? 0}</div>
        </div>
        <div className="card kpi">
          <div className="label">Low risk</div>
          <div className="value" style={{ color: 'var(--green)' }}>{loading ? '…' : stats?.low ?? 0}</div>
        </div>
      </div>

      {!loading && stats && (
        <div className="card panel" style={{ marginTop: 12 }}>
          <h2>System Health Overview</h2>
          <div style={{ display: 'flex', height: 12, borderRadius: 6, overflow: 'hidden', background: 'rgba(255,255,255,0.05)' }}>
            <div style={{ width: `${(stats.low / stats.total_locations) * 100}%`, background: 'var(--green)' }} />
            <div style={{ width: `${(stats.medium / stats.total_locations) * 100}%`, background: 'var(--yellow)' }} />
            <div style={{ width: `${(stats.high / stats.total_locations) * 100}%`, background: 'var(--red)' }} />
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 8, fontSize: 12 }} className="muted">
            <span>Low Risk ({((stats.low / stats.total_locations) * 100).toFixed(0)}%)</span>
            <span>Medium Risk ({((stats.medium / stats.total_locations) * 100).toFixed(0)}%)</span>
            <span>High Risk ({((stats.high / stats.total_locations) * 100).toFixed(0)}%)</span>
          </div>
        </div>
      )}

      <div className="twoCol">
        <div className="card panel">
          <h2>ML Flood Risk Prediction (RandomForest)</h2>
          <form onSubmit={runPredict}>
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
              <button className="btn" type="submit" disabled={predictLoading}>
                {predictLoading ? 'Predicting…' : 'Predict risk'}
              </button>

              {predictRes ? (
                <span className="badge">
                  <span className={`dot ${predictRes.risk_level.toLowerCase()}`} />
                  {predictRes.risk_level} • {fmtPct(predictRes.risk_percent)}
                </span>
              ) : null}
            </div>

            {predictRes?.alert_triggered ? (
              <div className="badge" style={{ marginTop: 10, borderColor: 'rgba(239,68,68,.5)' }}>
                Alert triggered: {predictRes.alert_message}
              </div>
            ) : null}

            {predictErr ? (
              <div className="badge" style={{ marginTop: 10, borderColor: 'rgba(239,68,68,.5)' }}>
                {predictErr}
              </div>
            ) : null}
          </form>
        </div>

        <div className="card panel">
          <h2>Flood-risk education</h2>
          <div className="grid">
            {education.map((x) => (
              <div key={x.t} className="card" style={{ padding: 12, background: 'var(--card2)' }}>
                <div style={{ color: 'var(--heading)', fontWeight: 800, fontSize: 13 }}>{x.t}</div>
                <div className="muted" style={{ marginTop: 6 }}>
                  {x.d}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  )
}
