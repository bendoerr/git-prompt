from git import *
from colorama import init, Fore, Back, Style
from sys import argv
from git_prompt_remote import *

try:
    repo = Repo()                                                           #=> <git.Repo "/cygdrive/c/sanctuary/projects/git-prompt/.git">
except InvalidGitRepositoryError:
    exit()

# Initialize Colorama
init()

curr_tb = repo.head.ref.tracking_branch()                                   #=> <git.RemoteReference "refs/remotes/origin/master">

remote_color = Style.BRIGHT + Fore.RED
if curr_tb:
    invalidateCache = True if len(argv) > 1 and str(argv[1]) == "invalidate" else False
    remote_status = check_status_with_remote(repo, curr_tb, invalidateCache)

    if remote_status == LocalRemoteState.UP_TO_DATE:
        remote_color = Fore.WHITE
    elif remote_status == LocalRemoteState.AHEAD:
        remote_color = Fore.YELLOW
    elif remote_status == LocalRemoteState.BEHIND:
        remote_color = Fore.MAGENTA
    elif remote_status == LocalRemoteState.DIVERGED:
        remote_color = Back.MAGENTA + Style.BRIGHT + Fore.WHITE

not_staged = repo.index.diff(None)                                          #=> [<git.diff.Diff object at 0x7ecafa74>]
staged = repo.index.diff('HEAD')                                            #=> [<git.diff.Diff object at 0x7ecafa74>]

local_color = Fore.WHITE
if bool(staged):
    if bool(not_staged):
        local_color = Fore.YELLOW
    else:
        local_color = Fore.GREEN
elif bool(not_staged):
    local_color = Fore.RED

curr_b = repo.head.ref.name                                                 #=> 'master'
print remote_color + "(" + Style.RESET_ALL + local_color + curr_b + Style.RESET_ALL + remote_color + ")" + Style.RESET_ALL