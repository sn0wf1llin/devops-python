import argparse
import requests
import getpass


def checker(func):
    def _checker(self, *args, **kwargs):
        if any([kwargs['owner'], kwargs['repo'],
                kwargs['user']]) is None:
            raise Exception("No <owner> | <repo> |"
                            " <user> args provided")

        return func(self, *args, **kwargs)

    return _checker


class GithubPullRequestGrabber:
    def __init__(self):
        self.version = "v0.1"
        self.__url = "https://api.github.com/repos/{}/" \
                     "{}/pulls?state=all"

    @staticmethod
    def _stats_by_default_keys(pull_data):
        print(f"State: {pull_data['state']}\n"
              f"Title: {pull_data['title']}\n"
              f"Number: {pull_data['number']}\n"
              f"Created at: {pull_data['created_at']}"
              f"Updated at: {pull_data['updated_at']}\n"
              f"State: {pull_data['state']}\n"
              f"Url: {pull_data['url']}\n{'-'*44}")

    @checker
    def get_stats(self, owner, user, repo):
        passwd = getpass.getpass()

        url = self.__url.format(owner, repo)
        r = requests.get(url, auth=(user, passwd))
        data = r.json()
        print(f"#{'-'*66}\n# Pulls count: {len(data)}\n#{'-'*66}\n")

        for pull_data in data:
            self._stats_by_default_keys(pull_data)

        return data


if __name__ == "__main__":
    # Usage: pr_stats.py [options]
    # -u|--user <user> -o|--owner <owner> -r|--repo <repo>

    gitgrabber = GithubPullRequestGrabber()

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='store_true',
                        default=False, dest='version',
                        help="Script version")
    parser.add_argument('-u', '--user', action='store', type=str,
                        dest='user', help="User nickname")
    parser.add_argument('-o', '--owner', action='store', type=str,
                        dest='owner',
                        help="Repository owner nickname")
    parser.add_argument('-r', '--repo', action='store',
                        type=str, dest='repo', help="Repository")

    args = parser.parse_args()

    if args.version:
        print(gitgrabber.version)
        exit()

    gitgrabber.get_stats(user=args.user, owner=args.owner, repo=args.repo)
