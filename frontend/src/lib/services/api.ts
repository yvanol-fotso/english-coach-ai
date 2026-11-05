import { preferences } from '$lib/stores/preferences.svelte';
import type {
  ActivityOut,
  CallSummary,
  ChatEvent,
  ChatRequest,
  ConversationDetail,
  CorrectionResult,
  DrillSet,
  Exercise,
  Explanation,
  Level,
  Lesson,
  PracticeKind,
  QuickAnswer,
  ReviewGrade,
  SavedWord,
  Skill,
  TranslationResult
} from '$lib/types';

export class ApiError extends Error {
  constructor(public code: string, message = '') {
    super(message || code);
  }
}

export const codeOf = (error: unknown): string => (error instanceof ApiError ? error.code : 'unknown');
export const isAbort = (error: unknown): boolean => error instanceof DOMException && error.name === 'AbortError';

async function failure(res: Response): Promise<ApiError> {
  const body = await res.json().catch(() => null);
  return new ApiError(body?.code ?? 'unknown', body?.detail);
}

async function request(path: string, init: RequestInit): Promise<Response> {
  let res: Response;
  try {
    res = await fetch(`/api/${path}`, init);
  } catch (error) {
    if (isAbort(error)) throw error;
    throw new ApiError('network');
  }
  if (!res.ok) throw await failure(res);
  return res;
}

const json = (body: unknown): RequestInit => ({
  method: 'POST',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify(body)
});

const post = async <T>(path: string, body: unknown): Promise<T> => (await request(path, json(body))).json();
const context = () => ({ ui_language: preferences.lang, target: preferences.target });

export const translate = (text: string, source: 'auto' | 'native' | 'target') =>
  post<TranslationResult>('translate', { text, source, ...context() });

export const correct = (text: string, level: Level) => post<CorrectionResult>('correct', { text, level, ...context() });
export const explain = (term: string, level: Level) => post<Explanation>('explain', { term, level, ...context() });
export const ask = (question: string, level: Level, detail: 'short' | 'full') =>
  post<QuickAnswer>('ask', { question, level, detail, ...context() });

export const generateExercise = (kind: PracticeKind, level: Level, topic: string) =>
  post<Exercise>('practice', { kind, level, topic: topic || null, ...context() });

export const generateDrill = (kind: 'pronunciation' | 'dictation', level: Level, topic: string, count = 5) =>
  post<DrillSet>('drills', { kind, level, topic: topic || null, count, target: preferences.target });

export const getLesson = (unitId: string) => post<Lesson>(`course/${unitId}/lesson`, context());
export const completeLesson = async (unitId: string, score: number) =>
  void (await request(`course/${unitId}/complete`, json({ target: preferences.target, score })));

export const getCallSummary = (conversationId: number) =>
  post<CallSummary>(`conversations/${conversationId}/summary`, { ui_language: preferences.lang });

export const logActivity = (skill: Skill, score: number, payload: Record<string, unknown>) =>
  post<ActivityOut>('activities', { skill, score, payload });

export const reviewWord = async (id: number, grade: ReviewGrade) => void (await request(`words/${id}/review`, json({ grade })));
export const saveWord = (word: Explanation) => post<SavedWord>('words', { ...word, language: preferences.target });
export const removeWord = async (id: number) => void (await request(`words/${id}`, { method: 'DELETE' }));

export const getConversation = async (id: number): Promise<ConversationDetail> =>
  (await request(`conversations/${id}`, { method: 'GET' })).json();
export const deleteConversation = async (id: number) => void (await request(`conversations/${id}`, { method: 'DELETE' }));

async function* readLines(res: Response): AsyncGenerator<Record<string, any>> {
  if (!res.body) throw new ApiError('unknown');
  const reader = res.body.pipeThrough(new TextDecoderStream()).getReader();
  let buffer = '';
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += value;
    const lines = buffer.split('\n');
    buffer = lines.pop() ?? '';
    for (const line of lines) {
      if (!line) continue;
      const event = JSON.parse(line);
      if (event.error) throw new ApiError(event.error);
      yield event;
    }
  }
}

export async function* streamChat(body: ChatRequest, signal: AbortSignal): AsyncGenerator<ChatEvent> {
  const res = await request('chat', { ...json({ ...body, ...context() }), signal });
  for await (const event of readLines(res)) {
    if (event.conversation) yield { type: 'conversation', id: event.conversation };
    if (event.correction) yield { type: 'correction', data: event.correction };
    if (event.token) yield { type: 'token', text: event.token };
  }
}

export async function* streamTool(
  id: string,
  body: { input: string; options: Record<string, string>; level: Level },
  signal: AbortSignal
): AsyncGenerator<string> {
  const res = await request(`tools/${id}`, { ...json({ ...body, ...context() }), signal });
  for await (const event of readLines(res)) if (event.token) yield event.token as string;
}
