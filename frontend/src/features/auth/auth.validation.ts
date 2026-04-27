import type { LoginPayload, RegisterPayload } from './auth.types'

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export type LoginFieldErrors = {
  email?: string
  password?: string
}

export type RegisterFieldErrors = {
  imie?: string
  nazwisko?: string
  email?: string
  password?: string
  confirmPassword?: string
}

export const getLoginFieldErrors = (payload: LoginPayload): LoginFieldErrors => {
  const errors: LoginFieldErrors = {}

  if (!payload.email.trim()) {
    errors.email = 'Podaj email.'
  } else if (!emailRegex.test(payload.email)) {
    errors.email = 'Podaj poprawny adres email.'
  }

  if (payload.password.length < 4) {
    errors.password = 'Haslo musi miec minimum 4 znaki.'
  }

  return errors
}

export const getRegisterFieldErrors = (payload: RegisterPayload): RegisterFieldErrors => {
  const errors: RegisterFieldErrors = {}

  if (!payload.imie.trim()) {
    errors.imie = 'Imie jest wymagane.'
  }

  if (!payload.nazwisko.trim()) {
    errors.nazwisko = 'Nazwisko jest wymagane.'
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
  if (errors.email) return errors.email
  if (errors.password) return errors.password

  return null
}

export const validateRegister = (payload: RegisterPayload): string | null => {
  const errors = getRegisterFieldErrors(payload)
  if (errors.imie) return errors.imie
  if (errors.nazwisko) return errors.nazwisko
  if (errors.email) return errors.email
  if (errors.password) return errors.password
  if (errors.confirmPassword) return errors.confirmPassword

  return null
}

