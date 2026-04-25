import type { ChatMessage } from '../chat.types'

type ChatMessageProps = {
  message: ChatMessage
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-3 animate-fade-in`}>
      <div
        className={`max-w-xs px-4 py-2 rounded-lg ${
          isUser
            ? 'bg-discord-accent text-white rounded-br-none'
            : 'bg-discord-panel border border-discord-border text-discord-text rounded-bl-none'
        }`}
      >
        <p className="text-sm break-words">{message.content}</p>
        <span className="text-xs opacity-60 mt-1 block">
          {message.timestamp.toLocaleTimeString('pl-PL', {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </span>
      </div>
    </div>
  )
}
