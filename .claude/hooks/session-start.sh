#!/bin/bash
# Prepares the playback-notes skill in Claude Code cloud sessions:
# installs Node.js 24 (the skill needs 24.15+) and the skill's npm packages.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-.}"

NODE_VERSION=v24.22.1
NODE_DIR=/opt/node-$NODE_VERSION

# Node.js 24, outside the repository, only if missing
if [ ! -x "$NODE_DIR/bin/node" ]; then
  tmp="$(mktemp -d)"
  curl -fsSL "https://nodejs.org/dist/$NODE_VERSION/node-$NODE_VERSION-linux-x64.tar.xz" -o "$tmp/node.tar.xz"
  mkdir -p "$NODE_DIR"
  tar -xJf "$tmp/node.tar.xz" -C "$NODE_DIR" --strip-components=1
  rm -rf "$tmp"
fi
export PATH="$NODE_DIR/bin:$PATH"

# The skill's npm packages, only if its manifest or this script changed
SKILL_DIR=.claude/skills/playback-notes
hashes="$SKILL_DIR/node_modules/.session-start.sha256"
if ! sha256sum --check --status "$hashes" 2>/dev/null; then
  rm -f "$hashes"
  (cd "$SKILL_DIR" && npm ci --no-audit --no-fund)
  sha256sum .claude/hooks/session-start.sh "$SKILL_DIR/package.json" "$SKILL_DIR/package-lock.json" > "$hashes" || rm -f "$hashes"
fi

# Put Node.js 24 first on PATH for the rest of the session
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo "export PATH=\"$NODE_DIR/bin:\$PATH\"" >> "$CLAUDE_ENV_FILE"
fi
