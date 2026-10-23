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
#   bash freeze.sh submit LIST JOBS   split LIST (tools/freeze.py plan's lines) into JOBS shares of
#                                     about equal stated size and queue one job for each
#   bash freeze.sh status             the jobs and the sets frozen so far
#   bash freeze.sh run SHARE          inside a job: freeze each set of SHARE not yet frozen
#
# A job that reaches its wall time or is requeued carries on: a set already frozen is skipped, and
# a set half read resumes from its checkpoint (.FROZEN.partial) in its folder.
#
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=8G
set -euo pipefail

PROJECT=spine-datasets
JOB=freeze
HOME_DIR=${FREEZE_HOME:-/rs/rs_grp_oschome/$USER/spine-datasets-freeze}
HPCW=${HPCWORKER:-$HOME/hpcworker/framework/bin/hpcworker}
CODE=${FREEZE_CODE:-$HOME_DIR/code/freeze.py}

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
  local list=$1 jobs=$2
  sort -t$'\t' -k3,3 -g -r "$list" | awk -F'\t' -v jobs="$jobs" -v dir="$HOME_DIR/shares" '
    { size = ($3 == "-") ? 100000000000 : $3; best = 1
      for (j = 2; j <= jobs; j++) if (load[j] < load[best]) best = j
      load[best] += size; print > (dir "/share-" best ".tsv") }'
}

case "${1:-}" in
  submit)
    [ -n "${2:-}" ] && [ -n "${3:-}" ] || { echo "usage: freeze.sh submit LIST JOBS"; exit 2; }
    mkdir -p "$HOME_DIR/shares" "$HOME_DIR/frozen" "$HOME_DIR/measured"
    [ -f "$CODE" ] && [ -f "$HOME_DIR/code/freeze.sh" ] || { echo "copy tools/freeze.py and grid/freeze.sh from the default branch into $HOME_DIR/code first"; exit 2; }
    rm -f "$HOME_DIR"/shares/share-*.tsv
    split_list "$2" "$3"
    for share in "$HOME_DIR"/shares/share-*.tsv; do
      hpcw job submit --project "$PROJECT" --name "$JOB" --class batch --dir "$HOME_DIR" \
        -- "$HOME_DIR/code/freeze.sh" run "$share"
    done
    ;;
  status)
    squeue -u "$USER" -n "$PROJECT-$JOB" || true
    echo "frozen so far: $(ls "$HOME_DIR"/frozen/*.json 2>/dev/null | wc -l)"
    ;;
  run)
    [ -n "${SLURM_JOB_ID:-}" ] || { echo "run is for inside a job; use submit"; exit 2; }
    py=$(python_bin)
    while IFS=$'\t' read -r ident folder _size; do
      if [ -f "$HOME_DIR/frozen/$ident.json" ]; then continue; fi
      echo "$(date -u +%FT%TZ) $ident: freezing $folder"
      if "$py" "$CODE" freeze "$folder" --id "$ident" --workers "${SLURM_CPUS_PER_TASK:-1}" \
          --copy "$HOME_DIR/frozen/$ident.json.tmp"; then
        "$py" "$CODE" measured "$folder/FROZEN.json" > "$HOME_DIR/measured/$ident.json"
        mv "$HOME_DIR/frozen/$ident.json.tmp" "$HOME_DIR/frozen/$ident.json"
      else
        echo "$ident: not frozen (exit $?); the next job tries again"
      fi
    done < "$2"
    ;;
  *)
    echo "usage: freeze.sh submit LIST JOBS | status | run SHARE"; exit 2
    ;;
esac
