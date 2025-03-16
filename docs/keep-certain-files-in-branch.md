## Mainly intended for the lecture staff

How to keep files or directories, that are special to a certain branch, the way they are when
merging another branch where these files don't exist or have been changed.

Howto based on this [blog post](https://medium.com/@porteneuve/how-to-make-git-preserve-specific-files-while-merging-18c92343826b).

The following has to be done by each user,
and it seems to be platform dependent (the `true` part).

`git config --global merge.ours.driver true`

Create a `.gitattributes` file similar to `.gitignore` (#-comments, \*-globs) with
content like the following, assuming there is a file *branchSpecificReadme.md*.

```
# file .gitattributes
branchSpecificReadme.md merge=ours
```

Make sure to commit this change before the next merge.

`git add .gitattributes`  
`git commit -m"Add .gitattributes to preserve branch-specific files during merges"`
