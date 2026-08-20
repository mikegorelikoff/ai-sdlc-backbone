#!/usr/bin/env node
import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { spawnSync } from "node:child_process";
import { pathToFileURL } from "node:url";

const PRODUCT = "ai-sdlc-backbone";
const INSTALLER_VERSION = "1.0.0";
const ERROR_CODES = new Set(["INVALID_LICENSE", "EXPIRED_LICENSE", "REVOKED_LICENSE", "VERSION_NOT_ALLOWED", "INSTALL_LIMIT_REACHED", "UNSUPPORTED_PLATFORM", "RELEASE_NOT_FOUND"]);

export function platformId() {
  const arch = process.arch === "x64" ? "x64" : process.arch === "arm64" ? "arm64" : process.arch;
  return `${process.platform}-${arch}`;
}

export function safeEntryName(name) {
  const normalized = name.replaceAll("\\", "/");
  if (normalized.startsWith("/") || /^[A-Za-z]:/.test(normalized) || normalized.split("/").includes("..") || normalized.includes("\0")) throw new Error("Installation aborted: unsafe artifact path.");
  return normalized;
}

export function validateInstallResponse(value, apiOrigin) {
  const required = ["product", "version", "download_url", "expires_in", "sha256", "artifact"];
  if (!value || required.some((key) => !(key in value)) || value.product !== PRODUCT || !/^\d+\.\d+\.\d+$/.test(value.version) || !Number.isInteger(value.expires_in) || value.expires_in <= 0 || value.expires_in > 900 || !/^[0-9a-f]{64}$/.test(value.sha256)) throw new Error("Installation aborted: licensing response is invalid.");
  const download = new URL(value.download_url);
  if (download.origin !== apiOrigin || !/^ai-sdlc-backbone-[0-9]+\.[0-9]+\.[0-9]+\.tar\.gz$/.test(value.artifact)) throw new Error("Installation aborted: licensing response is invalid.");
  return value;
}

export async function sha256(file) {
  const hash = crypto.createHash("sha256");
  for await (const chunk of fs.createReadStream(file)) hash.update(chunk);
  return hash.digest("hex");
}

export async function verifyArtifact(file, expected) {
  if (await sha256(file) !== expected) throw new Error("Installation aborted: artifact integrity verification failed.");
}

async function promptSecret() {
  if (!process.stdin.isTTY || !process.stderr.isTTY) throw new Error("AI_SDLC_LICENSE_KEY is required in non-interactive mode.");
  process.stderr.write("License key: ");
  process.stdin.setRawMode(true);
  process.stdin.resume();
  process.stdin.setEncoding("utf8");
  return await new Promise((resolve, reject) => {
    let value = "";
    const done = () => { process.stdin.setRawMode(false); process.stdin.pause(); process.stderr.write("\n"); resolve(value); };
    process.stdin.on("data", (key) => {
      if (key === "\u0003") reject(new Error("Installation cancelled."));
      else if (key === "\r" || key === "\n") done();
      else if (key === "\u007f") value = value.slice(0, -1);
      else value += key;
    });
  });
}

async function download(url, destination) {
  const response = await fetch(url, { redirect: "error", signal: AbortSignal.timeout(60000) });
  if (!response.ok || !response.body) throw new Error("Installation aborted: artifact download failed.");
  const declaredSize = Number(response.headers.get("content-length") || "0");
  if (!Number.isFinite(declaredSize) || declaredSize < 0 || declaredSize > 100 * 1024 * 1024) throw new Error("Installation aborted: artifact exceeds size limit.");
  const stream = fs.createWriteStream(destination, { flags: "wx", mode: 0o600 });
  try {
    let size = 0;
    for await (const chunk of response.body) {
      size += chunk.length;
      if (size > 100 * 1024 * 1024) throw new Error("Installation aborted: artifact exceeds size limit.");
      if (!stream.write(chunk)) await new Promise((resolve) => stream.once("drain", resolve));
    }
    await new Promise((resolve, reject) => stream.end((error) => error ? reject(error) : resolve()));
  } catch (error) {
    stream.destroy();
    throw error;
  }
}

async function extract(archive, destination) {
  const tar = await import("tar");
  await tar.t({ file: archive, onentry(entry) { safeEntryName(entry.path); if (!["File", "Directory"].includes(entry.type)) throw new Error("Installation aborted: unsafe artifact member."); } });
  await tar.x({ file: archive, cwd: destination, strict: true, preservePaths: false, filter(entryPath, entry) { safeEntryName(entryPath); return ["File", "Directory"].includes(entry.type); } });
}

function parseArgs(argv) {
  const result = { profile: "codex-project", projectRoot: process.cwd(), requestedVersion: "latest", skillsRoot: null };
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === "--help" || value === "-h") {
      console.log("Usage: ai-sdlc-backbone [--profile PROFILE] [--project-root PATH] [--skills-root PATH] [--version X.Y.Z|latest]");
      return null;
    }
    if (value === "--profile") result.profile = argv[++index];
    else if (value === "--project-root") result.projectRoot = path.resolve(argv[++index]);
    else if (value === "--skills-root") result.skillsRoot = argv[++index];
    else if (value === "--version") result.requestedVersion = argv[++index];
    else throw new Error(`Unknown option: ${value}`);
  }
  if (!new Set(["codex-project", "claude-code-project", "agent-project"]).has(result.profile)) throw new Error("Unsupported profile.");
  if (result.profile === "agent-project" && !result.skillsRoot) throw new Error("--skills-root is required for agent-project.");
  return result;
}

export async function main(argv = process.argv.slice(2)) {
  const options = parseArgs(argv);
  if (options === null) return;
  const api = new URL(process.env.AI_SDLC_LICENSE_API || "https://licenses.ai-sdlc.dev");
  const licenseKey = process.env.AI_SDLC_LICENSE_KEY || await promptSecret();
  console.log("AI-SDLC Backbone Installer");
  const response = await fetch(new URL("/v1/install", api), { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ license_key: licenseKey, installer_version: INSTALLER_VERSION, requested_version: options.requestedVersion, platform: platformId() }), signal: AbortSignal.timeout(15000) });
  const payload = await response.json().catch(() => null);
  if (!response.ok) {
    const code = payload?.error?.code;
    throw new Error(ERROR_CODES.has(code) ? `Installation aborted: ${code}.` : "Installation aborted: license validation failed.");
  }
  const grant = validateInstallResponse(payload, api.origin);
  console.log(`✓ License valid\n✓ Version: ${grant.version}`);
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "ai-sdlc-install-"));
  try {
    const archive = path.join(temporary, grant.artifact);
    await download(grant.download_url, archive);
    console.log("✓ Downloaded");
    await verifyArtifact(archive, grant.sha256);
    console.log("✓ SHA256 verified");
    await extract(archive, temporary);
    const packageRoot = path.join(temporary, `${PRODUCT}-${grant.version}`);
    const installArgs = [path.join(packageRoot, "installer/install.py"), options.profile, "--project-root", options.projectRoot];
    if (options.skillsRoot) installArgs.push("--skills-root", options.skillsRoot);
    const command = spawnSync(process.env.AI_SDLC_PYTHON || "python3", installArgs, { stdio: "inherit" });
    if (command.status !== 0) throw new Error("Installation aborted: controlled install failed.");
    const skillsRoot = options.skillsRoot || (options.profile === "codex-project" ? ".agents/skills" : ".claude/skills");
    const verify = path.join(skillsRoot, "ai-sdlc-shared-runtime/scripts/ai_sdlc_install_record.py");
    console.log(`✓ Installed\n\nAI-SDLC Backbone ${grant.version} installed.\nVerify from the project root: ${process.env.AI_SDLC_PYTHON || "python3"} ${verify}`);
  } finally { fs.rmSync(temporary, { recursive: true, force: true }); }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) main().catch((error) => { console.error(error.message); process.exitCode = 1; });
