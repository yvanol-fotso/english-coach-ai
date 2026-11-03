export const topics = [
  { id: 'day', text: "Let's talk about my day." },
  { id: 'news', text: "I'd like to talk about the news today." },
  { id: 'sport', text: "Let's talk about sport, especially football." },
  { id: 'politics', text: "I'd like to discuss a political topic. Ask me what I think." },
  { id: 'work', text: "Let's talk about my work." },
  { id: 'family', text: "Let's talk about my family and friends." },
  { id: 'movies', text: "Let's talk about movies and series." },
  { id: 'travel', text: "Let's talk about travel and places I know." }
] as const;

export const situations = [
  { id: 'meeting', text: "Hi! It's nice to meet you." },
  { id: 'daily', text: "Hello! I'd like to practise a real-life situation." },
  { id: 'interview', text: "Hello, I'm ready for my PhD interview." },
  { id: 'science', text: "Hi! Let's talk about my research." }
] as const;

export const levels = ['A0', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2'] as const;
