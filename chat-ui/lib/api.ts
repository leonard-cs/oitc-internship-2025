// lib/api.ts
import { Message } from '@/types/message';

export async function fetchMessages(): Promise<Message[]> {
  const res = await fetch('/api/messages');
  if (!res.ok) throw new Error('Failed to fetch messages');
  return res.json();
}

export async function sendMessage(message: Omit<Message, 'id' | 'time'>): Promise<Message> {
  const res = await fetch('/api/messages', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(message),
  });
  if (!res.ok) throw new Error('Failed to send message');
  return res.json();
}
