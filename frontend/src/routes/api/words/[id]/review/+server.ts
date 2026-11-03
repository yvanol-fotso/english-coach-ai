import { forward } from '$lib/server/backend';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = (event) => forward(event, `/words/${event.params.id}/review`);
