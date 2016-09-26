import sys
import os
import subprocess
import argparse
from Github import Github

def main(args):
    """
    Clone an existing repo, create a Github repo and push the actual repo into it
    :param args: {path: the path to clone it, repo_url: the original repo url}
    :return:
    """
    path = os.path.join(os.getcwd(), args.path)
    try:
        subprocess.run(["git", "clone", args.repo_url, path], check=True)
    except subprocess.CalledProcessError as e:
        sys.exit("Error during git clone")
    g = Github()
    r = g.create_repo(os.path.basename(path), auto_init=False)
    os.chdir(args.path)
    try:
        subprocess.run(["git", "remote", "add", "github", r["ssh_url"]], check=True)
    except subprocess.CalledProcessError as e:
        sys.exit("Error during adding Github remote")
    try:
        subprocess.run(["git", "push", "-u", "github", "master"], check=True)
    except subprocess.CalledProcessError as e:
        sys.exit("Error during pushing to Github but repo successfully created")
    print ("Everything went well")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to clone repo and create repo using Github API")
    parser.add_argument('repo_url')
    parser.add_argument('path')
    args = parser.parse_args()
    main(args)
