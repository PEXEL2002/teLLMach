import type { ChangeEvent, FormEvent } from 'react'
import { useState } from 'react'

import type { RegisterPayload } from '../auth.types'
import type { RegisterFieldErrors } from '../auth.validation'

type RegisterFormProps = {
  value: RegisterPayload
  errors: RegisterFieldErrors
  isInvalid: boolean
  isTermsAccepted: boolean
  isLoading: boolean
  onChange: (next: RegisterPayload) => void
  onTermsAcceptedChange: (value: boolean) => void
  onSubmit: (event: FormEvent<HTMLFormElement>) => void
}

export function RegisterForm({
  value,
  errors,
  isInvalid,
  isTermsAccepted,
  isLoading,
  onChange,
  onTermsAcceptedChange,
  onSubmit,
}: RegisterFormProps) {
  const [touched, setTouched] = useState<Record<keyof RegisterPayload, boolean>>({
    imie: false,
    nazwisko: false,
    email: false,
    password: false,
    confirmPassword: false,
  })

  const handleFieldChange =
    (field: keyof RegisterPayload) => (event: ChangeEvent<HTMLInputElement>) => {
      onChange({ ...value, [field]: event.target.value })
    }

  const handleFieldBlur = (field: keyof RegisterPayload) => () => {
    if (!touched[field]) {
      setTouched((prev) => ({ ...prev, [field]: true }))
    }
  }

  const showError = (field: keyof RegisterPayload): boolean => touched[field] && Boolean(errors[field])

  return (
    <form className="form-switch space-y-4" onSubmit={onSubmit} noValidate>
      <label className="block space-y-2">
        <span className="text-sm text-discord-muted">Imie</span>
        <input
          className={`w-full rounded-xl border bg-discord-card px-4 py-3 text-sm outline-none transition focus:border-discord-accent ${
            showError('imie') ? 'border-red-400/80' : 'border-discord-border'
          }`}
          value={value.imie}
          onChange={handleFieldChange('imie')}
          onBlur={handleFieldBlur('imie')}
          placeholder="Jan"
          autoComplete="given-name"
          aria-invalid={showError('imie')}
        />
        {showError('imie') ? <p className="text-xs text-red-300">{errors.imie}</p> : null}
      </label>

      <label className="block space-y-2">
        <span className="text-sm text-discord-muted">Nazwisko</span>
        <input
          className={`w-full rounded-xl border bg-discord-card px-4 py-3 text-sm outline-none transition focus:border-discord-accent ${
            showError('nazwisko') ? 'border-red-400/80' : 'border-discord-border'
          }`}
          value={value.nazwisko}
          onChange={handleFieldChange('nazwisko')}
          onBlur={handleFieldBlur('nazwisko')}
          placeholder="Kowalski"
          autoComplete="family-name"
          aria-invalid={showError('nazwisko')}
        />
        {showError('nazwisko') ? <p className="text-xs text-red-300">{errors.nazwisko}</p> : null}
      </label>

      <label className="block space-y-2">
        <span className="text-sm text-discord-muted">Email</span>
        <input
          type="email"
          className={`w-full rounded-xl border bg-discord-card px-4 py-3 text-sm outline-none transition focus:border-discord-accent ${
            showError('email') ? 'border-red-400/80' : 'border-discord-border'
          }`}
          value={value.email}
          onChange={handleFieldChange('email')}
          onBlur={handleFieldBlur('email')}
          placeholder="mail@domena.pl"
          autoComplete="email"
          aria-invalid={showError('email')}
        />
        {showError('email') ? <p className="text-xs text-red-300">{errors.email}</p> : null}
      </label>

      <label className="block space-y-2">
        <span className="text-sm text-discord-muted">Haslo</span>
        <input
          type="password"
          className={`w-full rounded-xl border bg-discord-card px-4 py-3 text-sm outline-none transition focus:border-discord-accent ${
            showError('password') ? 'border-red-400/80' : 'border-discord-border'
          }`}
          value={value.password}
          onChange={handleFieldChange('password')}
          onBlur={handleFieldBlur('password')}
          placeholder="Minimum 8 znakow"
          autoComplete="new-password"
          aria-invalid={showError('password')}
        />
        {showError('password') ? <p className="text-xs text-red-300">{errors.password}</p> : null}
      </label>

      <label className="block space-y-2">
        <span className="text-sm text-discord-muted">Powtorz haslo</span>
        <input
          type="password"
          className={`w-full rounded-xl border bg-discord-card px-4 py-3 text-sm outline-none transition focus:border-discord-accent ${
            showError('confirmPassword') ? 'border-red-400/80' : 'border-discord-border'
          }`}
          value={value.confirmPassword}
          onChange={handleFieldChange('confirmPassword')}
          onBlur={handleFieldBlur('confirmPassword')}
          placeholder="Powtorz haslo"
          autoComplete="new-password"
          aria-invalid={showError('confirmPassword')}
        />
        {showError('confirmPassword') ? (
          <p className="text-xs text-red-300">{errors.confirmPassword}</p>
        ) : null}
      </label>

      <label className="flex items-start gap-3 rounded-xl border border-discord-border bg-discord-card px-4 py-3 text-sm text-discord-muted">
        <input
          type="checkbox"
          className="mt-0.5 h-4 w-4 rounded border-discord-border bg-discord-panel accent-discord-accent"
          checked={isTermsAccepted}
          onChange={(event) => onTermsAcceptedChange(event.target.checked)}
        />
        <span>
          Rejestrujac sie, akceptujesz nasz{' '}
          <a
            href="/regulamin.html"
            target="_blank"
            rel="noreferrer"
            className="font-medium text-[#8ea1ff] hover:text-[#b3beff]"
          >
            Regulamin
          </a>{' '}
          oraz{' '}
          <a
            href="/polityka-prywatnosci.html"
            target="_blank"
            rel="noreferrer"
            className="font-medium text-[#8ea1ff] hover:text-[#b3beff]"
          >
            Polityke Prywatnosci
          </a>
          .
        </span>
      </label>

      <button
        type="submit"
        disabled={isLoading || isInvalid || !isTermsAccepted}
        className="w-full rounded-xl bg-discord-ok px-4 py-3 text-sm font-semibold text-white transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-70"
      >
        {isLoading ? 'Tworzenie konta...' : 'Utworz konto'}
      </button>
    </form>
  )
}

