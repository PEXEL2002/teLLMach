import type { SessionUser } from './auth.types'

const AUTH_SESSION_KEY = 'tellmach-auth-session'
const AUTH_TOKEN_KEY = 'tellmach-auth-token'

export interface StoredSession {
  user: SessionUser
  token: string
}

export const getStoredSession = (): StoredSession | null => {
  const raw = localStorage.getItem(AUTH_SESSION_KEY)
  const token = localStorage.getItem(AUTH_TOKEN_KEY)

  if (!raw || !token) {
    return null
  }

  try {
    const user = JSON.parse(raw) as SessionUser
    if (!user.id || !user.email) {
      return null
    }
    return { user, token }
  } catch {
    return null
  }
}

export const saveSession = (user: SessionUser, token: string): void => {
  localStorage.setItem(AUTH_SESSION_KEY, JSON.stringify(user))
  localStorage.setItem(AUTH_TOKEN_KEY, token)
}

export const getToken = (): string | null => {
  return localStorage.getItem(AUTH_TOKEN_KEY)
}

export const clearSession = (): void => {
  localStorage.removeItem(AUTH_SESSION_KEY)
  localStorage.removeItem(AUTH_TOKEN_KEY)
}

