import type { LoginPayload, RegisterPayload, SessionUser } from './auth.types'

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

export const mockAuthApi = {
  async login(payload: LoginPayload): Promise<SessionUser> {
    await delay(700)

    const identifier = payload.emailOrUsername.trim().toLowerCase()
    if (identifier === 'admin' && payload.password === 'admin') {
      return { username: 'admin' }
    }

    throw new Error('Niepoprawne dane logowania. Uzyj admin / admin.')
  },

  async register(_payload: RegisterPayload): Promise<{ ok: true }> {
    await delay(900)
    return { ok: true }
  },
}
