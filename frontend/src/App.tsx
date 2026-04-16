import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'

import { showSweetAlert } from './features/alerts/SweetAlertClient'
import { mockAuthApi } from './features/auth/auth.api.mock'
import { clearSession, getStoredSession, saveSession } from './features/auth/auth.storage'
import type { AuthTab, LoginPayload, RegisterPayload } from './features/auth/auth.types'
import {
  getRegisterFieldErrors,
  validateLogin,
  validateRegister,
} from './features/auth/auth.validation'
import { AuthTabs } from './features/auth/components/AuthTabs'
import { LoginForm } from './features/auth/components/LoginForm'
import { RegisterForm } from './features/auth/components/RegisterForm'
import { ForgotPasswordPage } from './features/auth/pages/ForgotPasswordPage'
import { DashboardView } from './features/dashboard/DashboardView'

const emptyLoginForm: LoginPayload = {
  emailOrUsername: '',
  password: '',
}

const emptyRegisterForm: RegisterPayload = {
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
}

function App() {
  const isForgotPasswordRoute = window.location.pathname === '/forgot-password'

  const [tab, setTab] = useState<AuthTab>('login')
  const [isLoading, setIsLoading] = useState(false)
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [userName, setUserName] = useState('')
  const [loginForm, setLoginForm] = useState<LoginPayload>(emptyLoginForm)
  const [registerForm, setRegisterForm] = useState<RegisterPayload>(emptyRegisterForm)
  const [isTermsAccepted, setIsTermsAccepted] = useState(false)

  const registerErrors = getRegisterFieldErrors(registerForm)
  const isRegisterInvalid = Boolean(
    registerErrors.username ||
      registerErrors.email ||
      registerErrors.password ||
      registerErrors.confirmPassword,
  )

  useEffect(() => {
    const session = getStoredSession()
    if (!session) {
      return
    }

    setIsLoggedIn(true)
    setUserName(session.username)
  }, [])

  const handleLogin = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    const validationError = validateLogin(loginForm)
    if (validationError) {
      await showSweetAlert({
        icon: 'error',
        title: 'Blad walidacji',
        text: validationError,
      })
      return
    }

    setIsLoading(true)
    try {
      const session = await mockAuthApi.login(loginForm)
      saveSession(session)
      setUserName(session.username)
      setIsLoggedIn(true)

      await showSweetAlert({
        icon: 'success',
        title: 'Zalogowano',
        text: 'Witaj! Trwa przekierowanie do dashboardu.',
      })
    } catch (error) {
      await showSweetAlert({
        icon: 'error',
        title: 'Logowanie nieudane',
        text: error instanceof Error ? error.message : 'Wystapil nieoczekiwany blad.',
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleRegister = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    if (!isTermsAccepted) {
      await showSweetAlert({
        icon: 'error',
        title: 'Brak zgody',
        text: 'Aby utworzyc konto, zaakceptuj Regulamin oraz Polityke Prywatnosci.',
      })
      return
    }

    const validationError = validateRegister(registerForm)
    if (validationError) {
      await showSweetAlert({
        icon: 'error',
        title: 'Blad walidacji',
        text: validationError,
      })
      return
    }

    setIsLoading(true)
    try {
      await mockAuthApi.register(registerForm)
      await showSweetAlert({
        icon: 'success',
        title: 'Konto utworzone',
        text: 'Rejestracja zakonczona sukcesem. Mozesz sie teraz zalogowac.',
      })

      setRegisterForm(emptyRegisterForm)
      setIsTermsAccepted(false)
      setTab('login')
    } catch {
      await showSweetAlert({
        icon: 'error',
        title: 'Rejestracja nieudana',
        text: 'Sprobuj ponownie za chwile.',
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleLogout = () => {
    clearSession()
    setIsLoggedIn(false)
    setUserName('')
    setLoginForm(emptyLoginForm)
  }

  if (isLoggedIn) {
    return <DashboardView userName={userName} onLogout={handleLogout} />
  }

  if (isForgotPasswordRoute) {
    return <ForgotPasswordPage />
  }

  return (
    <main className="grid h-screen max-h-screen place-items-center overflow-hidden bg-discord-bg p-5 text-discord-text">
      <div className="atmo-bg" aria-hidden="true" />

      <section className="auth-card relative z-10 w-full max-w-md max-h-screen overflow-hidden rounded-3xl border border-discord-border bg-discord-panel/95 p-6 shadow-discord md:p-8">
        <div className="mb-7 text-center">
          <h1 className="text-3xl font-bold">teLLMach</h1>
          <p className="mt-2 text-sm text-discord-muted">Twój asysten AI do planowania podróży</p>
        </div>

        <AuthTabs activeTab={tab} onChange={setTab} />

        {tab === 'login' ? (
          <LoginForm value={loginForm} isLoading={isLoading} onChange={setLoginForm} onSubmit={handleLogin} />
        ) : (
          <RegisterForm
            value={registerForm}
            errors={registerErrors}
            isInvalid={isRegisterInvalid}
            isTermsAccepted={isTermsAccepted}
            isLoading={isLoading}
            onTermsAcceptedChange={setIsTermsAccepted}
            onChange={setRegisterForm}
            onSubmit={handleRegister}
          />
        )}
      </section>
    </main>
  )
}

export default App
