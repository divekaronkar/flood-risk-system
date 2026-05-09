import { useMemo, useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { api } from '../lib/api.js'
import { setToken, setUser } from '../lib/auth.js'

export function LoginPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const from = useMemo(() => location.state?.from || '/', [location.state])

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function onSubmit(e) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const res = await api.post('/auth/login', { email, password })
      setToken(res.data.access_token)
      setUser(res.data.user)
      navigate(from, { replace: true })
    } catch (err) {
      setError(err?.response?.data?.detail || err?.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="authWrap">
      <div className="card authCard">
        <h1>Login</h1>
        <p>Access your flood-risk dashboard (JWT auth).</p>

        <form onSubmit={onSubmit} className="grid">
          <div>
            <div className="muted">Email</div>
            <input className="input" value={email} onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div>
            <div className="muted">Password</div>
            <input
              className="input"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          {error ? <div className="badge" style={{ borderColor: 'rgba(239,68,68,.5)' }}>{error}</div> : null}

          <button className="btn" type="submit" disabled={loading}>
            {loading ? 'Signing in…' : 'Sign in'}
          </button>
        </form>

        <div style={{ marginTop: 12 }} className="muted">
          New here? <Link to="/register">Create an account</Link>
        </div>
      </div>
    </div>
  )
}

