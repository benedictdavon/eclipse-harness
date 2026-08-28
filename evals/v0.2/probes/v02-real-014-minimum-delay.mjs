// Dependency-free behavioural probe for the frozen V02-REAL-014 candidate.
//
// Usage: node --experimental-strip-types <this-file> <candidate-source-root>
// The candidate is a checkout of REAL-TS-NODE at its frozen commit with the
// recorded patch applied. The temporary constants module mirrors the only
// runtime dependency of normalize.ts; all other imports are type-only.

import {mkdtemp, mkdir, readFile, rm, writeFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {pathToFileURL} from 'node:url';

const sourceRoot = process.argv[2];

if (!sourceRoot) {
	throw new Error('pass the candidate source root');
}

const probeRoot = await mkdtemp(join(tmpdir(), 'eclipse-v02-real-014-'));
const source = join(probeRoot, 'source');

try {
	await mkdir(join(source, 'utils'), {recursive: true});
	await mkdir(join(source, 'core'), {recursive: true});
	await writeFile(
		join(source, 'utils', 'normalize.ts'),
		await readFile(join(sourceRoot, 'utils', 'normalize.ts'), 'utf8'),
	);
	await writeFile(
		join(source, 'core', 'constants.js'),
		"export const requestMethods = ['get', 'post', 'put', 'patch', 'head', 'delete', 'query'];\n",
	);

	const {normalizeRetryOptions} = await import(
		pathToFileURL(join(source, 'utils', 'normalize.ts')).href,
	);
	const defaults = normalizeRetryOptions();
	const bounded = normalizeRetryOptions({minimumDelayMs: 500});
	if (defaults.delay(1) !== 300 || bounded.delay(1) !== 500 || bounded.delay(2) !== 600) {
		throw new Error('minimum delay behavior is not preserved');
	}

	try {
		normalizeRetryOptions({minimumDelayMs: -1});
		throw new Error('negative minimumDelayMs was accepted');
	} catch (error) {
		if (error instanceof Error && error.message !== 'retry.minimumDelayMs must be non-negative') {
			throw error;
		}
	}

	console.log('ECLIPSE_ACCEPTANCE_EVIDENCE: PASS');
} finally {
	await rm(probeRoot, {force: true, recursive: true});
}
