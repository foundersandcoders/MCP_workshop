#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/../data"
rm -rf sample_repo
mkdir -p sample_repo && cd sample_repo
git init -q
echo '{"name":"demo","version":"1.0.0"}' > package.json
git add . && git commit -m "chore: init" --author="Alice <alice@example.com>" --date="2025-09-01T10:00:00" >/dev/null
mkdir -p src/api
echo 'export function auth(){ /* TODO: improve */ }' > src/api/auth.ts
git add . && git commit -m "feat(api): add auth" --author="Bob <bob@example.com>" --date="2025-09-05T12:00:00" >/dev/null
echo 'export function users(){ }' > src/api/users.ts
git add . && git commit -m "feat(api): users endpoint" --author="Alice <alice@example.com>" --date="2025-09-10T09:00:00" >/dev/null
