import type { SessionUser } from './auth.types'

const AUTH_SESSION_KEY = 'tellmach-auth-session'

export const getStoredSession = (): SessionUser | null => {
  const raw = localStorage.getItem(AUTH_SESSION_KEY)
  if (!raw) {
    return null
  }

  try {
    const parsed = JSON.parse(raw) as SessionUser
    if (!parsed.username) {
      return null
    }
    return parsed
  } catch {
    return null
  }
}

export const saveSession = (session: SessionUser): void => {
  localStorage.setItem(AUTH_SESSION_KEY, JSON.stringify(session))
}

export const clearSession = (): void => {
  localStorage.removeItem(AUTH_SESSION_KEY)
}
