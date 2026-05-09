import { useEffect, useState } from 'react'
import { api } from '../lib/api.js'
import { getUser, setUser } from '../lib/auth.js'

export function ProfilePage() {
  const [profile, setProfile] = useState(getUser())
  const [form, setForm] = useState({
    full_name: '',
    phone_number: '',
  })
  const [loading, setLoading] = useState(false)
  const [fetching, setFetching] = useState(true)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  useEffect(() => {
    async function fetchProfile() {
      try {
        const res = await api.get('/auth/me')
        setProfile(res.data)
        setUser(res.data)
        setForm({
          full_name: res.data.full_name || '',
          phone_number: res.data.phone_number || '',
        })
      } catch (err) {
        console.error('Failed to fetch profile', err)
      } finally {
        setFetching(false)
      }
    }
    fetchProfile()
  }, [])

  async function onSave(e) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setSuccess(false)
    try {
      const res = await api.patch('/users/me', form)
      setProfile(res.data)
      setUser(res.data) // Update local storage
      setSuccess(true)
    } catch (err) {
      setError(err?.response?.data?.detail || 'Update failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <div className="topbar">
        <div>
          <h1 className="pageTitle">User Profile</h1>
          <p className="subtitle">Manage your personal information and alert settings.</p>
        </div>
      </div>

      <div className="card panel" style={{ maxWidth: 600 }}>
        {fetching ? (
          <div className="muted">Loading profile details...</div>
        ) : (
          <form onSubmit={onSave} className="grid">
            <div>
              <div className="muted">Email (Read-only)</div>
              <input className="input" value={profile?.email || ''} disabled />
            </div>
            <div>
              <div className="muted">Full Name</div>
              <input
                className="input"
                value={form.full_name}
                onChange={(e) => setForm({ ...form, full_name: e.target.value })}
                required
              />
            </div>
            <div>
              <div className="muted">Phone Number (for SMS alerts)</div>
              <input
                className="input"
                placeholder="+91..."
                value={form.phone_number}
                onChange={(e) => setForm({ ...form, phone_number: e.target.value })}
              />
            </div>
            <div>
              <div className="muted">Role</div>
              <div className="badge">{profile?.role || 'user'}</div>
            </div>

            {error && <div className="badge" style={{ borderColor: 'rgba(239,68,68,.5)' }}>{error}</div>}
            {success && <div className="badge" style={{ borderColor: 'rgba(34,197,94,.5)', color: 'var(--green)' }}>Profile updated successfully!</div>}

            <button className="btn" type="submit" disabled={loading}>
              {loading ? 'Saving...' : 'Update Profile'}
            </button>
          </form>
        )}
      </div>
    </>
  )
}
