import git
import os


def push_to_github(commit_message="Updates"):
    repo_dir = os.path.dirname(os.path.abspath(__file__))  # Path to your project directory
    repo = git.Repo(repo_dir)

    try:
        repo.git.add(A=True)
        repo.index.commit(commit_message)
        origin = repo.remote(name='origin')
        origin.push()
        print("Changes pushed to GitHub.")
    except Exception as e:
        print(f"Failed to push changes: {e}")


# Example usage
if __name__ == "__main__":
    push_to_github("Updated the project with new changes.")
