export type ChatPosition = 'start' | 'end';

export interface Message {
  id: string;
  position: ChatPosition;
  name: string;
  avatarUrl: string;
  time: string;
  content: string;
}
