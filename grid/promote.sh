#!/bin/bash
# The promoter's Slurm chain, run under the owner's own grid account: the one writer of
# /rs/rs_grp_oschome/shared/datasets (tools/promote.py says what each pass does, grid/README.md
# how a collaborator's pull request reaches it). Each job queues its successor first, so the chain
# comes back after a wall time or a preemption with nobody at the keyboard, then takes the
# promoter's code from the default branch where it came from the owner's own pull request, and runs
# one pass every ten minutes until its wall time is near. Successors are singleton jobs of one name,
# so however many get queued they run one at a time, and a lock keeps two passes apart. Every job is
# queued by hpcworker's `job submit`, class batch, which takes the partition, QoS, account and requeue
# from the site's profile and keeps each job's id and log in its ledger for the project spine-datasets;
# this script says only its own time, CPUs, memory and the singleton rule. Nothing runs on the login
# node but gh, squeue, scancel and hpcworker; every download and every python3 runs inside the job.
# Started, read and stopped by the grid gate's words promoter-start, promoter-status and promoter-stop
# (hpcworker's tools/grid_gate.sh), so nobody types these by hand:
#
#   bash promote.sh start [REF]   queue the chain, unless one is already queued or running; the
#                                 first copy of the code is taken at REF, the commit the owner names
#   bash promote.sh status    what the chain is doing and its latest log lines
#   bash promote.sh stop      cancel the chain
#
#SBATCH --time=08:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --dependency=singleton
set -euo pipefail

PROJECT=spine-datasets
JOB=promoter
NAME=$PROJECT-$JOB   # the job name hpcworker gives it, which singleton and squeue go by
REPO=${PROMOTER_REPO:-OpenSpineConsortium/spine-datasets}
OWNERS=${PROMOTER_OWNERS:-Gregory-Schwing-MD-PhD}
SHARED=${PROMOTER_SHARED:-/rs/rs_grp_oschome/shared/datasets}
HOME_DIR=${PROMOTER_HOME:-/rs/rs_grp_oschome/$USER/spine-datasets-promoter}
INTERVAL=${PROMOTER_INTERVAL:-600}
# the gate names its own clone's hpcworker; a job, and a copy started any other way, find the clone
# in the home folder, where hpcworker's setup puts it (the clone keeps it 0644, so it runs through bash)
HPCW=${HPCWORKER:-$HOME/hpcworker/framework/bin/hpcworker}
# the job's own clock, so a busy scheduler never ends the loop early: eight hours of wall time, and
# no pass started in the last half hour of it, so a pass is never cut off mid-rename
WALL=28800
MARGIN=${PROMOTER_MARGIN:-1800}

python_bin() {
  # the newest python3 the node has; the promoter needs nothing newer than 3.6
  for candidate in python3.12 python3.11 python3.10 python3.9 python3.8 python3 ; do
    if command -v "$candidate" >/dev/null 2>&1; then echo "$candidate"; return; fi
  done
  echo "no python3 on $(hostname -s)" >&2; exit 2
}

queued() {
  squeue -h -u "$USER" -n "$NAME" -o %i "$@"
}

fetch_code() {
  # the first copy, before any self-update, at the commit the owner named: later copies come only
  # through self-update's provenance rule
  local ref=$1 path
  mkdir -p "$HOME_DIR/code" "$HOME_DIR/logs"
  for path in tools/promote.py grid/promote.sh tools/freeze.py; do
    if [ ! -f "$HOME_DIR/code/${path##*/}" ]; then
      gh api -H "Accept: application/vnd.github.raw" "repos/$REPO/contents/$path?ref=$ref" > "$HOME_DIR/code/${path##*/}.tmp"
      mv "$HOME_DIR/code/${path##*/}.tmp" "$HOME_DIR/code/${path##*/}"
    fi
  done
}

one_pass() {
  local py
  py=$(python_bin)
  (
    flock -n 9 || { echo "another pass holds the lock; skipped"; exit 0; }
    "$py" "$HOME_DIR/code/promote.py" self-update --repo "$REPO" --owners "$OWNERS" --into "$HOME_DIR/code" || true
    "$py" "$HOME_DIR/code/promote.py" once --repo "$REPO" --shared "$SHARED" --owners "$OWNERS" \
      --job "${SLURM_JOB_ID:-local}" || echo "pass failed with exit $?; the next pass tries again"
  ) 9>"$HOME_DIR/promoter.lock"
}

hpcw() {
  [ -f "$HPCW" ] || { echo "no hpcworker at $HPCW" >&2; return 2; }
  bash "$HPCW" "$@"
}

submit() {
  # from inside a job, the job's own SLURM_ names would ride into the new job's request; only
  # SLURM_CONF, which says where the scheduler is, goes along
  (
    for v in $(compgen -e); do
      case "$v" in SLURM_CONF) ;; SLURM_*) unset "$v";; esac
    done
    hpcw job submit --project "$PROJECT" --name "$JOB" --class batch --dir "$HOME_DIR" \
      -- "$HOME_DIR/code/promote.sh" run
  )
}

queue_successor() {
  # one successor waiting is enough; where squeue cannot answer, queue one anyway, since singleton
  # runs the extras one after another and each of them looks again before queueing its own
  local waiting
  if waiting=$(queued -t PENDING); then
    [ -z "$waiting" ] || return 0
  fi
  submit
}

case "${1:-run}" in
  start)
    [ -n "${2:-}" ] || { echo "usage: promote.sh start COMMIT (the commit the owner names)"; exit 2; }
    fetch_code "$2"
    if [ -n "$(queued)" ]; then echo "already queued: $(queued | tr '\n' ' ')"; exit 0; fi
    submit
    ;;
  status)
    squeue -u "$USER" -n "$NAME"
    hpcw job status --project "$PROJECT" --last 5 || true
    running=$(queued -t RUNNING | head -1 || true)
    if [ -n "$running" ]; then
      echo "== job $running"; hpcw job log --project "$PROJECT" "$running" --lines 20 || true
    else
      # jobs queued before hpcworker kept the chain wrote their logs here
      latest=$(ls -t "$HOME_DIR"/logs/*.out 2>/dev/null | head -1 || true)
      if [ -n "$latest" ]; then echo "== $latest"; tail -20 "$latest"; fi
    fi
    ;;
  stop)
    ids=$(queued)
    if [ -n "$ids" ]; then echo "$ids" | xargs scancel; fi
    echo "stopped"
    ;;
  run)
    [ -n "${SLURM_JOB_ID:-}" ] || { echo "run is for inside a job; use start"; exit 2; }
    # the successor first: singleton holds it until this job ends, however it ends
    queue_successor || echo "could not queue a successor; the chain ends with this job"
    started=$(date +%s)
    echo "$(date -u +%FT%TZ) promoter job $SLURM_JOB_ID on $(hostname -s), shared tree $SHARED"
    while [ $(( $(date +%s) - started )) -lt $(( WALL - MARGIN )) ]; do
      one_pass
      sleep "$INTERVAL"
    done
    ;;
  *)
    echo "usage: promote.sh start COMMIT|status|stop"; exit 2
    ;;
esac
