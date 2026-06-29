#!/usr/bin/env node

const { spawnSync } = require("child_process");
const path = require("path");

const lynsePy = path.resolve(__dirname, "..", "lynse.py");
const userArgs = process.argv.slice(2);

const candidates = process.platform === "win32"
  ? [
      { command: "python", args: [lynsePy, ...userArgs] },
      { command: "py", args: ["-3", lynsePy, ...userArgs] },
      { command: "python3", args: [lynsePy, ...userArgs] },
    ]
  : [
      { command: "python3", args: [lynsePy, ...userArgs] },
      { command: "python", args: [lynsePy, ...userArgs] },
    ];

for (const candidate of candidates) {
  const result = spawnSync(candidate.command, candidate.args, { stdio: "inherit" });

  if (result.error && result.error.code === "ENOENT") {
    continue;
  }

  if (result.error) {
    console.error(`Error: failed to run ${candidate.command}: ${result.error.message}`);
    process.exit(1);
  }

  if (result.signal) {
    process.kill(process.pid, result.signal);
  }

  process.exit(result.status ?? 0);
}

console.error("Error: Python 3.8+ was not found. Install Python, then retry.");
process.exit(1);
