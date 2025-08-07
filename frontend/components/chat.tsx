"use client";

import { PreviewMessage, ThinkingMessage } from "@/components/message";
import { ChatInput } from "@/components/chat-input";
import { MultimodalInput } from "@/components/multimodal-input";
import { Overview } from "@/components/overview";
import { useScrollToBottom } from "@/hooks/use-scroll-to-bottom";
import { ToolInvocation } from "ai";
// import { useChat } from "ai/react";
import { toast } from "sonner";
import { useState, useRef } from "react";
import type { Attachment, Message } from "ai";

export interface MyMessage {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  attachments?: Attachment[];
}

// Convert MyMessage to AI SDK Message format for PreviewMessage compatibility
function convertToAIMessage(myMessage: MyMessage): Message {
  return {
    id: myMessage.id,
    role: myMessage.role as "user" | "assistant" | "system",
    content: myMessage.content,
    createdAt: new Date(),
  };
}

export function Chat() {
  const chatId = "001";
  const [messages, setMessages] = useState<Array<MyMessage>>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  // const {
  //   messages,
  //   setMessages,
  //   handleSubmit,
  //   input,
  //   setInput,
  //   append,
  //   isLoading,
  //   stop,
  // } = useChat({
  //   maxSteps: 4,
  //   onError: (error) => {
  //     if (error.message.includes("Too many requests")) {
  //       toast.error(
  //         "You are sending too many messages. Please try again later."
  //       );
  //     }
  //   },
  // });
  const abortControllerRef = useRef<AbortController | null>(null);

  const [messagesContainerRef, messagesEndRef] =
    useScrollToBottom<HTMLDivElement>();

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
  };

  const stop = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      setIsLoading(false);
    }
  };

  const handleSubmit = async (
    messageContent?: string,
    attachments?: Attachment[]
  ) => {
    const content = messageContent || input;
    if (!content.trim()) return;

    const userMessage: MyMessage = {
      id: Date.now().toString(),
      role: "user",
      content: content.trim(),
      attachments: attachments,
    };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);

    // Only clear input if we're using the input field
    if (!messageContent) {
      setInput("");
    }

    setIsLoading(true);
    abortControllerRef.current = new AbortController();

    try {
      const response = await fetch(
        "http://localhost:8000/api/v1/agent/ask_agent",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ user_query: userMessage.content }),
          signal: abortControllerRef.current.signal,
        }
      );

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();
      const assistantMessage: MyMessage = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.answer || "No response received",
      };
      // const assistantMessage: MyMessage = {
      //   id: (Date.now() + 1).toString(),
      //   role: "assistant",
      //   content: "No response received",
      // };

      setMessages([...newMessages, assistantMessage]);
    } catch (error: any) {
      if (error.name === "AbortError") {
        console.log("Request was aborted");
        toast.info("Request cancelled");
      } else {
        console.error("Chat error:", error);
        toast.error(error.message || "Something went wrong");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const append = (message: { role: string; content: string }) => {
    // If it's a user message, set input and trigger submission
    if (message.role === "user") {
      setInput(message.content);
      // Use setTimeout to ensure input is set before submission
      setTimeout(() => {
        handleSubmit(message.content, []);
      }, 10);
    } else {
      // For non-user messages, just add to messages
      const newMessage: MyMessage = {
        id: Date.now().toString(),
        role: message.role as "user" | "assistant" | "system",
        content: message.content,
      };
      setMessages([...messages, newMessage]);
    }
  };

  return (
    <div className="flex flex-col min-w-0 h-[calc(100dvh-52px)] bg-background">
      <div
        ref={messagesContainerRef}
        className="flex flex-col min-w-0 gap-6 flex-1 overflow-y-scroll pt-4"
      >
        {messages.length === 0 && <Overview />}

        {messages.map((message, index) => (
          <PreviewMessage
            key={message.id}
            chatId={chatId}
            message={convertToAIMessage(message)}
            isLoading={isLoading && messages.length - 1 === index}
            attachments={message.attachments}
          />
        ))}

        {isLoading &&
          messages.length > 0 &&
          messages[messages.length - 1].role === "user" && <ThinkingMessage />}

        <div
          ref={messagesEndRef}
          className="shrink-0 min-w-[24px] min-h-[24px]"
        />
      </div>

      <form className="flex mx-auto px-4 bg-background pb-4 md:pb-6 gap-2 w-full md:max-w-3xl">
        <ChatInput
          input={input}
          handleInput={handleInput}
          isLoading={isLoading}
          handleSubmit={handleSubmit}
          append={append}
          messagesLength={messages.length}
          stop={stop}
        />
        {/* <MultimodalInput
          chatId={chatId}
          input={input}
          setInput={setInput}
          // handleSubmit={handleSubmit}
          handleSubmit={submitForm}
          isLoading={isLoading}
          stop={stop}
          messages={messages}
          // setMessages={setMessages}
          setMessages={() => {}}
          append={append}
        /> */}
      </form>
    </div>
  );
}
