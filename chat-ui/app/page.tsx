"use client"

import { useState } from "react"
import MessageInput from "./components/MessageInput"

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
    <MessageInput inputMessage={inputMessage} setInputMessage={setInputMessage} sendMessage={sendMessage} isLoading={isLoading}/>
  );
}
