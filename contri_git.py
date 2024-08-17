from collections import defaultdict
import os
import subprocess
def find_git_repos(path):
    gitRepos = []
    for dirPath, dirNames, files in os.walk(path):
        if ".git" in dirNames:
            gitRepos.append(dirPath)
    return gitRepos

def get_commit_stats(repo, sort_by_author=False):
    result = subprocess.run(
        [
            "git", "shortlog",
            "-n",
            "-s",
            # "--since=" + start
            # "--author=" + author,
        ],
        cwd= repo,
        stdout=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )
    # handling errors
    if result.returncode != 0:
        print(f"Error running git shortlog command in repository: {repo}")
        return None
    
    # Parse the output
    commit_data = {}
    for line in result.stdout.strip().split('\n'):
        count, author = line.strip().split('\t', 1)
        commit_data[author] = int(count)

    # Sort by author name if requested
    if sort_by_author:
        commit_data = dict(sorted(commit_data.items()))
    return commit_data

def get_total_commit_per_day(repo, author):
    result = subprocess.run(
        [
            "git", "log",
            "--author=" + author,
            "--pretty=format:%ad",
            "--date=format:%Y-%m-%d"
        ],
        cwd= repo,
        stdout=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )

    # handling errors
    if result.returncode != 0:
        print(f"Error running git shortlog command in repository: {repo}")
        return None
    
    # Parse the output to count commits per day
    daily_commits = defaultdict(int)  # Using defaultdict to avoid key errors
    for line in result.stdout.strip().split('\n'):
        daily_commits[line] += 1  # Increment the count for the specific day

    return dict(daily_commits)  # Convert to regular dictionary for output

def sortAllRepos(repos, author, sort_by_author=False):
    reposData = {}

    for repo in repos:
        # commit_counts = get_total_commit_per_day(repo, author)
        commit_counts = get_total_commit_per_day(repo, author)
        if commit_counts:
            reposData[repo] = commit_counts
        else:
            print(f"Skipping repository: {repo} due to error")

    print(f"Processed {len(reposData)} out of {len(repos)} repositories successfully.")
    return reposData

# Example usage with customizations
if __name__ == "__main__":
    # Customize these parameters as needed
    path = "/Users/akinl/myProjects"
    repos = find_git_repos(path)
    print(f"Found {len(repos)} Git repositories in {path}.\n")

    sort_by_author = False
    author = "gamedevnifemi"

    commitRange = sortAllRepos(repos, author)
    for repo, data in commitRange.items():
        print(f"\nRepository: {repo}")
        print(f"\nAuthor is: {author}")
        for day, count in data.items():
            print(f"day: {day}, Commits: {count}")
    
    # for repo, data in commitRange.items():
    #     print(f"\nRepository: {repo}")
    #     for author, count in data.items():
    #         print(f"Author: {author}, Commits: {count}")
            
    
