# How to Delete a Git Branch

This guide explains how to delete Git branches both locally and remotely.

## Prerequisites

Before deleting a branch, ensure that:
- You have committed and pushed any important changes
- You have merged the branch if needed
- You are not currently on the branch you want to delete

## Deleting a Local Branch

### Delete a Fully Merged Branch

To delete a local branch that has been fully merged:

```bash
git branch -d branch-name
```

Example:
```bash
git branch -d copilot/delete-branch
```

This is a "safe" delete that will prevent you from deleting a branch with unmerged changes.

### Force Delete a Branch

To delete a branch regardless of its merge status:

```bash
git branch -D branch-name
```

⚠️ **Warning:** This will permanently delete the branch and any unmerged changes.

## Deleting a Remote Branch

To delete a branch from the remote repository (e.g., GitHub):

```bash
git push origin --delete branch-name
```

Example:
```bash
git push origin --delete copilot/delete-branch
```

### Alternative Syntax

You can also use this alternative syntax:

```bash
git push origin :branch-name
```

## Complete Workflow Example

Here's a complete example of deleting both local and remote branches:

```bash
# 1. Switch to a different branch (e.g., main)
git checkout main

# 2. Delete the local branch
git branch -d copilot/delete-branch

# 3. Delete the remote branch
git push origin --delete copilot/delete-branch
```

## Verification

### Check Local Branches

To verify the branch has been deleted locally:

```bash
git branch
```

### Check Remote Branches

To see all remote branches:

```bash
git branch -r
```

Or update your remote branch list:

```bash
git fetch --prune
```

## Common Scenarios

### Scenario 1: Delete Current Branch

You cannot delete the branch you're currently on. First, switch to another branch:

```bash
git checkout main
git branch -d old-branch
```

### Scenario 2: Branch Not Fully Merged

If you try to delete a branch with unmerged changes, Git will warn you:

```
error: The branch 'branch-name' is not fully merged.
```

You can either:
- Merge the branch first: `git merge branch-name`
- Force delete if you're sure: `git branch -D branch-name`

### Scenario 3: Delete Multiple Branches

To delete multiple branches at once:

```bash
git branch -d branch1 branch2 branch3
```

## Best Practices

1. **Always verify** which branch you're on before deleting: `git branch`
2. **Merge important changes** before deleting
3. **Use `-d` instead of `-D`** when possible for safety
4. **Delete remote branches** after deleting local branches to keep repositories clean
5. **Clean up regularly** to avoid branch clutter

## Troubleshooting

### Error: "branch not found"

Make sure the branch name is correct:
```bash
git branch -a  # List all branches to find the correct name
```

### Error: "refusing to delete the current branch"

Switch to a different branch first:
```bash
git checkout main
```

### Remote branch still appears after deletion

Update your local repository's remote branch list:
```bash
git fetch --prune
```

## Additional Resources

- [Git Documentation - Branch Management](https://git-scm.com/book/en/v2/Git-Branching-Branch-Management)
- [GitHub Documentation - Managing Branches](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches)
