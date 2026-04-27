export function ForgotPasswordPage() {
  return (
    <main className="grid h-screen max-h-screen place-items-center overflow-hidden bg-discord-bg p-5 text-discord-text">
      <div className="atmo-bg" aria-hidden="true" />

      <section className="auth-card relative z-10 w-full max-w-md rounded-3xl border border-discord-border bg-discord-panel/95 p-6 shadow-discord md:p-8">
        <div className="text-center">
          <p className="mb-2 text-xs uppercase tracking-[0.2em] text-discord-muted">teLLMach</p>
          <h1 className="text-3xl font-bold">Zapomnialem hasla</h1>
          <p className="mt-3 text-sm text-discord-muted">
            Funkcja resetu hasla jest w przygotowaniu. Coming soon.
          </p>
        </div>

        <a
          href="/"
          className="mt-6 block w-full rounded-xl bg-discord-accent px-4 py-3 text-center text-sm font-semibold text-white transition hover:brightness-110"
        >
          Wroc do logowania
        </a>
      </section>
    </main>
  )
}
