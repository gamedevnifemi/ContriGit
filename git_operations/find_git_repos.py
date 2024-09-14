import os

def find_git_repos(path):
    gitRepos = []
    for dirPath, dirNames, files in os.walk(path):
        if ".git" in dirNames:
            gitRepos.append(dirPath)
    return gitRepos