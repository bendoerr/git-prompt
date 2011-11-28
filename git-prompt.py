from git import *
from colorama import init, Fore, Back, Style

try:
    repo = Repo()                                                               #=> <git.Repo "/cygdrive/c/sanctuary/projects/git-prompt/.git">
except InvalidGitRepositoryError:
    exit()

init()

remote_color = Style.BRIGHT + Fore.RED

curr_b = repo.head.ref.name                                                     #=> 'master'
curr_tb = repo.head.ref.tracking_branch()                                       #=> <git.RemoteReference "refs/remotes/origin/master">

if curr_tb:
    curr_rb = curr_tb.name.split("/")                                           #=> {'origin', 'master'}

    curr_commit = repo.head.commit.hexsha                                       #=> '6b800a2fe00d33b3b953eda423438f03c3d59320'
    curr_r_commit = Git().ls_remote(curr_rb[0],
                                    "refs/heads/" + curr_rb[1]).split("\t")[0]  #=> 'bf1e66aa5ec90325bf358469d1b13fac6777c045'

    if curr_commit != curr_r_commit:
        # We differ. We might be ahead (curr_rb_commit would be in our history).
        # We might be behind (curr_commit is in their history) or we might have
        # diverged.
        remote_color = Fore.MAGENTA
    else:
        remote_color = Fore.WHITE

not_staged = repo.index.diff(None)
staged = repo.index.diff('HEAD')

local_color = Fore.WHITE

if bool(staged):
    if bool(not_staged):
        local_color = Fore.YELLOW
    else:
        local_color = Fore.GREEN
elif bool(not_staged):
    local_color = Fore.RED

print remote_color + "(" + Style.RESET_ALL + local_color + curr_b + Style.RESET_ALL + remote_color + ")" + Style.RESET_ALL