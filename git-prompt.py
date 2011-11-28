from git import *
from colorama import init, Fore, Back, Style

try:
    repo = Repo()                                                               #=> <git.Repo "/cygdrive/c/sanctuary/projects/git-prompt/.git">
except InvalidGitRepositoryError:
    exit()

# Initialize Colorama
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
        remote_commits = Git().cherry(curr_b, "remotes/" + curr_tb.name)        #=> ''
        local_commits = Git().cherry()                                          #=> ''

        if bool(remote_commits) == False and bool(local_commits) == False:
            repo.remote(curr_rb[0]).fetch()

        remote_commits = Git().cherry(curr_b, "remotes/" + curr_tb.name)        #=> '+ cb601efd16ecb322c349378a4393620e7b05301c'
        local_commits = Git().cherry()                                          #=> '+ a305fad893e72ca4ad78171b18977227cb61bf25\n+ 4155609d8350c0112280b419df6b0f6c7ec641b7'

        if bool(remote_commits):
            if bool(local_commits):
                # Diverged
                remote_color = Back.MAGENTA + Style.BRIGHT + Fore.WHITE
            else:
                remote_color = Fore.MAGENTA
        elif bool(local_commits):
            remote_color = Fore.YELLOW
    else:
        remote_color = Fore.WHITE

not_staged = repo.index.diff(None)                                              #=> [<git.diff.Diff object at 0x7ecafa74>]
staged = repo.index.diff('HEAD')                                                #=> [<git.diff.Diff object at 0x7ecafa74>]

local_color = Fore.WHITE

if bool(staged):
    if bool(not_staged):
        local_color = Fore.YELLOW
    else:
        local_color = Fore.GREEN
elif bool(not_staged):
    local_color = Fore.RED

print remote_color + "(" + Style.RESET_ALL + local_color + curr_b + Style.RESET_ALL + remote_color + ")" + Style.RESET_ALL