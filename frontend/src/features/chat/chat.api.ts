import { getToken } from '../auth/auth.storage'
import type { ChatMessage } from './chat.types'

const API_BASE = (import.meta.env.VITE_API_URL || 'http://localhost:8000') + '/api'

function authHeaders() {
  const token = getToken()
  return {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
  }
}

function extractText(raw: string): string {
  const trimmed = raw.trim()
  if (!trimmed || trimmed === '[DONE]') return ''
  try {
    const parsed = JSON.parse(trimmed)
    return parsed.output ?? parsed.content ?? parsed.text ?? parsed.chunk ?? ''
  } catch {
    return trimmed
  }
}

export const chatApi = {
  async loadHistory(): Promise<ChatMessage[]> {
    const response = await fetch(`${API_BASE}/history`, { headers: authHeaders() })
    if (!response.ok) return []
    const rows: { id: number; role: string; content: string; created_at: string }[] = await response.json()
    return rows.map(r => ({
      id: String(r.id),
      role: r.role as ChatMessage['role'],
      content: r.content,
      timestamp: new Date(r.created_at),
    }))
  },

  async saveMessages(messages: Pick<ChatMessage, 'role' | 'content'>[]): Promise<void> {
    await fetch(`${API_BASE}/history`, {
      method: 'POST',
      headers: authHeaders(),
      body: JSON.stringify({ messages }),
    })
  },

  async streamMessage(
    message: string,
    onChunk: (text: string) => void,
    onDone: () => void,
  ): Promise<void> {
    const response = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: authHeaders(),
      body: JSON.stringify({ message }),
    })

    if (!response.ok) {
      throw new Error(`Chat request failed: ${response.status} ${response.statusText}`)
    }

    const contentType = response.headers.get('content-type') ?? ''

    if (contentType.includes('event-stream') || contentType.includes('octet-stream')) {
      const reader = response.body!.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() ?? ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            if (data === '[DONE]') { onDone(); return }
            const text = extractText(data)
            if (text) onChunk(text)
          } else if (line.startsWith('event:') || line === '') {
            // skip SSE metadata lines
          } else {
            const text = extractText(line)
            if (text) onChunk(text)
          }
        }
      }

      onDone()
      return
    }

    const data = await response.json()
    const text = data.output ?? data.content ?? data.text ?? ''
    if (text) onChunk(text)
    onDone()
  },
}
