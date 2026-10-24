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
- Not built yet: the grid job words that carry out a merged request (retire, fetch, move), and the
  reading of the home's use. Until they are, a merged request is the record of what to do, and
  each action is sent by its own gate word on the owner's word.
