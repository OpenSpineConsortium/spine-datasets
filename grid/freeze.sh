#!/bin/bash
# Freezing the sets already on the grid (tools/freeze.py; the thread "Frozen dataset manifests",
# 2026-10-23): each job reads every file of its share of the sets once, writes FROZEN.json and
# FROZEN.files.tsv.gz into each set's folder, and keeps the public copy (frozen/<id>.json) and the
# record's measured block under its home, where a session reads them back into a pull request. A
# set the promoter installs from now on is frozen by the promoter itself, so this is for the sets
# that landed before. It runs under the owner's own grid account, since the owner's data root is
# the owner's to write; every job is queued by hpcworker's `job submit`, class batch, as
# grid/promote.sh's are, and only on the owner's word with the count of jobs (the project's rule:
# no grid job without the owner's word and the count).
#
#   bash freeze.sh pilot [ID]         one job for the one set ID of grid/freeze-plan.tsv, to measure
#                                     the read rate before the rest; with no ID, the set whose stated
#                                     size is nearest 100 GB (amos22 on 2026-10-23)
#   bash freeze.sh start [JOBS]       the sets of grid/freeze-plan.tsv not yet frozen, in JOBS (1 to 8,
#                                     4 when not given, the count the owner approved on 2026-10-23)
#                                     jobs of about equal stated size
#   bash freeze.sh submit LIST JOBS   the same for any list of tools/freeze.py plan's lines
#   bash freeze.sh status             the jobs, the sets frozen so far and each job's last lines
#   bash freeze.sh report             the public copies kept so far, sent to the branch freeze-report
#                                     of spine-datasets as one commit with no parent, through the
#                                     account's own gh; no job, a few calls to GitHub's API, and a
#                                     session brings them into the records (tools/freeze.py apply)
#   bash freeze.sh run SHARE          inside a job: freeze each set of SHARE not yet frozen
#
# The grid gate's words freeze pilot, freeze start, freeze status and freeze report (hpcworker's
# tools/grid_gate.sh) fetch tools/freeze.py, this file and grid/freeze-plan.tsv at the head of the
# default branch into code/ and run these, so nobody types them. A job that reaches its wall time or
# is requeued carries on: a set already frozen is skipped, a set half read resumes from its
# checkpoint (.FROZEN.partial) in its folder, and a lock per set, which the kernel lets go when a job
# dies, keeps two jobs off one set.
#
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=8G
set -euo pipefail

PROJECT=spine-datasets
JOB=freeze
# the folder above code/ when run from there, as the gate and the jobs it queues run it, since a
# job may not carry the gate's environment; else FREEZE_HOME, else the lab's usual place
HERE=$(cd "$(dirname "$0")" && pwd)
if [ -z "${FREEZE_HOME:-}" ] && [ "$(basename "$HERE")" = code ]; then FREEZE_HOME=$(dirname "$HERE"); fi
HOME_DIR=${FREEZE_HOME:-/rs/rs_grp_oschome/$USER/spine-datasets-freeze}
PLAN=$HOME_DIR/code/freeze-plan.tsv
HPCW=${HPCWORKER:-$HOME/hpcworker/framework/bin/hpcworker}
CODE=${FREEZE_CODE:-$HOME_DIR/code/freeze.py}
REPO=OpenSpineConsortium/spine-datasets
REPORT_BRANCH=freeze-report

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

split_list() {
  # the largest sets first, each to the share with the least so far; a set with no stated size
  # counts as 100 GB, so the unknown ones spread out too
  local list=$1 jobs=$2 stamp=$3
  sort -t$'\t' -k3,3 -g -r "$list" | awk -F'\t' -v jobs="$jobs" -v dir="$HOME_DIR/shares" -v stamp="$stamp" '
    { size = ($3 == "-") ? 100000000000 : $3; best = 1
      for (j = 2; j <= jobs; j++) if (load[j] < load[best]) best = j
      load[best] += size; print > (dir "/" stamp "-" best ".tsv") }'
}

unfrozen() { # LIST: its lines whose set has no freeze kept here yet
  local ident rest
  while IFS=$'\t' read -r ident rest; do
    [ -f "$HOME_DIR/frozen/$ident.json" ] || printf '%s\t%s\n' "$ident" "$rest"
  done < "$1"
}

submit() { # LIST JOBS
  local list=$1 jobs=$2 stamp share
  [[ "$jobs" =~ ^[1-8]$ ]] || { echo "JOBS is 1 to 8"; exit 2; }
  mkdir -p "$HOME_DIR/shares" "$HOME_DIR/frozen" "$HOME_DIR/measured" "$HOME_DIR/locks"
  [ -f "$CODE" ] && [ -f "$HOME_DIR/code/freeze.sh" ] || { echo "copy tools/freeze.py and grid/freeze.sh from the default branch into $HOME_DIR/code first"; exit 2; }
  stamp=$(date -u +%Y%m%dT%H%M%S)-$$  # one name per call, so a share a queued job will read is never rewritten
  unfrozen "$list" > "$HOME_DIR/shares/$stamp.todo"
  [ -s "$HOME_DIR/shares/$stamp.todo" ] || { echo "nothing to freeze: every set of $list is frozen"; return 0; }
  split_list "$HOME_DIR/shares/$stamp.todo" "$jobs" "$stamp"
  for share in "$HOME_DIR/shares/$stamp"-*.tsv; do
    echo "queueing $(wc -l < "$share") sets: $(cut -f1 "$share" | tr '\n' ' ')"
    hpcw job submit --project "$PROJECT" --name "$JOB" --class batch --dir "$HOME_DIR" \
      -- "$HOME_DIR/code/freeze.sh" run "$share"
  done
}

case "${1:-}" in
  submit)
    [ -n "${2:-}" ] && [ -n "${3:-}" ] || { echo "usage: freeze.sh submit LIST JOBS"; exit 2; }
    submit "$2" "$3"
    ;;
  pilot)
    mkdir -p "$HOME_DIR/shares"
    if [ -n "${2:-}" ]; then
      [[ "$2" =~ ^[a-z0-9_]{1,40}$ ]] || { echo "usage: freeze.sh pilot [ID]"; exit 2; }
      awk -F'\t' -v id="$2" '$1 == id' "$PLAN" > "$HOME_DIR/shares/pilot.tsv"
    else
      awk -F'\t' '$3 != "-" { d = $3 - 1e11; if (d < 0) d = -d; if (best == "" || d < bd) { best = $0; bd = d } }
        END { if (best != "") print best }' "$PLAN" > "$HOME_DIR/shares/pilot.tsv"
    fi
    [ -s "$HOME_DIR/shares/pilot.tsv" ] || { echo "no such set in $PLAN"; exit 2; }
    submit "$HOME_DIR/shares/pilot.tsv" 1
    ;;
  start)
    submit "$PLAN" "${2:-4}"
    ;;
  status)
    squeue -u "$USER" -n "$PROJECT-$JOB" || true
    echo "frozen so far: $(ls "$HOME_DIR"/frozen/*.json 2>/dev/null | wc -l) of $(wc -l < "$PLAN" 2>/dev/null || echo '?')"
    for ident in $(ls -t "$HOME_DIR"/measured/*.json 2>/dev/null | head -20 | xargs -r -n1 basename | sed 's/\.json$//'); do
      echo "measured $ident: $(tr -d ' \n' < "$HOME_DIR/measured/$ident.json")"
    done
    hpcw job status --project "$PROJECT" --last 8 || true
    ;;
  report)
    command -v gh >/dev/null 2>&1 || { echo "no gh on this account's path"; exit 2; }
    py=$(python_bin)
    tree_body=$HOME_DIR/report-tree.json
    "$py" "$CODE" bundle "$HOME_DIR/frozen" > "$tree_body.tmp" && mv -f "$tree_body.tmp" "$tree_body" \
      || { rm -f "$tree_body.tmp"; echo "nothing to report"; exit 1; }
    tree=$(gh api -X POST "repos/$REPO/git/trees" --input "$tree_body" --jq .sha < /dev/null)
    [[ "$tree" =~ ^[0-9a-f]{40}$ ]] || { echo "GitHub took no tree"; exit 1; }
    sets=$(ls "$HOME_DIR"/frozen/*.json 2>/dev/null | wc -l)
    commit=$(gh api -X POST "repos/$REPO/git/commits" -f message="The public copies of $sets frozen sets, as grid/freeze.sh report found them" \
      -f tree="$tree" --jq .sha < /dev/null)
    [[ "$commit" =~ ^[0-9a-f]{40}$ ]] || { echo "GitHub took no commit"; exit 1; }
    # the branch holds only this commit, so each report replaces the last; a first report makes it
    if gh api "repos/$REPO/git/ref/heads/$REPORT_BRANCH" --jq .object.sha < /dev/null > /dev/null 2>&1; then
      gh api -X PATCH "repos/$REPO/git/refs/heads/$REPORT_BRANCH" -f sha="$commit" -F force=true --jq .object.sha < /dev/null > /dev/null
    else
      gh api -X POST "repos/$REPO/git/refs" -f ref="refs/heads/$REPORT_BRANCH" -f sha="$commit" --jq .object.sha < /dev/null > /dev/null
    fi || { echo "GitHub did not move $REPORT_BRANCH"; exit 1; }
    echo "reported $sets frozen sets to $REPORT_BRANCH at ${commit:0:12}"
    ;;
  run)
    [ -n "${SLURM_JOB_ID:-}" ] || { echo "run is for inside a job; use submit"; exit 2; }
    py=$(python_bin)
    mkdir -p "$HOME_DIR/locks"
    while IFS=$'\t' read -r ident folder _size; do
      if [ -f "$HOME_DIR/frozen/$ident.json" ]; then continue; fi
      (
        flock -n 9 || { echo "$ident: another job holds it; skipped"; exit 0; }
        started=$(date +%s)
        echo "$(date -u +%FT%TZ) $ident: freezing $folder"
        if "$py" "$CODE" freeze "$folder" --id "$ident" --workers "${SLURM_CPUS_PER_TASK:-1}" \
            --copy "$HOME_DIR/frozen/$ident.json.tmp"; then
          "$py" "$CODE" measured "$folder/FROZEN.json" > "$HOME_DIR/measured/$ident.json"
          mv "$HOME_DIR/frozen/$ident.json.tmp" "$HOME_DIR/frozen/$ident.json"
          echo "$ident: $(( $(date +%s) - started )) seconds"
        else
          echo "$ident: not frozen (exit $?); the next job tries again"
        fi
      ) 9>"$HOME_DIR/locks/$ident.lock"
    done < "$2"
    ;;
  *)
    echo "usage: freeze.sh pilot ID | start JOBS | submit LIST JOBS | status | report | run SHARE"; exit 2
    ;;
esac
