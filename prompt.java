import org.eclipse.jgit.lib.*;
import java.io.*;

class Prompt {
  public static void main(String[] args)
      throws IOException {
    System.out.println("Test");

    Repository repo = new RepositoryBuilder()
        .setGitDir(new File(".git"))
        .readEnvironment()
        .findGitDir()
        .build();

    if(repo.isBare()) { // No .git (might not even be a git repop)
        System.out.println("No Repo");
        return;
    }

    System.out.println(repo.getRepositoryState());
  }
}
