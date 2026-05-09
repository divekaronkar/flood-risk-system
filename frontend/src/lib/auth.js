export function setToken(token) {
  localStorage.setItem('token', token)
}

export function setUser(user) {
  localStorage.setItem('user', JSON.stringify(user))
}

export function getUser() {
  const u = localStorage.getItem('user')
  try {
    return u ? JSON.parse(u) : null
  } catch {
    return null
  }
}

export function clearToken() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
}

export function getToken() {
  return localStorage.getItem('token')
}

export function isAuthed() {
  return Boolean(getToken())
}

