import subprocess

def get_git_commits():
    result = subprocess.run(
        ["git", "log", "--all", "--pretty=format:%H\t%P\t%D"],
        capture_output=True,
        text=True
    )
    commits = []
    for line in result.stdout.splitlines():
        commit, parents, refs = line.split("\t")
        commits.append({
            "id": commit,
            "parents": parents.split() if parents else [],
            "refs": refs
        })
    return commits
print(get_git_commits())
