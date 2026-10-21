#!/bin/bash
# The promoter's Slurm chain, run under the owner's own grid account: the one writer of
# /rs/rs_grp_oschome/shared/datasets (tools/promote.py says what each pass does, grid/README.md
# how a collaborator's pull request reaches it). Each job queues its successor first, so the chain
# comes back after a wall time or a preemption with nobody at the keyboard, then takes the
# promoter's code from the default branch where an owner merged it, and runs one pass every ten
# minutes until its wall time is near. Nothing runs on the login node but gh, squeue, sbatch and
# scancel; every download and every python3 runs inside the job. Started once by the owner:
#
#   bash promote.sh start     queue the chain, unless one is already queued or running
#   bash promote.sh status    what the chain is doing and its latest log lines
#   bash promote.sh stop      cancel the chain
#
#SBATCH --job-name=spine-datasets-promoter
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --time=08:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --requeue
set -euo pipefail

NAME=spine-datasets-promoter
REPO=${PROMOTER_REPO:-OpenSpineConsortium/spine-datasets}
OWNERS=${PROMOTER_OWNERS:-Gregory-Schwing-MD-PhD}
SHARED=${PROMOTER_SHARED:-/rs/rs_grp_oschome/shared/datasets}
HOME_DIR=${PROMOTER_HOME:-/rs/rs_grp_oschome/$USER/spine-datasets-promoter}
INTERVAL=${PROMOTER_INTERVAL:-600}
# stop starting passes this long before the wall time, so a pass is never cut off mid-rename
MARGIN=${PROMOTER_MARGIN:-1800}

python_bin() {
  # the newest python3 the node has; the promoter needs nothing newer than 3.6
  for candidate in python3.12 python3.11 python3.10 python3.9 python3.8 python3 ; do
    if command -v "$candidate" >/dev/null 2>&1; then echo "$candidate"; return; fi
  done
  echo "no python3 on $(hostname -s)" >&2; exit 2
}

queued() {
  squeue -h -u "$USER" -n "$NAME" -o %i
}

fetch_code() {
  # the first copy, before any self-update: the default branch's promoter, read through gh
  mkdir -p "$HOME_DIR/code" "$HOME_DIR/logs"
  if [ ! -f "$HOME_DIR/code/promote.py" ]; then
    gh api -H "Accept: application/vnd.github.raw" "repos/$REPO/contents/tools/promote.py" > "$HOME_DIR/code/promote.py.tmp"
    mv "$HOME_DIR/code/promote.py.tmp" "$HOME_DIR/code/promote.py"
  fi
  if [ ! -f "$HOME_DIR/code/promote.sh" ]; then
    gh api -H "Accept: application/vnd.github.raw" "repos/$REPO/contents/grid/promote.sh" > "$HOME_DIR/code/promote.sh.tmp"
    mv "$HOME_DIR/code/promote.sh.tmp" "$HOME_DIR/code/promote.sh"
  fi
}

one_pass() {
  local py
  py=$(python_bin)
  "$py" "$HOME_DIR/code/promote.py" self-update --repo "$REPO" --owners "$OWNERS" --into "$HOME_DIR/code" || true
  "$py" "$HOME_DIR/code/promote.py" once --repo "$REPO" --shared "$SHARED" --owners "$OWNERS" \
    --job "${SLURM_JOB_ID:-local}" || echo "pass failed with exit $?; the next pass tries again"
}

seconds_left() {
  local end
  end=$(squeue -h -j "$SLURM_JOB_ID" -o %e)
  echo $(( $(date -d "$end" +%s) - $(date +%s) ))
}

case "${1:-run}" in
  start)
    fetch_code
    if [ -n "$(queued)" ]; then echo "already queued: $(queued | tr '\n' ' ')"; exit 0; fi
    sbatch -D "$HOME_DIR" --output="$HOME_DIR/logs/%x-%j.out" "$HOME_DIR/code/promote.sh" run
    ;;
  status)
    squeue -u "$USER" -n "$NAME"
    latest=$(ls -t "$HOME_DIR"/logs/*.out 2>/dev/null | head -1 || true)
    if [ -n "$latest" ]; then echo "== $latest"; tail -20 "$latest"; fi
    ;;
  stop)
    ids=$(queued)
    if [ -n "$ids" ]; then echo "$ids" | xargs scancel; fi
    echo "stopped"
    ;;
  run)
    [ -n "${SLURM_JOB_ID:-}" ] || { echo "run is for inside a job; use start"; exit 2; }
    # the successor first, unless one waits already: afterany brings the chain back however this job ends
    if [ "$(queued | grep -cv "^$SLURM_JOB_ID$" || true)" = 0 ]; then
      sbatch -D "$HOME_DIR" --output="$HOME_DIR/logs/%x-%j.out" --dependency="afterany:$SLURM_JOB_ID" \
        "$HOME_DIR/code/promote.sh" run
    fi
    echo "$(date -u +%FT%TZ) promoter job $SLURM_JOB_ID on $(hostname -s), shared tree $SHARED"
    while [ "$(seconds_left)" -gt "$MARGIN" ]; do
      one_pass
      sleep "$INTERVAL"
    done
    ;;
  *)
    echo "usage: promote.sh start|status|stop"; exit 2
    ;;
esac
