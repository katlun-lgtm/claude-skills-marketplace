#!/usr/bin/env bash
# sync-frontend-design.sh
#
# Sync the local frontend-design skill source into this marketplace repo,
# optionally bump version, commit, tag, and push.
#
# Usage:
#   ./scripts/sync-frontend-design.sh                    # sync + show diff, no commit
#   ./scripts/sync-frontend-design.sh --bump patch       # sync + bump patch + commit + tag
#   ./scripts/sync-frontend-design.sh --bump minor       # bump 0.x.0
#   ./scripts/sync-frontend-design.sh --bump major       # bump x.0.0
#   ./scripts/sync-frontend-design.sh --version 0.3.0    # set explicit version
#   ./scripts/sync-frontend-design.sh --bump patch --push  # full pipeline incl. push
#
# Source:  ~/.claude/skills/frontend-design/  (live install + private repo)
# Dest:    ./plugins/frontend-design/skills/frontend-design/

set -euo pipefail

SOURCE="${HOME}/.claude/skills/frontend-design"
DEST_PLUGIN="plugins/frontend-design"
DEST_SKILL="${DEST_PLUGIN}/skills/frontend-design"
PLUGIN_JSON="${DEST_PLUGIN}/.claude-plugin/plugin.json"
MARKETPLACE_JSON=".claude-plugin/marketplace.json"

# colors
g='\033[32m'; y='\033[33m'; r='\033[31m'; d='\033[2m'; b='\033[1m'; n='\033[0m'

die() { printf "${r}error:${n} %s\n" "$1" >&2; exit 1; }
note() { printf "${d}%s${n}\n" "$1"; }
ok()   { printf "${g}%s${n}\n" "$1"; }

# --- locate marketplace repo root ---
cd "$(dirname "$0")/.."
[[ -f "$MARKETPLACE_JSON" ]] || die "must be run from a marketplace repo (no $MARKETPLACE_JSON)"
[[ -d "$SOURCE" ]] || die "source not found: $SOURCE"

# --- parse args ---
BUMP=""
EXPLICIT_VERSION=""
PUSH=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --bump) BUMP="$2"; shift 2 ;;
    --version) EXPLICIT_VERSION="$2"; shift 2 ;;
    --push) PUSH=1; shift ;;
    -h|--help) sed -n '2,16p' "$0" | sed 's/^# \?//'; exit 0 ;;
    *) die "unknown flag: $1" ;;
  esac
done

[[ -n "$BUMP" && -n "$EXPLICIT_VERSION" ]] && die "use --bump OR --version, not both"
case "${BUMP:-patch}" in patch|minor|major|"") ;; *) die "--bump must be patch|minor|major" ;; esac

# --- bail if marketplace repo has TRACKED uncommitted changes outside the sync targets ---
# (untracked files are fine — won't be touched by sync)
dirty_outside="$(git status --porcelain --untracked-files=no \
  | grep -v -E "^.. (${DEST_SKILL}|${PLUGIN_JSON}|${MARKETPLACE_JSON})" || true)"
if [[ -n "$dirty_outside" ]]; then
  die "marketplace repo has uncommitted tracked changes outside the sync targets — commit or stash first:
$dirty_outside"
fi

# --- sync content (preserves nothing in dest that source doesn't have) ---
note "syncing: $SOURCE/ → $DEST_SKILL/"
mkdir -p "$DEST_SKILL"
rsync -a --delete \
  --exclude='.git' --exclude='.gitignore' --exclude='__pycache__' --exclude='*.pyc' --exclude='.DS_Store' \
  "$SOURCE/" "$DEST_SKILL/"

# --- detect changes ---
git add "$DEST_SKILL" "$PLUGIN_JSON" "$MARKETPLACE_JSON" 2>/dev/null || true
if git diff --cached --quiet -- "$DEST_SKILL"; then
  ok "no content changes in skill source — nothing to sync"
  git reset HEAD >/dev/null 2>&1 || true
  exit 0
fi

# --- show what changed ---
echo
printf "${b}changes in ${DEST_SKILL}:${n}\n"
git diff --cached --stat -- "$DEST_SKILL"
echo

# --- if no bump requested, stop here (dry-run review mode) ---
if [[ -z "$BUMP" && -z "$EXPLICIT_VERSION" ]]; then
  # unstage so a follow-up bump call starts clean
  git reset HEAD -- "$DEST_SKILL" "$PLUGIN_JSON" "$MARKETPLACE_JSON" >/dev/null 2>&1 || true
  printf "${y}sync complete (no version bump).${n} Run with --bump patch|minor|major to commit + tag.\n"
  printf "To discard the synced files: ${d}git checkout -- $DEST_SKILL${n}\n"
  exit 0
fi

# --- compute next version ---
CURRENT="$(jq -r '.version' "$PLUGIN_JSON")"
[[ "$CURRENT" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || die "current version not semver: $CURRENT"

if [[ -n "$EXPLICIT_VERSION" ]]; then
  NEXT="$EXPLICIT_VERSION"
else
  IFS='.' read -r MAJ MIN PAT <<< "$CURRENT"
  case "$BUMP" in
    patch) NEXT="${MAJ}.${MIN}.$((PAT + 1))" ;;
    minor) NEXT="${MAJ}.$((MIN + 1)).0" ;;
    major) NEXT="$((MAJ + 1)).0.0" ;;
  esac
fi
[[ "$NEXT" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || die "computed version invalid: $NEXT"

printf "${b}bump:${n} %s → %s\n" "$CURRENT" "$NEXT"

# --- update plugin.json + marketplace.json ---
tmp="$(mktemp)"
jq --arg v "$NEXT" '.version = $v' "$PLUGIN_JSON" > "$tmp" && mv "$tmp" "$PLUGIN_JSON"
jq --arg v "$NEXT" '(.plugins[] | select(.name=="frontend-design") | .version) = $v' "$MARKETPLACE_JSON" > "$tmp" && mv "$tmp" "$MARKETPLACE_JSON"

# --- validate manifests before committing ---
if ! claude plugin validate . >/dev/null 2>&1; then
  die "marketplace validation failed after bump — aborting"
fi
if ! claude plugin validate "$DEST_PLUGIN" >/dev/null 2>&1; then
  die "plugin validation failed after bump — aborting"
fi
ok "manifests validated"

# --- commit + tag ---
git add "$DEST_SKILL" "$PLUGIN_JSON" "$MARKETPLACE_JSON"
git commit -m "release: frontend-design ${NEXT}

Synced skill source from ~/.claude/skills/frontend-design/
Previous version: ${CURRENT}"

TAG="frontend-design-${NEXT}"
git tag -a "$TAG" -m "frontend-design ${NEXT}"
ok "committed and tagged: $TAG"

# --- push (only if --push) ---
if [[ "$PUSH" -eq 1 ]]; then
  git push origin "$(git symbolic-ref --short HEAD)"
  git push origin "$TAG"
  ok "pushed to origin"
else
  printf "${y}not pushed.${n} Run: ${d}git push origin main && git push origin $TAG${n}\n"
fi
