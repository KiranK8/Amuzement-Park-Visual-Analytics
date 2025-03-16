## How to keep your repository up to date

Your repository for the assignments is a fork of the template repository that we maintain. 
Each group has their own fork.
In software development parlance our repository is called *upstream* and yours *downstream*.
As we will only update the upstream repository (and not each group's)
you have to take care of keeping your repository up to date yourself.

Whenever we make larger changes that we want you to get, we will write an OLAT News.

Because conflicting files may have to be merged manually after you have worked on an assignment, we suggest that **only one member of your group does the update procedure** and the others just pull the updated state later.


### Initialize updates

We recommend to work from the command line (rather than the GitLab GUI)
so you can fix merge conflicts more easily.

Working on your local clone of your repository, add *upstream* to your *remote* repositories (change XX to the last digits of the current year).

```console
$ git remote add upstream https://gitlab.rhrk.uni-kl.de/assignments/visanaXX/template.git
```


### Fetch updates

Get all the upstream info.

```console
$ git fetch upstream
```

Remember that you always merge implicitly into the currently checked out branch.
So make sure you are where you want to be (we suggest your *main* branch).

```console
$ git status
```

Merge (try to merge) upstream changes into your downstream repository.

```console
$ git merge upstream/main
```

If the automatic merge has worked, you see a text editor with a prepared commit message.
Save and quit, and push.

```console
$ git push
```


### Fix conflicts

It may happen that there are conflicts between the changes you made to your 
repository and the upstream repository. In this case git is not able to merge 
automatically and gives a warning that looks something like this:

```
CONFLICT (add/add): Merge conflict in docs/updateDownstream.md
Automatic merge failed; fix conflicts and then commit the result.
```

Git tells you which files have conflicts. In the case above it is *docs/updateDownstream.md*.

If you are sure you want to keep all changes from upstream,
dismissing all of your own changes that have caused a conflict, you can do
`git checkout --theirs docs/updateDownstream.md`.
If, on the other hand, you want to ignore all conflicting upstream changes, you can do
`git checkout --ours docs/updateDownstream.md`.

If the above technique is not applicable, open the file and search for passages with the following pattern.

```
<<<<<<< HEAD your version
=======
changed version from the template >>>>>>> template/main
```

Then fix the merge conflicts there manually.

In any case, commit as usual.

```console
$ git add docs/updateDownstream.md  # substitute the affected file(s)
$ git commit -m "Resolve merge conflict by incorporating both suggestions."
$ git push
```
