type DashboardViewProps = {
  userName: string
  onLogout: () => void
}

export function DashboardView({ userName, onLogout }: DashboardViewProps) {
  return (
    <main className="min-h-screen bg-discord-bg p-6 text-discord-text">
      <section className="auth-card mx-auto flex min-h-[calc(100vh-3rem)] w-full max-w-3xl flex-col items-center justify-center rounded-3xl border border-discord-border bg-discord-panel/90 p-10 text-center shadow-discord backdrop-blur">
        <p className="mb-3 text-sm uppercase tracking-[0.18em] text-discord-muted">Dashboard</p>
        <h1 className="mb-4 text-4xl font-bold md:text-5xl">Witaj, {userName}</h1>
        <p className="max-w-xl text-base text-discord-muted md:text-lg">
          Logowanie przebieglo poprawnie. To jest mockowany dashboard dostepu uzytkownika.
        </p>
        <button
          type="button"
          className="mt-8 rounded-xl bg-discord-accent px-5 py-3 text-sm font-semibold text-white transition hover:brightness-110"
          onClick={onLogout}
        >
          Wyloguj
        </button>
      </section>
    </main>
  )
}
