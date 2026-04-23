import type { ChangeEvent, FormEvent } from 'react'

import type { LoginPayload } from '../auth.types'

type LoginFormProps = {
  value: LoginPayload
  isLoading: boolean
  onChange: (next: LoginPayload) => void
  onSubmit: (event: FormEvent<HTMLFormElement>) => void
}

export function LoginForm({ value, isLoading, onChange, onSubmit }: LoginFormProps) {
  const handleFieldChange =
    (field: keyof LoginPayload) => (event: ChangeEvent<HTMLInputElement>) => {
      onChange({ ...value, [field]: event.target.value })
    }

  return (
    <form className="form-switch space-y-4" onSubmit={onSubmit} noValidate>
      <label className="block space-y-2">
        <span className="text-sm text-discord-muted">Email</span>
        <input
          type="email"
          className="w-full rounded-xl border border-discord-border bg-discord-card px-4 py-3 text-sm outline-none transition focus:border-discord-accent"
          value={value.email}
          onChange={handleFieldChange('email')}
          placeholder="mail@domena.pl"
          autoComplete="email"
        />
      </label>

      <label className="block space-y-2">
        <span className="text-sm text-discord-muted">Haslo</span>
        <input
          type="password"
          className="w-full rounded-xl border border-discord-border bg-discord-card px-4 py-3 text-sm outline-none transition focus:border-discord-accent"
          value={value.password}
          onChange={handleFieldChange('password')}
          placeholder="Twoje haslo"
          autoComplete="current-password"
        />
      </label>

      <div className="flex justify-end">
        <a
          href="/forgot-password"
          className="text-xs font-medium text-[#8ea1ff] transition hover:text-[#b3beff]"
        >
          Zapomnialem hasla
        </a>
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="w-full rounded-xl bg-discord-accent px-4 py-3 text-sm font-semibold text-white transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-70"
      >
        {isLoading ? 'Logowanie...' : 'Zaloguj sie'}
      </button>
    </form>
  )
}

