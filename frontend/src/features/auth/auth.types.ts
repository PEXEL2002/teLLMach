export type AuthTab = 'login' | 'register'

export type LoginPayload = {
  emailOrUsername: string
  password: string
}

export type RegisterPayload = {
  username: string
  email: string
  password: string
  confirmPassword: string
}

export type SessionUser = {
  username: string
}
