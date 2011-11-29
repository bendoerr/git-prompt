import anydbm
from git import *
from datetime import datetime, timedelta
import time

expire_after = timedelta(hours=6)

class LocalRemoteState:
    UP_TO_DATE = 1
    BEHIND = 2
    DIVERGED = 3
    AHEAD = 5

def check_status_with_remote(repo, curr_tb, invalidateCache):
    key = repo.git_dir + " " + curr_tb.path

    cache = anydbm.open('/cygdrive/c/sanctuary/home/bendoerr/.git_prompt', 'c')

    if invalidateCache == False and\
       key + " checked" in cache and\
       ((datetime.fromtimestamp(float(cache[key + " checked"])) + expire_after) > datetime.now()):
        state = int(cache[key + " state"])
    else:
        state = check_status_with_remote_no_cache(repo, curr_tb) #{'checked': datetime.now(), 'state': }

        cache[key + " checked"] = str(time.time())
        cache[key + " state"] = str(state)
        
    cache.close()

    return state


def check_status_with_remote_no_cache(repo, curr_tb):
    b = repo.head.ref.name                                                      #=> 'master'
    rb = curr_tb.name.split("/")                                                #=> {'origin', 'master'}

    curr_commit = repo.head.commit.hexsha                                       #=> '6b800a2fe00d33b3b953eda423438f03c3d59320'
    curr_r_commit = Git(repo.git_dir).ls_remote(rb[0],
                                "refs/heads/" + rb[1]).split("\t")[0]           #=> 'bf1e66aa5ec90325bf358469d1b13fac6777c045'

    if curr_commit != curr_r_commit:
        lGit = Git(repo.git_dir)
        remote_commits = lGit.cherry(b, "remotes/" + curr_tb.name)              #=> ''
        local_commits = lGit.cherry()                                           #=> ''

        if bool(remote_commits) == False and bool(local_commits) == False:
            repo.remote(rb[0]).fetch()

        remote_commits = lGit.cherry(b, "remotes/" + curr_tb.name)              #=> '+ cb601efd16ecb322c349378a4393620e7b05301c'
        local_commits = lGit.cherry()                                           #=> '+ a305fad893e72ca4ad78171b18977227cb61bf25\n+ 4155609d8350c0112280b419df6b0f6c7ec641b7'

        if bool(remote_commits):
            if bool(local_commits):
                return LocalRemoteState.DIVERGED
            else:
                return LocalRemoteState.BEHIND
        elif bool(local_commits):
            return LocalRemoteState.AHEAD
    else:
        return LocalRemoteState.UP_TO_DATE
