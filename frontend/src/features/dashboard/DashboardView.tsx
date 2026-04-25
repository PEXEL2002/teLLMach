import { ChatInterface } from '../chat'

type DashboardViewProps = {
  userName: string
  onLogout: () => void
}

export function DashboardView({ userName, onLogout }: DashboardViewProps) {
  return (
    <main className="grid h-screen max-h-screen place-items-center overflow-hidden bg-discord-bg p-5 text-discord-text">
      <div className="atmo-bg" aria-hidden="true" />

      <section className="auth-card relative z-10 flex flex-col w-full max-w-4xl max-h-screen rounded-3xl border border-discord-border bg-discord-panel/95 shadow-discord overflow-hidden">
        {/* Header with User Info */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-discord-border bg-discord-panel/80">
          <div>
            <h1 className="text-xl font-semibold text-discord-text">Witaj, {userName}</h1>
            <p className="text-xs text-discord-muted mt-1">AI Travel Assistant</p>
          </div>
          <button
            type="button"
            className="px-4 py-2 text-sm font-medium text-discord-muted hover:text-discord-text border border-discord-border rounded-lg transition hover:bg-discord-panel/50"
            onClick={onLogout}
          >
            Wyloguj
          </button>
        </div>

        {/* Chat Interface */}
        <div className="flex-1 overflow-hidden">
          <ChatInterface />
        </div>
      </section>
    </main>
  )
}
