// news-image-20261124 entry: "Sum up 24 November's world news in one image".
//
// The poster beside this file (entry.png, a 1024x1024 newspaper front page
// drawn at build time by make_poster.py) is the whole entry. This program's
// only job is to place those exact bytes at the output entry.png in the
// grader's sandbox, where MAKEFUN_OUTPUT_DIR stands in for /output:
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// It does no drawing at run time — the grading sandbox is Node-only with a
// read-only repository, so rendering there would fail — and the two grading
// runs therefore produce the identical file, byte for byte.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

function posterSource(): string {
  return join(dirname(fileURLToPath(import.meta.url)), "entry.png");
}

function placePoster(): void {
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  mkdirSync(outDir, { recursive: true });
  copyFileSync(posterSource(), join(outDir, "entry.png"));
}

placePoster();
