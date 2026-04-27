export type AlertKind = 'success' | 'error' | 'warning' | 'info' | 'question'

type SwalFireOptions = {
  icon?: AlertKind
  title: string
  text: string
  confirmButtonColor?: string
  background?: string
  color?: string
}

type SwalApi = {
  fire: (options: SwalFireOptions) => Promise<unknown>
}

declare global {
  interface Window {
    Swal?: SwalApi
  }
}

export const showSweetAlert = async (options: SwalFireOptions): Promise<void> => {
  if (window.Swal) {
    await window.Swal.fire({
      confirmButtonColor: '#5865F2',
      background: '#313338',
      color: '#F2F3F5',
      ...options,
    })
    return
  }

  window.alert(`${options.title}\n\n${options.text}`)
}
