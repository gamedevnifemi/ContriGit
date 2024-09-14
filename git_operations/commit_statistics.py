import subprocess
from collections import defaultdict

def get_total_commit_per_day(repo):
    result = subprocess.run(
        [
            "git", "log",
            "--author=" + "gamedevnifemi",
            "--pretty=format:%ad",
            "--date=format:%Y-%m-%d"
        ],
        cwd= repo,
        stdout=subprocess.PIPE,
        text=True,
        encoding= 'utf-8'
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

def sort_all_repos(repos):
    reposData = {}
    for repo in repos:
        commit_counts = get_total_commit_per_day(repo)
        if commit_counts:
            reposData[repo] = commit_counts
        else:
            print(f"Skipping repository: {repo} due to error")

    print(f"Processed {len(reposData)} out of {len(repos)} repositories successfully.")
    return reposData