export type AuthTab = 'login' | 'register'

export type LoginPayload = {
  email: string
  password: string
}

export type RegisterPayload = {
  imie: string
  nazwisko: string
  email: string
  password: string
  confirmPassword: string
}

export type SessionUser = {
  id: number
  imie: string
  nazwisko: string
  email: string
}

export type TokenResponse = {
  access_token: string
  token_type: string
  user_id: number
  email: string
}
