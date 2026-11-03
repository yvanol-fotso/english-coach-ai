import { forward } from '$lib/server/backend';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = (event) => forward(event, `/conversations/${event.params.id}`);
export const DELETE: RequestHandler = (event) => forward(event, `/conversations/${event.params.id}`);
