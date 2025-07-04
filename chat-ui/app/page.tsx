"use client"

import { useState } from "react"
import MessageInput from "./components/MessageInput"
import AgentHeader from "./components/AgentHeader"
import ChatMessage from "./components/ChatMessage"

export default function Home() {
  const [inputMessage, setInputMessage] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  function sendMessage() {
    setIsLoading(true)

    console.log(inputMessage)
    setInputMessage("")

    setIsLoading(false)
  }

  return (
    <div className="h-screen w-full relative overflow-hidden">
      <div className="fixed top-0 left-0 right-0 z-20">
        <AgentHeader />
      </div>
      
      <div className="absolute top-[3rem] bottom-[4.5rem] left-0 right-0 overflow-y-auto px-4 py-2 space-y-2">
        <ChatMessage position="start" avatarUrl="https://img.daisyui.com/images/profile/demo/kenobee@192.webp" name="AI" time="" message="I'm AI" />
        <ChatMessage position="end" avatarUrl="https://img.daisyui.com/images/profile/demo/anakeen@192.webp" name="Me" time="" message="I'm user" />
        <ChatMessage position="start" avatarUrl="https://img.daisyui.com/images/profile/demo/kenobee@192.webp" name="AI" time="" message="I'm AI" />
        <ChatMessage position="end" avatarUrl="https://img.daisyui.com/images/profile/demo/anakeen@192.webp" name="Me" time="" message="I'm user" />
        <ChatMessage position="start" avatarUrl="https://img.daisyui.com/images/profile/demo/kenobee@192.webp" name="AI" time="" message="I'm AI" />
        <ChatMessage position="end" avatarUrl="https://img.daisyui.com/images/profile/demo/anakeen@192.webp" name="Me" time="" message="I'm user" />
        <ChatMessage position="start" avatarUrl="https://img.daisyui.com/images/profile/demo/kenobee@192.webp" name="AI" time="" message="I'm AI" />
        <ChatMessage position="end" avatarUrl="https://img.daisyui.com/images/profile/demo/anakeen@192.webp" name="Me" time="" message="I'm user" />
        <ChatMessage position="start" avatarUrl="https://img.daisyui.com/images/profile/demo/kenobee@192.webp" name="AI" time="" message="I'm AI" />
        <ChatMessage position="end" avatarUrl="https://img.daisyui.com/images/profile/demo/anakeen@192.webp" name="Me" time="" message="I'm user" />
        <ChatMessage position="start" avatarUrl="https://img.daisyui.com/images/profile/demo/kenobee@192.webp" name="AI" time="" message="I'm AI" />
        <ChatMessage position="end" avatarUrl="https://img.daisyui.com/images/profile/demo/anakeen@192.webp" name="Me" time="" message="I'm user" />
        <ChatMessage position="start" avatarUrl="https://img.daisyui.com/images/profile/demo/kenobee@192.webp" name="AI" time="" message="I'm AI" />
        <ChatMessage position="end" avatarUrl="https://img.daisyui.com/images/profile/demo/anakeen@192.webp" name="Me" time="" message="I'm user" />
      </div>
      
      <div className="fixed bottom-0 left-0 right-0">
        <MessageInput inputMessage={inputMessage} setInputMessage={setInputMessage} sendMessage={sendMessage} isLoading={isLoading}/>
      </div>
    </div>
  );
}
