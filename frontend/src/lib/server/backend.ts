import { json, type Cookies, type RequestEvent } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';
import type { HealthStatus } from '$lib/types';

export const PROFILE_COOKIE = 'ec_profile';
const OFFLINE: HealthStatus = { api: false, ollama: false, model: '', model_ready: false, stt: false, tts: false };

const baseUrl = () => env.BACKEND_URL ?? 'http://127.0.0.1:8000/api/v1';

function headersFor(cookies: Cookies, contentType?: string | null): Headers {
  const headers = new Headers();
  if (contentType) headers.set('content-type', contentType);
  const profile = cookies.get(PROFILE_COOKIE);
  if (profile) headers.set('x-profile', encodeURIComponent(profile));
  return headers;
}

export async function forward({ request, url, cookies }: RequestEvent, path: string): Promise<Response> {
  const hasBody = !['GET', 'HEAD', 'DELETE'].includes(request.method);
  try {
    const upstream = await fetch(`${baseUrl()}${path}${url.search}`, {
      method: request.method,
      headers: headersFor(cookies, request.headers.get('content-type')),
      body: hasBody ? await request.arrayBuffer() : undefined,
      signal: request.signal
    });
    return new Response(upstream.status === 204 ? null : upstream.body, {
      status: upstream.status,
      headers: {
        'content-type': upstream.headers.get('content-type') ?? 'application/json',
        'cache-control': 'no-store'
      }
    });
  } catch {
    return json({ code: 'backend_unreachable', detail: 'backend_unreachable' }, { status: 502 });
  }
}

export async function backendGet<T>(cookies: Cookies, path: string): Promise<T | null> {
  try {
    const res = await fetch(`${baseUrl()}${path}`, {
      headers: headersFor(cookies),
      signal: AbortSignal.timeout(5000)
    });
    return res.ok ? ((await res.json()) as T) : null;
  } catch {
    return null;
  }
}

export async function getHealth(fetchFn: typeof fetch): Promise<HealthStatus> {
  try {
    const res = await fetchFn(`${baseUrl()}/health`, { signal: AbortSignal.timeout(4000) });
    return res.ok ? ((await res.json()) as HealthStatus) : OFFLINE;
  } catch {
    return OFFLINE;
  }
}
