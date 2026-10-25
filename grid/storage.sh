#!/bin/bash
# Carrying out a merged storage request on the grid (tools/storage.py, tools/retire.py; the thread
# "Check frozen manifest job", 2026-10-24). The planner turns the textbook artifact's selection
# into a request under storage/requests/, which the owner merges; that merge is his word for every
# set it names, and this file is what the grid does with it. Every job is queued by hpcworker's
# `job submit`, class batch, as grid/freeze.sh's are.
#
#   bash storage.sh apply STAMP       the merged request storage/requests/STAMP.json: one job that
#                                     plans each retirement it names (tools/retire.py plan), and the
#                                     fetch word of each set it fetches, for the owner to press;
#                                     a move waits for the home's path (STORAGE_HOME)
#   bash storage.sh plan STAMP        inside that job: each retirement's plan, written to plans/
#   bash storage.sh retire STAMP      one job that carries out the request's retirements whose plans
#                                     list files (tools/retire.py delete); sent by the owner's press
#   bash storage.sh delete STAMP      inside that job: each retirement, RETIRED.json written beside
#                                     the freeze and a copy kept under plans/ for report
#   bash storage.sh survey            one read-only job that sizes the whole volume by folder
#                                     (tools/survey.py): the datasets with their masks apart, and
#                                     the masks, untracked data, runs, jobs and the rest outside them
#   bash storage.sh measure           inside that job: the survey, written to survey.json
#   bash storage.sh status            the jobs, the plans so far and the home's reading
#   bash storage.sh home              the home's size and use, read with df, into home.json
#   bash storage.sh report            the plans' counts, the home's reading and the survey, sent to the branch
#                                     storage-report of spine-datasets as one commit with no parent,
#                                     through the account's own gh, as freeze report does
#
# A plan lists what a retirement would delete and keeps the freeze, the labels and the metadata;
# it deletes nothing. The owner allowed on 2026-10-24 that a merged request deletes a set's images
# through the grid gate, narrowly: retire deletes only what a plan listed, after tools/retire.py has
# run the same checks again on the folder as it is and found the same list, and it is a word of
# its own, sent after the plans have been reported, so what goes is seen before it goes.
#
# The grid gate's words (hpcworker's tools/grid_gate.sh) fetch tools/retire.py, tools/freeze.py,
# this file and the request at the head of the default branch into code/, so only a merged request
# is ever read, and nobody types these.
#
#SBATCH --time=4:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
set -euo pipefail

PROJECT=spine-datasets
JOB=storage
HERE=$(cd "$(dirname "$0")" && pwd)
if [ -z "${STORAGE_DIR:-}" ] && [ "$(basename "$HERE")" = code ]; then STORAGE_DIR=$(dirname "$HERE"); fi
HOME_DIR=${STORAGE_DIR:-/rs/rs_grp_oschome/$USER/spine-datasets-storage}
HPCW=${HPCWORKER:-$HOME/hpcworker/framework/bin/hpcworker}
RETIRE=$HOME_DIR/code/retire.py
REPO=OpenSpineConsortium/spine-datasets
REPORT_BRANCH=storage-report
STAMP_SHAPE='^[0-9]{8}T[0-9]{6}Z$'

python_bin() {
  for candidate in python3.12 python3.11 python3.10 python3.9 python3.8 python3 ; do
    if command -v "$candidate" >/dev/null 2>&1; then echo "$candidate"; return; fi
  done
  echo "no python3 on $(hostname -s)" >&2; exit 2
}

hpcw() {
  [ -f "$HPCW" ] || { echo "no hpcworker at $HPCW" >&2; return 2; }
  bash "$HPCW" "$@"
}

request_of() { # STAMP: the merged request's path, or a refusal
  [[ "${1:-}" =~ $STAMP_SHAPE ]] || { echo "STAMP is the request's time, as 20261024T210000Z" >&2; exit 2; }
  local file=$HOME_DIR/code/requests/$1.json
  [ -f "$file" ] || { echo "no merged request $1 in $HOME_DIR/code/requests" >&2; exit 2; }
  echo "$file"
}

case "${1:-}" in
  apply)
    file=$(request_of "${2:-}")
    [ -f "$RETIRE" ] && [ -f "$HOME_DIR/code/freeze.py" ] && [ -f "$HOME_DIR/code/storage.sh" ] \
      || { echo "copy tools/retire.py, tools/freeze.py and grid/storage.sh into $HOME_DIR/code first"; exit 2; }
    py=$(python_bin)
    actions=$("$py" "$RETIRE" actions "$file")
    retirements=$(printf '%s\n' "$actions" | awk -F'\t' '$1 == "retire"' | wc -l)
    printf '%s\n' "$actions" | awk -F'\t' '$1 == "fetch" { print "fetch " $2 ": the owner presses the word schwingnet-fetch-" $2 ", which reads its exact size first" }'
    printf '%s\n' "$actions" | awk -F'\t' '$1 == "move" { print "move " $2 " to " $3 ": waits until the home'"'"'s path is set (STORAGE_HOME)" }'
    if [ "$retirements" -eq 0 ]; then echo "no retirement to plan"; exit 0; fi
    mkdir -p "$HOME_DIR/applied" "$HOME_DIR/plans"
    if [ -f "$HOME_DIR/applied/$2" ]; then
      echo "request $2 was planned already ($(cat "$HOME_DIR/applied/$2")); not queueing again"; exit 0
    fi
    if squeue -h -u "$USER" -n "$PROJECT-$JOB" -o %i 2>/dev/null | grep -q .; then
      echo "a storage job is already queued or running; not queueing another"; exit 0
    fi
    echo "queueing one job to plan $retirements retirements of request $2; it deletes nothing"
    hpcw job submit --project "$PROJECT" --name "$JOB" --class batch --dir "$HOME_DIR" \
      -- "$HOME_DIR/code/storage.sh" plan "$2"
    date -u +%FT%TZ > "$HOME_DIR/applied/$2"
    ;;
  plan)
    [ -n "${SLURM_JOB_ID:-}" ] || { echo "plan is for inside a job; use apply"; exit 2; }
    file=$(request_of "${2:-}")
    py=$(python_bin)
    echo "$(date -u +%FT%TZ) storage job $SLURM_JOB_ID on $(hostname -s), request $2"
    status=0
    while IFS=$'\t' read -r kind ident _place folder tree; do
      [ "$kind" = retire ] || continue
      "$py" "$RETIRE" plan "$folder" --id "$ident" --tree "$tree" --out "$HOME_DIR/plans" || status=1
    done < <("$py" "$RETIRE" actions "$file")
    exit "$status"
    ;;
  retire)
    file=$(request_of "${2:-}")
    py=$(python_bin)
    ready=0
    while IFS=$'\t' read -r kind ident _place _folder _tree; do
      [ "$kind" = retire ] || continue
      if [ -s "$HOME_DIR/plans/$ident.delete" ] && grep -q '"problems": \[\]' "$HOME_DIR/plans/$ident.json" 2>/dev/null; then
        ready=$((ready + 1))
      else
        echo "$ident: no plan that lists files; send storage apply $2 first, or read its problems"
      fi
    done < <("$py" "$RETIRE" actions "$file")
    [ "$ready" -gt 0 ] || { echo "nothing to retire"; exit 1; }
    if squeue -h -u "$USER" -n "$PROJECT-$JOB" -o %i 2>/dev/null | grep -q .; then
      echo "a storage job is already queued or running; not queueing another"; exit 0
    fi
    echo "queueing one job to retire $ready sets of request $2"
    hpcw job submit --project "$PROJECT" --name "$JOB" --class batch --dir "$HOME_DIR" \
      -- "$HOME_DIR/code/storage.sh" delete "$2"
    ;;
  delete)
    [ -n "${SLURM_JOB_ID:-}" ] || { echo "delete is for inside a job; use retire"; exit 2; }
    file=$(request_of "${2:-}")
    py=$(python_bin)
    echo "$(date -u +%FT%TZ) storage job $SLURM_JOB_ID on $(hostname -s), retiring request $2"
    status=0
    while IFS=$'\t' read -r kind ident _place folder tree; do
      [ "$kind" = retire ] || continue
      "$py" "$RETIRE" delete "$folder" --id "$ident" --tree "$tree" --plans "$HOME_DIR/plans" --request "$2" || status=1
    done < <("$py" "$RETIRE" actions "$file")
    exit "$status"
    ;;
  survey)
    [ -f "$HOME_DIR/code/survey.py" ] && [ -f "$HOME_DIR/code/freeze-plan.tsv" ] && [ -f "$HOME_DIR/code/storage.sh" ] \
      || { echo "copy tools/survey.py, grid/freeze-plan.tsv and grid/storage.sh into $HOME_DIR/code first"; exit 2; }
    if squeue -h -u "$USER" -n "$PROJECT-$JOB" -o %i 2>/dev/null | grep -q .; then
      echo "a storage job is already queued or running; not queueing another"; exit 0
    fi
    echo "queueing one read-only job to size the volume by folder; it changes nothing"
    hpcw job submit --project "$PROJECT" --name "$JOB" --class batch --dir "$HOME_DIR" \
      -- "$HOME_DIR/code/storage.sh" measure
    ;;
  measure)
    [ -n "${SLURM_JOB_ID:-}" ] || { echo "measure is for inside a job; use survey"; exit 2; }
    py=$(python_bin)
    echo "$(date -u +%FT%TZ) storage job $SLURM_JOB_ID on $(hostname -s), survey of the volume"
    "$py" "$HOME_DIR/code/survey.py" run --plan "$HOME_DIR/code/freeze-plan.tsv" --out "$HOME_DIR/survey.json" \
      ${SURVEY_ROOT:+--root "$SURVEY_ROOT"} ${SURVEY_FLOOR_GB:+--floor-gb "$SURVEY_FLOOR_GB"}
    ;;
  home)
    [ -n "${STORAGE_HOME:-}" ] || { echo "the home's path is not set: STORAGE_HOME names the folder that holds 4 TB"; exit 2; }
    [ -d "$STORAGE_HOME" ] || { echo "the home's path is not a folder"; exit 2; }
    mkdir -p "$HOME_DIR"
    read -r size used < <(df -B1 --output=size,used "$STORAGE_HOME" | tail -1)
    printf '{"format": "spine-datasets/home 1", "read_at": "%s", "size_bytes": %s, "used_bytes": %s}\n' \
      "$(date -u +%FT%TZ)" "$size" "$used" > "$HOME_DIR/home.json"
    cat "$HOME_DIR/home.json"
    ;;
  status)
    squeue -u "$USER" -n "$PROJECT-$JOB" || true
    for plan in $(ls -t "$HOME_DIR"/plans/*.json 2>/dev/null | head -40); do
      echo "plan $(basename "$plan" .json): $(tr -d ' \n' < "$plan")"
    done
    [ -f "$HOME_DIR/home.json" ] && echo "home: $(cat "$HOME_DIR/home.json")"
    [ -f "$HOME_DIR/survey.json" ] && echo "survey: $(grep -o '"read_at": "[^"]*"' "$HOME_DIR/survey.json")"
    hpcw job status --project "$PROJECT" --last 4 || true
    ;;
  report)
    command -v gh >/dev/null 2>&1 || { echo "no gh on this account's path"; exit 2; }
    py=$(python_bin)
    tree_body=$HOME_DIR/report-tree.json
    "$py" "$RETIRE" bundle "$HOME_DIR/plans" > "$tree_body.tmp" || echo '{"tree": []}' > "$tree_body.tmp"
    for reading in home survey; do
      [ -f "$HOME_DIR/$reading.json" ] || continue
      "$py" - "$tree_body.tmp" "$HOME_DIR/$reading.json" "storage/$reading.json" <<'EOF'
import json, sys
body, source, path = sys.argv[1], sys.argv[2], sys.argv[3]
with open(body) as handle:
    tree = json.load(handle)
with open(source) as handle:
    reading = json.load(handle)
tree["tree"].append({"path": path, "mode": "100644", "type": "blob",
                     "content": json.dumps(reading, indent=1, sort_keys=True) + "\n"})
with open(body, "w") as handle:
    json.dump(tree, handle)
EOF
    done
    mv -f "$tree_body.tmp" "$tree_body"
    grep -q '"path"' "$tree_body" || { echo "nothing to report"; exit 1; }
    tree=$(gh api -X POST "repos/$REPO/git/trees" --input "$tree_body" --jq .sha < /dev/null)
    [[ "$tree" =~ ^[0-9a-f]{40}$ ]] || { echo "GitHub took no tree"; exit 1; }
    commit=$(gh api -X POST "repos/$REPO/git/commits" -f message="The storage plans, the home's reading and the survey, as grid/storage.sh report found them" \
      -f tree="$tree" --jq .sha < /dev/null)
    [[ "$commit" =~ ^[0-9a-f]{40}$ ]] || { echo "GitHub took no commit"; exit 1; }
    if gh api "repos/$REPO/git/ref/heads/$REPORT_BRANCH" --jq .object.sha < /dev/null > /dev/null 2>&1; then
      gh api -X PATCH "repos/$REPO/git/refs/heads/$REPORT_BRANCH" -f sha="$commit" -F force=true --jq .object.sha < /dev/null > /dev/null
    else
      gh api -X POST "repos/$REPO/git/refs" -f ref="refs/heads/$REPORT_BRANCH" -f sha="$commit" --jq .object.sha < /dev/null > /dev/null
    fi || { echo "GitHub did not move $REPORT_BRANCH"; exit 1; }
    echo "reported to $REPORT_BRANCH at ${commit:0:12}"
    ;;
  *)
    echo "usage: storage.sh apply STAMP | plan STAMP | retire STAMP | delete STAMP | survey | measure | status | home | report"; exit 2
    ;;
esac
