import { useEffect, useMemo, useState } from 'react'
import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from 'chart.js'
import { api } from '../lib/api.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend)

export function AnalyticsPage() {
  const [rows, setRows] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let mounted = true
    async function load() {
      setLoading(true)
      try {
        const res = await api.get('/analytics/trends')
        if (mounted) setRows(res.data)
      } finally {
        if (mounted) setLoading(false)
      }
    }
    load()
    return () => {
      mounted = false
    }
  }, [])

  const data = useMemo(() => {
    const labels = rows.map((r) => String(r.year))
    return {
      labels,
      datasets: [
        {
          label: 'Flood events',
          data: rows.map((r) => r.flood_events),
          borderColor: '#ef4444',
          backgroundColor: 'rgba(239,68,68,0.2)',
          tension: 0.25,
          yAxisID: 'y',
        },
        {
          label: 'Avg rainfall (mm)',
          data: rows.map((r) => r.avg_rainfall_mm),
          borderColor: '#7c3aed',
          backgroundColor: 'rgba(124,58,237,0.2)',
          tension: 0.25,
          yAxisID: 'y1',
        },
      ],
    }
  }, [rows])

  const options = useMemo(
    () => ({
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: '#cbd5e1' } },
        tooltip: { enabled: true },
      },
      scales: {
        x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(148,163,184,0.12)' } },
        y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(148,163,184,0.12)' }, position: 'left' },
        y1: {
          ticks: { color: '#94a3b8' },
          grid: { drawOnChartArea: false },
          position: 'right',
        },
      },
    }),
    [],
  )

  return (
    <>
      <div className="topbar">
        <div>
          <h1 className="pageTitle">Historical Analytics</h1>
          <p className="subtitle">Last 10 years trend (simulated historical dataset).</p>
        </div>
      </div>

      <div className="card panel" style={{ height: 420 }}>
        {loading ? (
          <div className="muted">Loading trend data…</div>
        ) : rows.length ? (
          <Line data={data} options={options} />
        ) : (
          <div className="muted">No analytics rows yet. Run backend seeding.</div>
        )}
      </div>
    </>
  )
}

