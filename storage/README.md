# The storage planner

Source: the thread "Check frozen manifest job", 2026-10-24, the owner's ask of that day to see
the drive's use, try combinations of datasets under 20 TB, trigger removals and additions from
the textbook's artifact, and keep some data in his own home on the grid, which holds 4 TB.

- VOLUME.json is the latest reading of the lab volume (used bytes, its quota, when it was read)
  and of the home (its 4 TB and, once a grid word reads it, its use), with the 20 TB target. A
  session updates it from the grid's status word; nothing else writes it.
- tools/storage.py makes the feed PLAN.json from it, the records under datasets/ and
  lineage/OVERLAP.json. .github/workflows/storage.yml publishes the feed on the branch
  storage-feed after each change, and the artifact reads it there. The feed holds ids and whole
  numbers only: no path below the top folder.
- A trial combination is a selection: `-id` retires a held set (its images are deleted, its
  record, freeze and file list stay, so it can be rebuilt and the rebuild proved identical), `+id`
  fetches one, `id@home` and `id@lab` move one. `python3 tools/storage.py check -- "<selection>"`
  prints the totals after it or every reason it cannot go ahead: a cap passed, a set not frozen or
  with no recipe, a set not open to fetch or with no size, the home's use not read yet.
- Running storage.yml by hand with a selection, or from the artifact, writes requests/<time>.json
  and offers it as a pull request naming every set. The owner's merge is his word for each set
  it names; a session never merges one. Every fetch still passes the grid's size rule, which reads
  the exact size from the source before a byte lands.
- On the grid, grid/storage.sh carries out a merged request: `apply STAMP` reads
  requests/STAMP.json as the default branch holds it and queues one job that plans each
  retirement (tools/retire.py: the folder must be the set's own under a data root with no link on
  its path, its freeze must be the tree hash the request names, and its files the freeze's, or
  nothing is listed), and names the fetch word of each fetch for the owner to press; `home` reads
  the home's use; `report` carries the plans' counts and the home's reading to the branch
  storage-report. A plan keeps the freeze, labels, masks and metadata and deletes nothing.
- `retire STAMP`, a word of its own sent by the owner once the plans are reported, queues one job
  that deletes what each plan listed (tools/retire.py delete), after the same checks pass again on
  the folder as it is and give the same list (the owner's choice of 2026-10-24: allowed, narrowly).
  It writes RETIRED.json beside the freeze, and report carries a copy back as
  storage/retired/<id>.json. A retirement cut short is carried on by sending the word again.
- `survey` queues one read-only job that sizes the whole volume by folder (tools/survey.py, the
  owner's yes of 2026-10-25, asking where the 9.9 TB that is not datasets is): each folder's
  recursive size from CephFS's ceph.dir.rbytes, the owner's and the shared tree opened down four
  levels above 50 GB, each folder put in one kind (a dataset with its masks and images apart by
  its frozen list, masks, untracked data, runs and outputs, jobs and logs, other), other accounts
  counted in one row and never named. `report` carries it back as storage/survey.json.
- The gate words are storage-apply-<stamp>, storage-retire-<stamp>, storage-survey,
  storage-status and storage-report in symphony-template's grid-accounts.yml (hpcworker's storage words).
- Not built yet: moves to the home, which wait for its path.
