# CONTRIBUTING

## Code style

This project follows PEP 8 guidelines with the following modifications:

* Recommended line length is 80 characters or fewer
* Maximum line length is 100 characters

## Git

The [triangle workflow][triangle-workflow] is the suggested git workflow for
this project.

Specific rules regarding the git workflow are as follows:

* Do **NOT** break the build on `master`
* Committing directly to `master` is prohibited (always use PRs)
* Have at least 1 person review your PR before merging
* Squash-merge and rebase are allowed, while merge-by-pull is prohibited

### Commit Message Guidelines

This project follows the
[conventional changelog format][conventional-changelog-format], so that we can
easily update the `CHANGELOG.md` programatically.

Full information can be found at the link above, but essentially:

* Format your commit subject line using the following format:
  `TYPE(SCOPE): MESSAGE` where `TYPE` is one of the following:
    - `feat` - A new feature
    - `impr` - An improvement to an existing feature
    - `perf` - A performance improvement
    - `docs` - Changes to documentation only
    - `tests` - Changes to the testing framework or tests only
    - `fix` - A bug fix
    - `refactor` - Code functionality doesn't change, but underlying structure
      may
    - `style` - Stylistic changes only, no functionality changes
    - `wip` - A work in progress commit (Should typically be `git rebase`'ed
      away)
    - `chore` - Catch all or things that have to do with the build system, etc.
    - `examples` - Changes to an existing example, or a new examples
* The `(SCOPE)` is optional, and may be a single file, directory, or logical
  component.
* For the subject message:
    * use the imperative, present tense: "change" not "changed" nor "changes"
    * don't capitalize first letter
    * no dot (.) at the end
* For the commit message body:
    * Just as in the subject, use the imperative, present tense: "change" not
      "changed" nor "changes".
      The body should include the motivation for the change and contrast this
      with previous behavior.

Example commit message:

```
feat: add cog for music functionality

Add music functionality cog with ability to play or pause music.
```

[conventional-changelog-format]: https://github.com/angular/angular.js/blob/master/CONTRIBUTING.md#commit
[pep8]: https://www.python.org/dev/peps/pep-0008/
[triangle-workflow]: https://www.sociomantic.com/blog/2014/05/git-triangular-workflow/
