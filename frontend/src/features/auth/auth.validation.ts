import type { LoginPayload, RegisterPayload } from './auth.types'

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export type LoginFieldErrors = {
  emailOrUsername?: string
  password?: string
}

export type RegisterFieldErrors = {
  username?: string
  email?: string
  password?: string
  confirmPassword?: string
}

export const getLoginFieldErrors = (payload: LoginPayload): LoginFieldErrors => {
  const errors: LoginFieldErrors = {}

  if (!payload.emailOrUsername.trim()) {
    errors.emailOrUsername = 'Podaj email albo nazwe uzytkownika.'
  } else if (payload.emailOrUsername.includes('@') && !emailRegex.test(payload.emailOrUsername)) {
    errors.emailOrUsername = 'Podaj poprawny adres email.'
  }

  if (payload.password.length < 4) {
    errors.password = 'Haslo musi miec minimum 4 znaki.'
  }

  return errors
}

export const getRegisterFieldErrors = (payload: RegisterPayload): RegisterFieldErrors => {
  const errors: RegisterFieldErrors = {}

  if (!payload.username.trim()) {
    errors.username = 'Nazwa uzytkownika jest wymagana.'
  }

  if (!emailRegex.test(payload.email)) {
    errors.email = 'Podaj poprawny adres email.'
  }

  if (payload.password.length < 8) {
    errors.password = 'Haslo musi miec minimum 8 znakow.'
  }

  if (payload.confirmPassword.length === 0 || payload.password !== payload.confirmPassword) {
    errors.confirmPassword = 'Hasla musza byc takie same.'
  }

  return errors
}

export const validateLogin = (payload: LoginPayload): string | null => {
  const errors = getLoginFieldErrors(payload)
  if (errors.emailOrUsername) return errors.emailOrUsername
  if (errors.password) return errors.password

  return null
}

export const validateRegister = (payload: RegisterPayload): string | null => {
  const errors = getRegisterFieldErrors(payload)
  if (errors.username) return errors.username
  if (errors.email) return errors.email
  if (errors.password) return errors.password
  if (errors.confirmPassword) return errors.confirmPassword

  return null
}
