from git import *

repo = Repo()                                                                   #=> <git.Repo "/cygdrive/c/sanctuary/projects/git-prompt/.git">

curr_b = repo.head.ref.name                                                     #=> 'master'
curr_tb = repo.head.ref.tracking_branch()

if curr_tb:
    curr_rb = curr_tb.name.split("/")                                               #=> {'origin', 'master'}

    curr_commit = repo.head.commit.hexsha                                           #=> '6b800a2fe00d33b3b953eda423438f03c3d59320'
    curr_rb_commit = Git().ls_remote(curr_rb[0],
                                     "refs/heads/" + curr_rb[1]).split("\t")[0]     #=> 'bf1e66aa5ec90325bf358469d1b13fac6777c045'

    if curr_commit != curr_rb_commit:
        # We differ. We might be ahead (curr_rb_commit would be in our history). We
        # might be behind (curr_commit is in their history) or we might have
        # diverged.
        print("Out of sync")
    else:
        print("Up to date")

not_staged = bool(repo.index.diff(None))
staged = bool(repo.index.diff('HEAD'))

if not_staged:
    print("Has Items Not Staged")

if staged:
    print("Has Items Staged")