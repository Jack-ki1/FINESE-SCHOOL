"""Git & GitHub subtopics — enriched schema."""

SUBTOPICS = [
    dict(
        id="git-mental-model",
        title="Git's Mental Model: Snapshots, Not Diffs",
        hook="Most Git confusion traces back to one wrong mental model — thinking it stores changes, when it actually stores complete snapshots.",
        explanation=(
            "Unlike older version control systems that stored a series of file-by-file changes (diffs), Git "
            "stores a full snapshot of every tracked file each time you commit. If a file hasn't changed between "
            "commits, Git just links to the identical previous version instead of storing it again, so this is "
            "efficient in practice, but conceptually every commit is a complete picture of the project at that "
            "moment, not a delta.\n\n"
            "A Git project has three working areas: the working directory (your actual files), the staging area "
            "/ index (a draft of what the next commit will contain), and the repository (the permanent, "
            "committed history). `git add` moves changes from working directory to staging, and `git commit` "
            "takes a permanent snapshot of whatever is currently staged — this two-step process is what lets you "
            "commit only part of your changes at a time.\n\n"
            "Every commit, once created, is identified by a SHA-1 hash computed from its content (the snapshot, "
            "the parent commit(s), author, message, and timestamp) — this is why changing anything about a "
            "commit, even just its message, technically produces a brand new commit with a new hash, and why "
            "Git can reliably detect if history has been tampered with: any change anywhere invalidates every "
            "hash depending on it."
        ),
        deep_dive=(
            "Because each commit's hash depends on its parent commit's hash, commits form a cryptographically "
            "linked chain — this is the same fundamental structure underlying blockchain technology, though "
            "Git predates that popularization by years, using the idea purely for reliable, tamper-evident "
            "history tracking rather than any distributed consensus mechanism.\n\n"
            "`git diff` computing readable line-by-line differences between commits doesn't contradict the "
            "snapshot model — Git computes that diff on the fly by comparing two complete snapshots, rather "
            "than storing the diff itself as the underlying data structure. This is a genuinely important "
            "distinction: the diff view you see is a derived, computed representation, not what's actually "
            "stored on disk.\n\n"
            "Content-addressable storage (Git's core technical design) means identical file content is stored "
            "exactly once regardless of which commits or branches reference it — two commits with a completely "
            "unchanged file both point at the exact same stored blob, which is precisely why Git can store many "
            "commits' worth of largely-similar snapshots efficiently rather than duplicating unchanged files "
            "over and over."
        ),
        code=dict(
            lang="bash",
            label="The three areas in action",
            src=(
                "git status                  # see what's changed in the working directory\n"
                "git add src/app.py           # stage this specific file\n"
                "git add .                    # stage everything changed\n"
                "git commit -m \"Add login validation\"   # snapshot what's staged\n"
                "git log --oneline            # see the snapshot history"
            ),
        ),
        advanced_code=dict(
            lang="bash",
            label="Inspecting the actual content-addressable objects Git stores",
            src=(
                "git cat-file -p HEAD                  # view the commit object's raw content\n"
                "git cat-file -p HEAD^{tree}            # view the tree (snapshot) it points to\n"
                "git rev-parse HEAD                     # the commit's SHA-1 hash\n\n"
                "# Two commits with an unchanged file point at the SAME blob object --\n"
                "# nothing is duplicated for files that didn't change between commits"
            ),
        ),
        example=(
            "A developer editing five files but only wanting to commit changes to two of them uses `git add "
            "file1.py file2.py` to stage just those, leaving the other three modified-but-uncommitted — a "
            "workflow only the staging area's snapshot model makes possible."
        ),
        best_practices=[
            "Write commit messages that describe why a change was made, not just what changed — the diff already shows what changed.",
            "Commit small, logically complete units of work rather than batching unrelated changes into one giant commit.",
            "Run `git status` before every commit as a habit — it's the fastest way to catch a file you forgot to stage, or one you staged by mistake.",
            "Understand that git diff is a computed comparison between snapshots, not evidence that Git internally stores diffs.",
        ],
        pitfalls=[
            "Running `git add .` without checking `git status` first, accidentally committing files that shouldn't be tracked (like `.env` or build artifacts).",
            "Treating a commit as a 'diff from the last commit' mentally, which leads to confusion when reasoning about what a commit actually contains.",
            "Assuming a commit's hash only reflects its content and not its parent, message, or metadata — any of these changing produces a genuinely different commit.",
        ],
        glossary=[
            dict(term="Snapshot", definition="A complete picture of every tracked file's state at the moment of a commit, Git's fundamental unit of history (as opposed to a diff)."),
            dict(term="Staging area / index", definition="A draft area where changes are prepared before being committed, populated via git add."),
            dict(term="SHA-1 hash", definition="A unique identifier computed from a commit's content and metadata, used by Git to reference and verify commits."),
            dict(term="Content-addressable storage", definition="Git's storage design where identical content is stored exactly once, referenced by its hash, regardless of how many commits point to it."),
        ],
        faq=[
            dict(q="What actually happens internally when I run git commit?", a="Git takes everything currently in the staging area, creates a new tree object representing that complete snapshot, creates a new commit object pointing to that tree and to the previous commit (its parent), and moves the current branch pointer to this new commit."),
            dict(q="How do I unstage a file I added by mistake before committing?", a="git restore --staged <file> (or the older git reset HEAD <file>) removes it from the staging area without discarding your actual changes in the working directory."),
            dict(q="Explain the difference between the working directory, staging area, and repository.", a="The working directory is your actual files as you're editing them. The staging area is a draft of exactly what the next commit will contain, populated with git add. The repository is the permanent history of committed snapshots, updated with git commit."),
        ],
        quiz=[
            dict(
                question="What does Git actually store for each commit?",
                options=["Only the lines that changed since the last commit", "A complete snapshot of every tracked file at that moment", "A description of the change in plain English", "The commit message only"],
                correct=1,
                explanation="Unlike diff-based version control systems, Git stores a full snapshot at every commit, though it stores unchanged files efficiently by referencing the same underlying content rather than duplicating it.",
            ),
        ],
        prompts=[
            "What actually happens internally when I run git commit?",
            "How do I unstage a file I added by mistake before committing?",
            "Explain the difference between the working directory, staging area, and repository.",
            "How does Git's content-addressable storage avoid duplicating unchanged files across commits?",
        ],
    ),
    dict(
        id="branching-merging",
        title="Branching & Merging",
        hook="A branch is just a movable pointer to a commit — understanding that makes branching feel a lot less mysterious and a lot more disposable.",
        explanation=(
            "A Git branch is a lightweight, movable label pointing at a specific commit; creating one is nearly "
            "instant because it doesn't copy any files, it just adds a new pointer. `main` (or `master`) is "
            "conventionally the primary branch, and feature branches let you develop something new in isolation "
            "without touching that stable line of history until it's ready.\n\n"
            "Merging brings the changes from one branch into another. If the target branch hasn't diverged (no "
            "new commits since the branch point), Git performs a fast-forward merge — it just moves the pointer "
            "forward. If both branches have new commits, Git creates a merge commit with two parents, combining "
            "both histories. When the same lines of the same file were changed differently on both branches, Git "
            "can't decide automatically and raises a merge conflict for you to resolve by hand.\n\n"
            "`HEAD` is a special pointer indicating which commit (and typically, which branch) you currently "
            "have checked out — it's what moves when you switch branches, and understanding it as 'a pointer "
            "to a pointer' (HEAD usually points at a branch name, which itself points at a commit) clarifies "
            "otherwise confusing states like a 'detached HEAD', where HEAD points directly at a specific commit "
            "rather than at a branch name."
        ),
        deep_dive=(
            "A detached HEAD state happens when you check out a specific commit directly (`git checkout "
            "<commit-hash>`) rather than a branch name — you can look around and even make new commits, but "
            "without creating a new branch to hold them, those commits become unreachable and eventually "
            "garbage-collected once you switch away, since no branch pointer is keeping them 'reachable.' This "
            "is a common source of 'I made commits and now I can't find them' panic, usually resolved by "
            "creating a branch at that point before switching away.\n\n"
            "Git's garbage collection (`git gc`) periodically cleans up commits that are no longer reachable "
            "from any branch, tag, or other reference — this is why deleting a branch doesn't necessarily "
            "delete its commits immediately, but they will eventually be cleaned up if truly unreachable, "
            "which is also why `git reflog` (a safety net logging where HEAD has recently pointed) is such a "
            "valuable recovery tool for commits that seem to have vanished but haven't actually been "
            "permanently garbage collected yet.\n\n"
            "Merge commits explicitly preserve the true chronological branching structure (both parent commits "
            "are recorded), which some teams value for an accurate historical record, while others prefer to "
            "avoid the visual clutter of many merge commits by using rebase or squash merging instead — a "
            "genuine style/workflow choice covered in depth in the merge vs. rebase lesson."
        ),
        code=dict(
            lang="bash",
            label="A typical feature branch workflow",
            src=(
                "git checkout -b feature/user-auth    # create and switch to a new branch\n"
                "# ... make commits on the branch ...\n"
                "git checkout main\n"
                "git pull origin main                 # make sure main is current\n"
                "git merge feature/user-auth           # bring the feature branch into main\n\n"
                "# if there's a conflict:\n"
                "# 1. Git marks the conflicting lines in the file with <<<<<<< ======= >>>>>>>\n"
                "# 2. edit the file to the correct final version\n"
                "git add resolved_file.py\n"
                "git commit                            # completes the merge"
            ),
        ),
        advanced_code=dict(
            lang="bash",
            label="Recovering 'lost' commits from a detached HEAD using reflog",
            src=(
                "git checkout a1b2c3d      # detached HEAD -- checking out a commit directly\n"
                "# ... make some commits here ...\n"
                "git checkout main          # switching away -- those commits look 'lost'\n\n"
                "git reflog                 # shows every recent position HEAD has been at\n"
                "# find the commit hash from before you switched away\n"
                "git branch recovered-work <that-commit-hash>   # create a branch to save it"
            ),
        ),
        example=(
            "Two developers both edit the same function on different branches — one renaming a variable, the "
            "other adding a new parameter — and merging surfaces a conflict because Git genuinely can't guess "
            "which combination of both edits the team actually wants."
        ),
        best_practices=[
            "Keep feature branches short-lived and focused on one task, merging back frequently to avoid large, painful conflicts.",
            "Pull the latest changes into your base branch before merging your feature branch in, so you resolve conflicts against the current state.",
            "Delete branches after merging (`git branch -d feature/x`) to keep the branch list meaningful rather than a growing pile of stale names.",
            "Create a branch before making commits in a detached HEAD state, so those commits don't become unreachable once you switch away.",
        ],
        pitfalls=[
            "Letting a feature branch drift for weeks without merging, guaranteeing a large, hard-to-resolve conflict later.",
            "Resolving a conflict by blindly keeping 'my' version without reading what the other branch actually changed and why.",
            "Panicking about 'lost' commits from a detached HEAD state instead of using git reflog to recover them.",
        ],
        glossary=[
            dict(term="Branch", definition="A lightweight, movable pointer to a specific commit, used to develop changes in isolation from other lines of work."),
            dict(term="HEAD", definition="A special pointer indicating the currently checked-out commit, typically pointing at a branch name which in turn points at a commit."),
            dict(term="Detached HEAD", definition="A state where HEAD points directly at a specific commit rather than a branch name, risking unreachable commits if you switch away without creating a branch."),
            dict(term="git reflog", definition="A log of every recent position HEAD has pointed to, a safety net for recovering seemingly lost commits."),
        ],
        faq=[
            dict(q="Walk me through resolving this merge conflict step by step.", a="Git marks the conflicting section directly in the file with <<<<<<<, =======, and >>>>>>> markers showing both versions. Edit the file to the correct final combined version, remove the conflict markers, then git add the resolved file and git commit to complete the merge."),
            dict(q="What's the difference between a fast-forward merge and a merge commit?", a="A fast-forward merge happens when the target branch hasn't diverged at all — Git simply moves the branch pointer forward, no new commit needed. A merge commit is created when both branches have new, divergent commits, combining both histories with a commit that has two parents."),
            dict(q="When should I create a new branch versus just committing directly to main?", a="Create a branch for any non-trivial change, especially anything that might take more than a few minutes or might need review before being considered done — keeping main stable and always in a working, deployable state."),
        ],
        quiz=[
            dict(
                question="What happens to commits made in a detached HEAD state if you switch to another branch without creating a new branch first?",
                options=["They're automatically merged into main", "They can become unreachable and eventually garbage collected", "Git refuses to let you switch", "They're saved automatically as a new branch"],
                correct=1,
                explanation="Without a branch pointer keeping them reachable, commits made in a detached HEAD state can become orphaned once you switch away — git reflog is the recovery tool if this happens before they're garbage collected.",
            ),
        ],
        prompts=[
            "Walk me through resolving this merge conflict step by step.",
            "What's the difference between a fast-forward merge and a merge commit?",
            "When should I create a new branch versus just committing directly to main?",
            "How do I recover commits I made in a detached HEAD state?",
        ],
    ),
    dict(
        id="merge-vs-rebase",
        title="Merge vs. Rebase",
        hook="Both merge and rebase combine work from two branches — they just leave a completely different-looking history behind, which matters more than most people expect.",
        explanation=(
            "`git merge` combines two branches by creating a new merge commit that has both branch tips as "
            "parents, preserving the exact history of when each branch's commits happened — the history shows "
            "branches diverging and reconnecting. `git rebase` takes the commits from one branch and replays "
            "them, one by one, on top of another branch's latest commit, producing a clean, linear history as if "
            "the work had happened sequentially — but it rewrites commit hashes in the process.\n\n"
            "The trade-off is real: merge preserves true history but can look messy with many branches; rebase "
            "produces a clean, linear log but rewrites history, which is dangerous on any branch other people "
            "have already pulled from, because their local history and the rewritten remote history will diverge.\n\n"
            "Interactive rebase (`git rebase -i`) goes beyond simply replaying commits — it lets you reorder, "
            "combine (squash), edit, or drop individual commits before they're replayed, making it a powerful "
            "tool for cleaning up a messy sequence of 'WIP' and 'fix typo' commits into a clean, readable "
            "history before merging or opening a pull request."
        ),
        deep_dive=(
            "Squash merging (a common option on GitHub/GitLab pull requests) takes an entirely different "
            "approach — it combines every commit from a feature branch into a single new commit on the target "
            "branch, discarding the individual commit history of the feature branch entirely in favor of one "
            "clean, summarizing commit. This is a popular middle ground for teams that want main's history to "
            "read as one commit per feature/PR, without needing every contributor to manually rebase and clean "
            "up their own commits first.\n\n"
            "The 'golden rule' of rebasing — never rebase a branch that others have already pulled and built "
            "work on top of — exists because rebasing creates entirely new commits with new hashes; anyone who "
            "already has the old commits will end up with a diverged, confusing history once they try to "
            "reconcile their local copy with the rewritten remote one, typically requiring manual, error-prone "
            "conflict resolution to untangle.\n\n"
            "`git rebase --onto` supports more surgical rebasing operations, like moving a range of commits "
            "from one base onto a different one entirely, useful in more complex scenarios like extracting a "
            "sub-feature's commits out of a branch that accidentally included unrelated work."
        ),
        code=dict(
            lang="bash",
            label="Rebasing a feature branch onto an updated main",
            src=(
                "git checkout feature/user-auth\n"
                "git fetch origin\n"
                "git rebase origin/main         # replay your commits on top of the latest main\n\n"
                "# if conflicts occur during rebase, resolve them, then:\n"
                "git add resolved_file.py\n"
                "git rebase --continue\n\n"
                "# NEVER rebase a branch that others have already pulled and built on top of"
            ),
        ),
        advanced_code=dict(
            lang="bash",
            label="Interactive rebase to clean up messy commits before opening a PR",
            src=(
                "git rebase -i HEAD~4    # interactively edit the last 4 commits\n\n"
                "# Opens an editor showing something like:\n"
                "# pick a1b2c3d Add login form\n"
                "# pick d4e5f6g fix typo\n"
                "# pick g7h8i9j WIP\n"
                "# pick j1k2l3m actually fix the bug\n\n"
                "# Change to:\n"
                "# pick a1b2c3d Add login form\n"
                "# squash d4e5f6g fix typo\n"
                "# squash g7h8i9j WIP\n"
                "# squash j1k2l3m actually fix the bug\n"
                "# -> combines all 4 into one clean commit before merging"
            ),
        ),
        example=(
            "A solo developer's local feature branch rebases cleanly onto an updated main before opening a pull "
            "request, producing a tidy, linear commit history for reviewers — but rebasing a shared `main` "
            "branch that three teammates already pulled would rewrite history under their feet and break their local repos."
        ),
        best_practices=[
            "Rebase your own local, not-yet-shared feature branches to keep history clean before opening a pull request.",
            "Use merge (never rebase) for any branch that other people have already pulled from or based work on.",
            "Use interactive rebase to squash noisy 'fix typo'/'WIP' commits into clean, meaningful ones before a PR review.",
            "If a team values a fully linear history, standardize on 'rebase before merging, merge with a fast-forward or squash' as the shared convention, rather than mixing strategies inconsistently.",
        ],
        pitfalls=[
            "Rebasing a shared branch and force-pushing it, silently breaking every teammate's local copy of that branch's history.",
            "Treating rebase as strictly 'better' than merge without considering that it discards the true chronological record of when work actually happened.",
            "Getting stuck mid-rebase due to conflicts and not knowing about `git rebase --abort` to safely back out entirely.",
        ],
        glossary=[
            dict(term="Rebase", definition="Replaying a branch's commits on top of a different base commit, producing new commit hashes and a linear history."),
            dict(term="Interactive rebase", definition="A rebase mode letting you reorder, squash, edit, or drop individual commits before they're replayed."),
            dict(term="Squash merge", definition="Combining every commit from a feature branch into one new commit on the target branch, discarding individual commit history."),
        ],
        faq=[
            dict(q="Is it safe to rebase this specific branch, and how do I check?", a="Safe if it's a local branch only you have pushed to, or one you're certain no one else has pulled from yet. Check with your team or via your Git host's UI whether anyone else has fetched that branch before rebasing and force-pushing it."),
            dict(q="What does 'rewriting history' actually mean in terms of commit hashes?", a="Since a commit's hash depends partly on its parent's hash, replaying a commit onto a new base changes its parent, which changes its own hash, cascading forward — every commit after the rebase point gets a genuinely new hash, even if its actual content (the diff) is identical to before."),
            dict(q="Explain squash merging and when a team would want it.", a="Squash merging combines an entire feature branch's commits into one single commit on the target branch. Teams that want one clean commit per feature or pull request, without needing individual contributors to manually clean up their own messy commit history first, commonly use this as their default merge strategy."),
        ],
        quiz=[
            dict(
                question="Why is rebasing a shared branch that others have already pulled considered dangerous?",
                options=["It's not actually dangerous", "Rebasing creates new commit hashes, causing anyone with the old commits to have a diverged, conflicting history", "Rebase only works on local branches technically", "It deletes the branch entirely"],
                correct=1,
                explanation="Because rebase rewrites commit hashes, anyone who already pulled the original commits will find their local history has diverged from the rewritten remote history, typically requiring manual, confusing reconciliation.",
            ),
        ],
        prompts=[
            "Is it safe to rebase this specific branch, and how do I check?",
            "What does 'rewriting history' actually mean in terms of commit hashes?",
            "Explain squash merging and when a team would want it.",
            "Walk me through using interactive rebase to clean up my last 5 commits.",
        ],
    ),
    dict(
        id="remotes-collaboration",
        title="Remotes, Push/Pull & Pull Requests",
        hook="Your local repository and GitHub's copy are two independent histories that only sync when you explicitly tell them to — nothing updates automatically.",
        explanation=(
            "A remote is a named reference to another copy of the repository, most commonly `origin`, pointing "
            "at GitHub. `git push` sends your local commits to the remote; `git pull` (a fetch plus a merge) "
            "brings the remote's new commits into your local branch. Because Git is distributed, your local "
            "repository is a complete, independent copy of the full history — GitHub isn't the 'real' repository "
            "with everyone else working on partial copies, it's just the commonly-agreed shared point of sync.\n\n"
            "A pull request (GitHub's term; GitLab calls it a merge request) is a request to merge one branch "
            "into another, built around a diff, discussion thread, and often automated checks (CI). It's a "
            "GitHub feature layered on top of Git, not a Git concept itself — plain Git has no notion of a pull request.\n\n"
            "`git fetch` downloads a remote's new commits and updates your local tracking references, without "
            "touching your current working branch at all — it's the safe, non-destructive half of what `git "
            "pull` does. `git pull` is really just `git fetch` immediately followed by a merge (or, "
            "configurable, a rebase) of those fetched commits into your current branch, which is why `git "
            "pull` can trigger a merge conflict, while `git fetch` alone never can."
        ),
        deep_dive=(
            "Forking (creating your own full copy of someone else's repository under your account) versus "
            "branching (creating a new line of work within the same repository) serve different collaboration "
            "models: forking is standard for open-source contribution where you don't have direct push access "
            "to the original repository, while branching directly is standard within a team that shares push "
            "access to one repository.\n\n"
            "Protected branches (a GitHub/GitLab feature, not a core Git concept) let a repository require "
            "certain conditions — passing CI checks, at least one approving review, no force-pushes — before "
            "a pull request can be merged into a specific branch like `main`, enforcing team process and "
            "quality gates directly at the platform level rather than relying purely on convention and trust.\n\n"
            "`git push --force-with-lease` is a safer alternative to a plain `git push --force` after rewriting "
            "local history — it refuses to overwrite the remote branch if someone else has pushed new commits "
            "to it since you last fetched, preventing you from accidentally clobbering a teammate's work that "
            "you simply hadn't seen yet."
        ),
        code=dict(
            lang="bash",
            label="The push/pull collaboration loop",
            src=(
                "git remote -v                       # see configured remotes\n"
                "git checkout -b fix/login-bug\n"
                "git commit -am \"Fix null check on login\"\n"
                "git push -u origin fix/login-bug     # push branch, set upstream tracking\n"
                "# ... open a pull request on GitHub ...\n\n"
                "git checkout main\n"
                "git pull origin main                 # get everyone else's merged changes"
            ),
        ),
        advanced_code=dict(
            lang="bash",
            label="Safer force-pushing after rewriting local history",
            src=(
                "# After an interactive rebase that rewrote your feature branch's commits:\n"
                "git push --force-with-lease origin feature/user-auth\n\n"
                "# This REFUSES to push if someone else pushed new commits to this\n"
                "# branch since your last fetch -- protecting against accidentally\n"
                "# overwriting work you simply hadn't seen yet\n\n"
                "# Plain --force would overwrite unconditionally -- riskier"
            ),
        ),
        example=(
            "A contributor forks an open-source repository, pushes commits to their own fork's branch, and opens "
            "a pull request against the original project — the maintainers review the diff, request changes, "
            "and eventually merge it, all without the contributor ever having direct push access to the original repository."
        ),
        best_practices=[
            "Pull before you start new work each session to reduce the chance of a large conflict later.",
            "Use `-u` (`git push -u origin branch-name`) the first time you push a new branch so future `git push`/`git pull` know which remote branch to sync with.",
            "Write pull request descriptions that explain the 'why,' link related issues, and call out anything reviewers should pay special attention to.",
            "Use `--force-with-lease` instead of plain `--force` when you need to force-push after rewriting your own branch's history.",
        ],
        pitfalls=[
            "Force-pushing (`git push --force`) to a shared branch without coordinating with the team, overwriting commits others have already pushed.",
            "Assuming `git pull` is always safe — it performs a merge under the hood, which can introduce a conflict you weren't expecting mid-task.",
            "Confusing forking (a separate repository copy, for open-source contribution) with branching (a new line of work within the same repository, for team collaboration).",
        ],
        glossary=[
            dict(term="Remote", definition="A named reference to another copy of a repository, most commonly `origin`, used for pushing and pulling."),
            dict(term="Pull request / merge request", definition="A GitHub/GitLab feature requesting that one branch be merged into another, with review and discussion built around the diff."),
            dict(term="Fork", definition="A full, independent copy of someone else's repository under your own account, standard for open-source contribution without direct push access."),
            dict(term="Protected branch", definition="A platform-level setting requiring conditions (passing checks, reviews) before a branch like main can be updated via merge."),
        ],
        faq=[
            dict(q="What's the difference between git fetch and git pull?", a="git fetch downloads new commits from the remote and updates tracking references, without touching your current working branch at all — completely safe. git pull does that same fetch, then immediately merges (or rebases) those commits into your current branch, which can trigger a conflict."),
            dict(q="How do I safely force-push after rewriting my own feature branch's history?", a="Use `git push --force-with-lease` instead of plain `--force` — it checks that the remote branch hasn't changed since you last fetched it, refusing the push (rather than silently overwriting) if someone else has pushed commits you haven't seen."),
            dict(q="Explain what happens under the hood when I open a pull request.", a="GitHub compares the commits on your source branch against the target branch, computing a diff and a list of commits unique to your branch — it's purely a review/discussion wrapper around that comparison; the actual merge only happens when you (or a reviewer) explicitly click merge, which runs a real git merge (or squash/rebase, depending on settings) on GitHub's servers."),
        ],
        quiz=[
            dict(
                question="What's the key difference between git fetch and git pull?",
                options=["They're identical commands", "fetch only downloads and updates tracking refs; pull also merges those changes into your current branch", "fetch is only for the first clone", "pull never touches the remote"],
                correct=1,
                explanation="git fetch safely downloads new commits without touching your working branch; git pull additionally merges (or rebases) those fetched commits into your current branch, which can produce a conflict.",
            ),
        ],
        prompts=[
            "What's the difference between git fetch and git pull?",
            "How do I safely force-push after rewriting my own feature branch's history?",
            "Explain what happens under the hood when I open a pull request.",
            "What's the difference between forking a repository and creating a branch?",
        ],
    ),
    dict(
        id="gitignore-clean-repos",
        title=".gitignore & Keeping a Repository Clean",
        hook="A repository with build artifacts, secrets, and dependency folders tracked in it isn't just messy — it's a genuine security and collaboration risk.",
        explanation=(
            "`.gitignore` is a plain text file listing patterns for files and folders Git should never track: "
            "dependency directories (`node_modules/`, `venv/`), build output, OS-generated files (`.DS_Store`), "
            "IDE settings, and — critically — anything containing secrets, like `.env` files with API keys. Git "
            "matches these patterns whenever you run `git add` or `git status`, silently skipping anything that "
            "matches.\n\n"
            "`.gitignore` only prevents newly created files from being tracked — it does nothing for a file "
            "that's already committed. If a secret was committed even once, it exists permanently in the "
            "repository's history and must be actively removed (and the secret rotated), not just added to "
            ".gitignore going forward.\n\n"
            "`.gitignore` patterns support wildcards (`*.log` matches every file ending in `.log`), directory-"
            "specific matches (a trailing slash like `build/` matches only directories), and negation (`!keep-"
            "this.log` re-includes a file that would otherwise match an earlier broader pattern) — giving fine "
            "control over exactly what gets excluded without needing separate rules for every single file."
        ),
        deep_dive=(
            "`git rm --cached <file>` removes a file from Git's tracking going forward while leaving it "
            "untouched on disk — the standard first step when you realize a file should have been ignored from "
            "the start but was already committed; you'd then add it to `.gitignore` so it doesn't get "
            "re-tracked on the next `git add .`.\n\n"
            "Tools like `git-secrets` or `gitleaks` scan commits (including historical ones, and can be wired "
            "into a pre-commit hook to catch new secrets before they're ever committed) for patterns that look "
            "like API keys, credentials, or other sensitive data — an automated safety net considerably more "
            "reliable than hoping every contributor remembers to manually check before every commit.\n\n"
            "`git filter-repo` (the modern, recommended replacement for the older `git filter-branch`) can "
            "rewrite a repository's entire history to remove a file (and all traces of it) from every commit "
            "it ever appeared in — a genuinely disruptive operation requiring every collaborator to re-clone "
            "the repository afterward, which is exactly why rotating the leaked secret immediately is the "
            "priority, with history-scrubbing treated as a secondary cleanup step rather than the primary fix."
        ),
        code=dict(
            lang="text",
            label="A typical Python project .gitignore",
            src=(
                "__pycache__/\n"
                "*.pyc\n"
                "venv/\n"
                ".env\n"
                ".DS_Store\n"
                "*.log\n"
                "dist/\n"
                "build/\n"
                ".vscode/\n"
                ".idea/"
            ),
        ),
        advanced_code=dict(
            lang="bash",
            label="Removing an accidentally-tracked file, and negation patterns",
            src=(
                "# .gitignore was added AFTER config.env was already committed --\n"
                "# adding it to .gitignore alone does nothing retroactively:\n"
                "git rm --cached config.env       # stop tracking it, keep it on disk\n"
                "echo \"config.env\" >> .gitignore   # prevent it from being re-added\n"
                "git commit -m \"Stop tracking config.env\"\n\n"
                "# .gitignore negation pattern example:\n"
                "# *.log          -- ignore all log files\n"
                "# !important.log -- EXCEPT this specific one, which should still be tracked"
            ),
        ),
        example=(
            "A team discovers an AWS key was accidentally committed six months ago; adding `.env` to "
            ".gitignore now does nothing to remove it from history, so the correct response is to immediately "
            "rotate (invalidate and reissue) the key and separately scrub the file from history with a tool like "
            "`git filter-repo`, treating the leaked key as compromised regardless."
        ),
        best_practices=[
            "Add a `.gitignore` file at the very start of a project, before the first commit, using a language-specific template (GitHub provides one for nearly every stack).",
            "Never store real secrets in a file that's ever been committed, even temporarily — use environment variables loaded from an untracked `.env` file instead.",
            "If a secret does leak into history, treat it as compromised and rotate it immediately; scrubbing history is a secondary cleanup step, not the primary fix.",
            "Use an automated secret-scanning tool (like gitleaks) as a pre-commit hook to catch potential leaks before they're ever committed.",
        ],
        pitfalls=[
            "Assuming adding a file to `.gitignore` retroactively removes it from a repository's history.",
            "Committing a `.env` file 'just this once for convenience' and forgetting to remove it before pushing.",
            "Using the older, more error-prone `git filter-branch` instead of the modern, recommended `git filter-repo` for history-rewriting operations.",
        ],
        glossary=[
            dict(term=".gitignore", definition="A file listing patterns for files and directories Git should never track, preventing them from being staged going forward."),
            dict(term="git rm --cached", definition="Removes a file from Git's tracking while leaving it untouched on disk, the standard fix for a file that should have been ignored from the start."),
            dict(term="git filter-repo", definition="A tool for rewriting a repository's entire history, capable of removing a file (and all traces of it) from every commit it ever appeared in."),
        ],
        faq=[
            dict(q="What should a .gitignore for a Flask project include?", a="Typically: __pycache__/, *.pyc, venv/ or .venv/, .env, instance/ (Flask's instance folder, often holding local config/secrets), .DS_Store, and any build/dist output directories — GitHub's Python .gitignore template covers most of these as a solid starting point."),
            dict(q="I accidentally committed a secret — what are the exact steps to fix this?", a="First and most importantly, rotate the secret immediately (invalidate the old key/credential and issue a new one) since it must be treated as compromised regardless of what you do next. Then, as cleanup, use git filter-repo (or a platform-specific tool) to scrub it from history, and notify anyone who may have already cloned the repository that they'll need to re-clone after the history rewrite."),
            dict(q="How is git filter-repo different from just deleting a file in a new commit?", a="Deleting a file in a new commit only removes it going forward — the file still exists in every earlier commit's history and can be retrieved from there. git filter-repo actually rewrites every historical commit to remove all trace of the file, changing every subsequent commit's hash in the process."),
        ],
        quiz=[
            dict(
                question="If a secret was already committed, does adding it to .gitignore afterward remove it from history?",
                options=["Yes, immediately", "No -- .gitignore only prevents future tracking, the secret remains in prior commits", "Only if you also run git commit again", "Only on GitHub, not local repositories"],
                correct=1,
                explanation=".gitignore has no effect on already-committed content — a leaked secret remains in the repository's history until explicitly removed with a history-rewriting tool, and should be rotated regardless.",
            ),
        ],
        prompts=[
            "What should a .gitignore for a Flask project include?",
            "I accidentally committed a secret — what are the exact steps to fix this?",
            "How is git filter-repo different from just deleting a file in a new commit?",
            "Show me how to remove a file from Git tracking without deleting it from disk.",
        ],
    ),
]