export type ConversationTurn = {
  role: 'user' | 'assistant' | 'system' | 'error';
  text: string;
  imageUrl?: string;
};
