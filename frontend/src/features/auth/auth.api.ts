import type { LoginPayload, RegisterPayload, SessionUser, TokenResponse } from './auth.types'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const authApi = {
  async login(payload: LoginPayload): Promise<TokenResponse> {
    const response = await fetch(`${API_URL}/login?email=${encodeURIComponent(payload.email)}&password=${encodeURIComponent(payload.password)}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Login failed')
    }

    return response.json()
  },

  async register(payload: RegisterPayload): Promise<SessionUser> {
    const response = await fetch(`${API_URL}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        imie: payload.imie,
        nazwisko: payload.nazwisko,
        email: payload.email,
        password: payload.password,
      }),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Registration failed')
    }

    return response.json()
  },

  async getCurrentUser(token: string): Promise<SessionUser> {
    const response = await fetch(`${API_URL}/me`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
    })

    if (!response.ok) {
      throw new Error('Failed to get current user')
    }

    return response.json()
  },
}
