import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { main, safeEntryName, sha256, validateInstallResponse, verifyArtifact } from "../src/cli.js";

test("response requires same-origin backend grant", () => {
  const valid = { product: "ai-sdlc-harness", version: "4.5.0", download_url: "https://licenses.test/v1/download/token", expires_in: 300, sha256: "a".repeat(64), artifact: "ai-sdlc-harness-4.5.0.tar.gz" };
  assert.equal(validateInstallResponse(valid, "https://licenses.test").version, "4.5.0");
  assert.throws(() => validateInstallResponse({ ...valid, download_url: "https://github.com/private" }, "https://licenses.test"));
});

test("unsafe archive paths fail closed", () => {
  for (const name of ["../secret", "/absolute", "C:\\secret", "safe/../../secret"]) assert.throws(() => safeEntryName(name));
  assert.equal(safeEntryName("ai-sdlc-harness-4.5.0/VERSION"), "ai-sdlc-harness-4.5.0/VERSION");
});

test("sha256 is exact", async () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), "installer-test-"));
  try { const file = path.join(directory, "artifact"); fs.writeFileSync(file, "abc"); assert.equal(await sha256(file), "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"); }
  finally { fs.rmSync(directory, { recursive: true, force: true }); }
});

test("corrupted artifact is rejected before installation", async () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), "installer-corrupt-"));
  try {
    const file = path.join(directory, "artifact.tar.gz");
    fs.writeFileSync(file, "corrupted");
    await assert.rejects(verifyArtifact(file, "0".repeat(64)), /artifact integrity verification failed/);
  } finally { fs.rmSync(directory, { recursive: true, force: true }); }
});

test("help does not contact the licensing service", async () => {
  await main(["--help"]);
});
