import org.eclipse.jgit.lib.IndexDiff;
import org.eclipse.jgit.lib.ObjectId;
import org.eclipse.jgit.lib.Repository;
import org.eclipse.jgit.lib.RepositoryBuilder;
import org.eclipse.jgit.revwalk.RevWalk;
import org.eclipse.jgit.treewalk.FileTreeIterator;

import java.io.File;
import java.io.IOException;

class Prompt {
    public static void main(String[] args)
            throws IOException {
        System.out.println("Test");

        Repository repo = new RepositoryBuilder()
                .setGitDir(new File("./.git/"))
                .readEnvironment()
                .findGitDir()
                .build();

        if (repo.isBare()) { // No .git (might not even be a git repop)
            System.out.println("No Repo");
            return;
        }

        String branch = repo.getBranch();
        System.out.println("Branch: " + branch);

        System.out.println(new FileTreeIterator(repo).getOptions().getAutoCRLF());

        IndexDiff index = new IndexDiff(repo, "HEAD", new FileTreeIterator(repo));
        index.diff();

        System.out.println("Changed not staged: " + index.getModified());
        System.out.println("Staged: " + index.getChanged());


        RevWalk walk = new RevWalk(repo);
        ObjectId from = repo.resolve("refs/heads/master");
        ObjectId to = repo.resolve("refs/remotes/origin/master");

        walk.markStart(walk.parseCommit(from));
        walk.markUninteresting(walk.parseCommit(to));
    }
}
