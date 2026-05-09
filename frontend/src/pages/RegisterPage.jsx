import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api } from '../lib/api.js'

export function RegisterPage() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [fullName, setFullName] = useState('')
  const [phoneNumber, setPhoneNumber] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function onSubmit(e) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      await api.post('/auth/register', { email, full_name: fullName, password, phone_number: phoneNumber })
      navigate('/login')
    } catch (err) {
      setError(err?.response?.data?.detail || err?.message || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="authWrap">
      <div className="card authCard">
        <h1>Register</h1>
        <p>Create an account. The first account is Admin for demo purposes.</p>

        <form onSubmit={onSubmit} className="grid">
          <div>
            <div className="muted">Full name</div>
            <input className="input" value={fullName} onChange={(e) => setFullName(e.target.value)} />
          </div>
          <div>
            <div className="muted">Email</div>
            <input className="input" value={email} onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div>
            <div className="muted">Phone Number (e.g. +91...)</div>
            <input 
              className="input" 
              placeholder="+910000000000"
              value={phoneNumber} 
              onChange={(e) => setPhoneNumber(e.target.value)} 
            />
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
            {loading ? 'Creating…' : 'Create account'}
          </button>
        </form>

        <div style={{ marginTop: 12 }} className="muted">
          Already registered? <Link to="/login">Login</Link>
        </div>
      </div>
    </div>
  )
}

