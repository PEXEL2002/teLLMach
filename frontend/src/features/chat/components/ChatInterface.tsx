import { useEffect, useRef, useState } from 'react'
import { showSweetAlert } from '../../alerts/SweetAlertClient'
import { chatApi } from '../chat.api'
import type { ChatMessage } from '../chat.types'
import { ChatMessage as ChatMessageComponent } from './ChatMessage'

const generateId = () => Math.random().toString(36).substring(2, 11)

export function ChatInterface() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: generateId(),
      role: 'assistant',
      content: 'Cześć! Jestem AI Travel Assistant. Jak się masz? Chciałbyś zaplanować podróż?',
      timestamp: new Date(),
    },
  ])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!inputValue.trim()) {
      return
    }

    // Add user message
    const userMessage: ChatMessage = {
      id: generateId(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInputValue('')
    setIsLoading(true)

    try {
      const response = await chatApi.sendMessage(inputValue)

      // Add assistant response
      const assistantMessage: ChatMessage = {
        id: response.id,
        role: 'assistant',
        content: response.content,
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      console.error('Chat error:', error)
      await showSweetAlert({
        icon: 'error',
        title: 'Błąd',
        text: error instanceof Error ? error.message : 'Nie udało się wysłać wiadomości',
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-full w-full overflow-hidden">
      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-3 scroll-smooth">
        {messages.map((message) => (
          <ChatMessageComponent key={message.id} message={message} />
        ))}

        {isLoading && (
          <div className="flex justify-start mb-3 animate-fade-in">
            <div className="bg-discord-panel border border-discord-border text-discord-text rounded-lg rounded-bl-none px-4 py-2">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-discord-muted rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-discord-muted rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                <div className="w-2 h-2 bg-discord-muted rounded-full animate-bounce" style={{ animationDelay: '0.4s' }} />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Field */}
      <div className="px-6 py-4 border-t border-discord-border bg-discord-panel/60">
        <form onSubmit={handleSendMessage} className="flex gap-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            disabled={isLoading}
            placeholder="Napisz wiadomość..."
            className="flex-1 px-4 py-3 bg-discord-bg border border-discord-border rounded-xl text-discord-text text-sm placeholder-discord-muted focus:outline-none focus:border-discord-accent transition disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={isLoading || !inputValue.trim()}
            className="px-6 py-3 bg-discord-accent text-white rounded-xl font-semibold text-sm hover:brightness-110 disabled:opacity-50 disabled:hover:brightness-100 transition whitespace-nowrap"
          >
            {isLoading ? 'Czeka...' : 'Wyślij'}
          </button>
        </form>
      </div>
    </div>
  )
}

