# Reflective Note: Merge Conflicts and Distributed Version Control

## The project

I built a small command-line calculator in Python (`calculator.py`) with unit tests
(`test_calculator.py`) and kept it in Git, with a GitHub remote
(https://github.com/Shreshth064/git-merge-conflict-calculator). The program is simple on
purpose. The point of the exercise was the Git workflow: making a repository, connecting
it to GitHub, working on feature branches, merging them, and handling a merge conflict.

## What caused the conflict

I made two feature branches from the same commit on `main`.

- `feature/zero-division-check` changed `divide()` so that it raises
  `ZeroDivisionError("Cannot divide by zero")` when the divisor is 0.
- `feature/rounded-division` changed the same `return a / b` line to
  `return round(a / b, 2)`.

Each branch also added a line in the same place in `README.md` and a new test in the same
place in `test_calculator.py`.

I merged the zero-check branch into `main` first. That merge was clean because `main` had
not changed since the branch was created. When I then merged the rounding branch, Git
did a three-way merge. It compared the common ancestor (the original `return a / b`), the
version now on `main`, and the version on the branch. Both sides had changed the same lines
in different ways, and Git cannot know which change I wanted, so it stopped and reported
`CONFLICT (content)` in all three files. A conflict is not an error. It is Git refusing to
guess when two people have edited the same lines.

## How I resolved it

1. **Understanding the problem.** `git status` listed the three files as *both modified*
   and said I was in the middle of a merge. `git diff` showed both sides of each conflict.
   `git diff --name-only --diff-filter=U` listed just the unmerged files.
2. **Reading the markers.** In each file Git had written the `main` version between
   `<<<<<<< HEAD` and `=======`, and the incoming version between `=======` and
   `>>>>>>> feature/rounded-division`.
3. **Choosing the result.** The two changes did not actually contradict each other.
   Checking for zero and rounding the result both made sense, so instead of keeping only
   "ours" or only "theirs" I wrote a combined version: check for zero first, then return
   `round(a / b, 2)`. I kept both README lines and both tests.
4. **Checking the result.** I used `grep` to make sure no conflict markers were left, staged
   the files with `git add` (which tells Git a file is resolved), and ran the tests. All
   seven passed, including the tests from both branches. That showed the combined code did
   what each branch meant to do.
5. **Finishing.** `git commit` created a merge commit with two parents, and `git push` sent
   it to GitHub. `git log --graph` shows both branches joining into `main`.

I also used `git restore` to throw away an accidental edit. I used `git pull` to bring in a
commit that I had pushed from a second clone of the repository, standing in for a teammate
on another machine.

## What I learned about distributed version control

**Every clone is a full repository.** My local folder and the second clone each had the
complete history, and each could make commits without the other. GitHub was just a shared
place where we both pushed and pulled. That is why work can continue offline and why no
single server holds the only copy of the history.

**Branches are cheap, and merging is where the work comes together.** Making a branch is
instant, so it makes sense to put every feature on its own branch. The price is that
branches drift apart, and the longer two branches change the same code, the more likely a
conflict becomes. Merging, pulling and pushing often keeps branches close to `main` and
keeps conflicts small.

**Git merges text, not meaning.** Git found the conflict because the same lines changed.
It would not have noticed two changes on different lines that break each other. That is
why running the tests after resolving mattered: a merge with no markers left is not
automatically correct.

**Resolving a conflict is a decision.** The easy fix is to keep one side, but that would have
quietly thrown away a teammate's work. Reading both versions and understanding why each was
written led to a better result than either branch on its own.

**There are several ways to resolve a conflict.** `git merge --abort` cancels a merge safely.
`git checkout --ours/--theirs` takes one side wholesale. `git restore` throws away unwanted
changes in the working copy. `git rebase` lets you fix the conflict on your own branch before
merging, which gives a straighter history. Knowing these options means a conflict is
something to work through calmly, not something to be afraid of.

Overall, creating a conflict on purpose took away the mystery. The markers, the `git status`
messages and the merge commit all make sense once you see that Git is recording two lines
of work and asking a person to decide where they disagree.
