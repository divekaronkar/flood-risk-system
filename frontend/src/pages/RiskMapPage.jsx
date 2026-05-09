import { useEffect, useMemo, useState } from 'react'
import { CircleMarker, MapContainer, Popup, TileLayer, useMap } from 'react-leaflet'
import { api } from '../lib/api.js'

function FitBounds({ locations }) {
  const map = useMap()
  useEffect(() => {
    if (locations.length > 0) {
      const bounds = locations.map(l => [l.lat, l.lng])
      map.fitBounds(bounds, { padding: [50, 50] })
    }
  }, [locations, map])
  return null
}

function colorForLevel(level) {
  if (level === 'High') return '#ef4444'
  if (level === 'Medium') return '#f59e0b'
  return '#22c55e'
}

export function RiskMapPage() {
  const [locations, setLocations] = useState([])
  const [loading, setLoading] = useState(true)
  const [live, setLive] = useState(true)

  const center = useMemo(() => {
    if (locations.length) return [locations[0].lat, locations[0].lng]
    return [19.076, 72.8777]
  }, [locations])

  useEffect(() => {
    let mounted = true
    async function load() {
      setLoading(true)
      try {
        const res = await api.get('/locations')
        if (mounted) setLocations(res.data)
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
    if (!live) return
    const ws = new WebSocket('ws://127.0.0.1:8000/api/ws')
    ws.onmessage = (evt) => {
      try {
        const msg = JSON.parse(evt.data)
        if (msg.type === 'locations_update' && Array.isArray(msg.locations)) {
          setLocations((prev) => {
            const map = new Map(prev.map((p) => [p.id, p]))
            for (const l of msg.locations) map.set(l.id, l)
            return Array.from(map.values())
          })
        }
      } catch {
        // ignore
      }
    }
    ws.onerror = () => {}
    return () => ws.close()
  }, [live])

  return (
    <>
      <div className="topbar">
        <div>
          <h1 className="pageTitle">Risk Map</h1>
          <p className="subtitle">Color-coded risk markers (Low / Medium / High).</p>
        </div>

        <div style={{ display: 'flex', gap: 10, alignItems: 'center', flexWrap: 'wrap' }}>
          <button className="btn secondary" type="button" onClick={() => setLive((v) => !v)}>
            Live: {live ? 'ON' : 'OFF'}
          </button>

          <div className="badge">
          <span className="dot low" />
          Low
          <span style={{ width: 10 }} />
          <span className="dot medium" />
          Medium
          <span style={{ width: 10 }} />
          <span className="dot high" />
          High
          </div>
        </div>
      </div>

      <div className="card mapWrap">
        {loading ? (
          <div style={{ padding: 16 }} className="muted">
            Loading locations…
          </div>
        ) : (
          <MapContainer center={center} zoom={5} style={{ height: '100%', width: '100%' }}>
            <TileLayer
              attribution='&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png"
            />
            <FitBounds locations={locations} />

            {locations.map((l) => (
              <CircleMarker
                key={l.id}
                center={[l.lat, l.lng]}
                radius={l.is_dam ? 14 : 10}
                pathOptions={{ 
                  color: colorForLevel(l.risk_level), 
                  fillOpacity: 0.75,
                  weight: l.is_dam ? 4 : 2,
                  dashArray: l.is_dam ? '5, 5' : null
                }}
              >
                <Popup>
                  <div style={{ color: '#0b1020', fontWeight: 800 }}>
                    {l.is_dam ? '🏢 ' : '🌊 '} {l.name}
                  </div>
                  <div style={{ color: '#0b1020' }}>
                    Type: <b>{l.is_dam ? 'Dam / Reservoir' : 'River Section'}</b>
                  </div>
                  <div style={{ color: '#0b1020' }}>
                    Risk: <b>{l.risk_level}</b> ({l.risk_percent?.toFixed?.(1)}%)
                  </div>
                  <div style={{ color: '#0b1020', marginTop: 6, fontSize: 12 }}>
                    Rainfall: {l.rainfall_mm}mm • Humidity: {l.humidity}% • {l.is_dam ? 'Water' : 'River'}: {l.river_level_m}m • Drainage:{' '}
                    {l.drainage_capacity}
                  </div>
                </Popup>
              </CircleMarker>
            ))}
          </MapContainer>
        )}
      </div>
    </>
  )
}

