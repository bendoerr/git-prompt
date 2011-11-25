import org.eclipse.jgit.lib.*;
import org.eclipse.jgit.dircache.*;
import org.eclipse.jgit.treewalk.*;
import java.io.*;

class Prompt {
  public static void main(String[] args)
      throws IOException {
    System.out.println("Test");

    Repository repo = new RepositoryBuilder()
        .setGitDir(new File("./.git/"))
        .readEnvironment()
        .findGitDir()
        .build();

    if(repo.isBare()) { // No .git (might not even be a git repop)
        System.out.println("No Repo");
        return;
    }

    String branch = repo.getBranch();
    IndexDiff index = new IndexDiff(repo, "HEAD", new FileTreeIterator(repo));
    index.diff();

    System.out.println("Branch: " + branch);
    System.out.println("Changed not staged: " + index.getModified());
    System.out.println("Staged: " + index.getChanged()); 
    
  }
}
