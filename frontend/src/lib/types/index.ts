export type Level = 'A0' | 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2';
export type Language = string;
export type Lang = 'fr' | 'en';
export type Theme = 'system' | 'light' | 'dark';
export type Accent = 'teal' | 'blue' | 'plum' | 'ember';
export type Scenario = string;
export type Feedback = 'inline' | 'off';
export type PracticeKind = 'reading' | 'listening';
export type Skill =
  | 'speaking'
  | 'pronunciation'
  | 'writing'
  | 'reading'
  | 'listening'
  | 'translation'
  | 'vocabulary'
  | 'grammar'
  | 'creative'
  | 'course';
export type Text = { fr: string; en: string };

export interface Prefs {
  lang: Lang;
  theme: Theme;
  accent: Accent;
  target: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  correction?: CorrectionResult | null;
}

export interface ChatRequest {
  opening?: boolean;
  messages: ChatMessage[];
  conversation_id: number | null;
  scenario: Scenario;
  level: Level;
  feedback: Feedback;
}

export type ChatEvent =
  | { type: 'conversation'; id: number }
  | { type: 'correction'; data: CorrectionResult }
  | { type: 'token'; text: string };

export interface TranslationResult {
  source_language: Language;
  target_language: Language;
  translation: string;
  alternatives: string[];
}

export interface Issue {
  original: string;
  correction: string;
  category: 'grammar' | 'vocabulary' | 'spelling' | 'punctuation' | 'style';
  explanation: string;
}

export interface CorrectionResult {
  corrected_text: string;
  issues: Issue[];
  tip: string;
}

export interface Question {
  question: string;
  choices: string[];
  answer_index: number;
  explanation: string;
}

export interface Exercise {
  title: string;
  passage: string;
  questions: Question[];
}

export interface Explanation {
  term: string;
  part_of_speech: string;
  definition: string;
  translation: string;
  examples: string[];
  pronunciation_tip: string;
}

export interface SavedWord extends Explanation {
  language: string;
  id: number;
  created_at: string;
}

export interface ConversationSummary {
  id: number;
  title: string;
  scenario: Scenario;
  level: Level;
  language: string;
  updated_at: string;
  message_count: number;
}

export interface ConversationDetail extends ConversationSummary {
  messages: (ChatMessage & { created_at: string })[];
}

export interface ActivityOut {
  id: number;
  skill: Skill;
  score: number | null;
  payload: Record<string, unknown> | null;
  created_at: string;
}

export interface Stats {
  total: number;
  streak: number;
  by_skill: Record<Skill, number>;
  days: { day: string; count: number }[];
}

export interface HealthStatus {
  api: boolean;
  ollama: boolean;
  model: string;
  model_ready: boolean;
  stt: boolean;
  tts: boolean;
}

export interface CatalogTopic {
  id: string;
  label: Text;
  starter: Record<string, string>;
}

export interface CatalogScenario {
  id: string;
  label: Text;
  starter: Record<string, string>;
  chip: boolean;
}

export interface CatalogLanguage {
  code: string;
  native: string;
  locale: string;
  label: Text;
  available: boolean;
}

export interface CatalogUnit {
  id: string;
  title: Text;
  goal: Text;
  level: Level;
}

export interface ToolOption {
  id: string;
  label: Text;
  choices: { id: string; label: Text }[];
}

export interface ToolSpec {
  id: string;
  icon: string;
  skill: Skill;
  title: Text;
  description: Text;
  placeholder: Text;
  options: ToolOption[];
}

export interface Catalog {
  languages: CatalogLanguage[];
  units: CatalogUnit[];
  topics: CatalogTopic[];
  scenarios: CatalogScenario[];
  tools: ToolSpec[];
}

export type ReviewGrade = 'again' | 'hard' | 'good' | 'easy';

export interface DrillSet {
  sentences: string[];
}

export interface QuickAnswer {
  title: string;
  rule: string;
  examples: string[];
  exceptions: string[];
  watch_out: string;
  spoken: string;
}

export interface Phrase {
  text: string;
  meaning: string;
  tip: string;
}

export interface Lesson {
  title: string;
  intro: string;
  phrases: Phrase[];
  dialogue: { speaker: string; text: string; meaning: string }[];
  quiz: Question[];
  tip: string;
}

export interface UnitProgress {
  id: string;
  done: boolean;
  score: number | null;
}

export interface CallSummary {
  summary: string;
  mistakes: { wrong: string; right: string; why: string }[];
  phrases: string[];
  next_step: string;
}
