interface ChatMessageProps {
  position: 'start' | 'end';
  avatarUrl: string;
  name: string;
  time: string;
  message: string;
}

export default function ChatMessage({
  position,
  avatarUrl,
  name,
  time,
  message,
}: ChatMessageProps) {
  return (
    <div className={`chat chat-${position}`}>
      <div className="chat-image avatar">
        <div className="w-10 rounded-full">
          <img src={avatarUrl} alt={`${name}'s avatar`} />
        </div>
      </div>
      <div className="chat-header">
        {name}
        <time className="text-xs opacity-50">{time}</time>
      </div>
      <div className="chat-bubble">{message}</div>
    </div>
  )
}
