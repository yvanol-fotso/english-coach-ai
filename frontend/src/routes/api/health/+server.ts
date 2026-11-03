import { json } from '@sveltejs/kit';
import { getHealth } from '$lib/server/backend';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ fetch }) => json(await getHealth(fetch));
