"use client"

import { useEffect, useState } from "react"
import { fetchMessages, sendMessage } from '@/lib/api';
import { Message } from "@/types/message"
import MessageInput from "@/components/MessageInput"
import AgentHeader from "@/components/AgentHeader"
import ChatMessage from "@/components/ChatMessage"

export default function Home() {
  const [inputMessage, setInputMessage] = useState("")
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    console.log("page useEffect");
    setIsLoading(true);
    fetchMessages()
      .then((data) => {
        console.log("📥 Fetched messages:", data); // <-- log here
        setMessages(data);
      })
      .catch(console.error)
      .finally(() => setIsLoading(false));
  }, []);

  async function handleSend(content: string) {
    setIsLoading(true)

    const newMessage = await sendMessage({
      name: 'You',
      avatarUrl: 'https://example.com/your-avatar.png',
      content,
      position: 'end',
    });
    setMessages(prev => [...prev, newMessage]);
    setInputMessage("")

    setIsLoading(false)
  }

  return (
    <div className="h-screen w-full relative overflow-hidden">
      <div className="fixed top-0 left-0 right-0 z-20">
        <AgentHeader />
      </div>

      <div className="absolute top-[3rem] bottom-[4.5rem] left-0 right-0 overflow-y-auto px-4 py-2 space-y-2">
        <div className="chat chat-start">
          <div className="chat-image avatar">
            <div className="w-10 rounded-full">
              <img
                alt="Tailwind CSS chat bubble component"
                src="https://img.daisyui.com/images/profile/demo/kenobee@192.webp"
              />
            </div>
          </div>
          <div className="chat-header">
            Obi-Wan Kenobi
            <time className="text-xs opacity-50">12:45</time>
          </div>
          <div className="chat-bubble">You were the Chosen One!</div>
          <div className="chat-footer opacity-50">Delivered</div>
        </div>
        <div className="chat chat-end">
          <div className="chat-image avatar">
            <div className="w-10 rounded-full">
              <img
                alt="Tailwind CSS chat bubble component"
                src="https://img.daisyui.com/images/profile/demo/anakeen@192.webp"
              />
            </div>
          </div>
          <div className="chat-header">
            Anakin
            <time className="text-xs opacity-50">12:46</time>
          </div>
          <div className="chat-bubble">I hate you!</div>
          <div className="chat-footer opacity-50">Seen at 12:46</div>
        </div>
        {messages.map((msg: Message) => <ChatMessage
          key={msg.id}
          position={msg.position}
          avatarUrl={msg.avatarUrl}
          name={msg.name}
          time={msg.time}
          message={msg.content} />)}
      </div>

      <div className="fixed bottom-0 left-0 right-0">
        <MessageInput inputMessage={inputMessage} setInputMessage={setInputMessage} handleSend={handleSend} isLoading={isLoading} />
      </div>
    </div>
  );
}
