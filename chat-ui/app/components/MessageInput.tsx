"use client"

import React from 'react'

interface MessageInputProps {
  inputMessage: string
  setInputMessage: (value: string) => void
  sendMessage: () => void
  isLoading: boolean
}

export default function MessageInput({ inputMessage, setInputMessage, sendMessage, isLoading } : MessageInputProps) {
  return (
    <div className="flex flex-col flex-auto justify-between bg-gray-100 p-6">
      <div className="top-[100vh] flex flex-row items-center h-16 rounded-xl bg-white w-full px-4">
        <div className="flex-grow ml-4">
          <div className="relative w-full">
            <input
              type="text"
              disabled={isLoading}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              className="flex w-full border rounded-xl focus:outline-none focus:border-indigo-300 pl-4 h-10"
            />
          </div>
        </div>
        <div className="ml-4">
          <button className="btn btn-info"
            onClick={sendMessage}
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <span className="loading loading-spinner w-5 h-5" />
                Loading
              </>
            ) : (
              <>
                Send
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="2.5" stroke="currentColor" className="size-[1.2em]">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3 10.5l19-7-7 19-2.69-8.34L3 10.5z" />
                </svg>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  )
}
