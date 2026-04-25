import { getToken } from '../auth/auth.storage'
import type { ChatResponse } from './chat.types'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:3001/api'

export const chatApi = {
  async sendMessage(message: string): Promise<ChatResponse> {
    const token = getToken()

    const response = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
      },
      body: JSON.stringify({ message }),
    })

    if (!response.ok) {
      throw new Error(`Chat request failed: ${response.statusText}`)
    }

    return response.json()
  },
}
