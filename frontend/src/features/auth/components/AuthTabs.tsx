import type { AuthTab } from '../auth.types'

type AuthTabsProps = {
  activeTab: AuthTab
  onChange: (tab: AuthTab) => void
}

export function AuthTabs({ activeTab, onChange }: AuthTabsProps) {
  return (
    <div className="relative mb-6 grid grid-cols-2 rounded-xl bg-discord-card p-1">
      <span
        className={`absolute inset-y-1 w-[calc(50%-0.25rem)] rounded-lg bg-discord-accent transition-all duration-300 ease-out ${
          activeTab === 'login' ? 'left-1' : 'left-[calc(50%+0.25rem)]'
        }`}
      />

      <button
        type="button"
        onClick={() => onChange('login')}
        className={`relative z-10 rounded-lg px-3 py-2 text-sm font-semibold transition ${
          activeTab === 'login' ? 'text-white' : 'text-discord-muted hover:text-discord-text'
        }`}
      >
        Logowanie
      </button>

      <button
        type="button"
        onClick={() => onChange('register')}
        className={`relative z-10 rounded-lg px-3 py-2 text-sm font-semibold transition ${
          activeTab === 'register' ? 'text-white' : 'text-discord-muted hover:text-discord-text'
        }`}
      >
        Rejestracja
      </button>
    </div>
  )
}
