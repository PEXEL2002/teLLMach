import ReactMarkdown from 'react-markdown'
import type { ChatMessage } from '../chat.types'

type ChatMessageProps = {
  message: ChatMessage
  isStreaming?: boolean
}

export function ChatMessage({ message, isStreaming }: ChatMessageProps) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-3 animate-fade-in`}>
      <div
        className={`max-w-[75%] px-4 py-2 rounded-lg ${
          isUser
            ? 'bg-discord-accent text-white rounded-br-none'
            : 'bg-discord-panel border border-discord-border text-discord-text rounded-bl-none'
        }`}
      >
        {isUser ? (
          <p className="text-sm break-words whitespace-pre-wrap">{message.content}</p>
        ) : (
          <div className="text-sm break-words prose prose-invert prose-sm max-w-none">
            <ReactMarkdown>{message.content}</ReactMarkdown>
            {isStreaming && (
              <span className="inline-block w-0.5 h-4 bg-discord-text ml-0.5 animate-pulse" />
            )}
          </div>
        )}
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
