import os
import asyncio

from agency_swarm.tools import BaseTool
from dotenv import load_dotenv
from github import Github
from pydantic import Field

load_dotenv()

class GetAListOfMyGithubRepositories(BaseTool):
    """
    A tool to retrieve a list of GitHub repositories owned by the authenticated user.
    Requires a GitHub access token stored in the environment variable GITHUB_ACCESS_TOKEN.
    """

    include_private: bool = Field(
        default=False,
        description="Whether to include private repositories in the list"
    )

    async def run(self) -> str:
        """
        Retrieves and returns a list of GitHub repositories.
        Returns a formatted string containing repository names and their visibility.
        """
        github_token = os.getenv("GITHUB_ACCESS_TOKEN")
        if not github_token:
            return "Error: GITHUB_ACCESS_TOKEN not found in environment variables"

        try:
            # Run the GitHub API calls in a thread to avoid blocking
            def get_repos():
                g = Github(github_token)
                user = g.get_user()
                repos = user.get_repos()
                
                repo_list = []
                for repo in repos:
                    if not self.include_private and repo.private:
                        continue
                    repo_list.append(f"- {repo.name} ({'private' if repo.private else 'public'})")
                return repo_list

            repo_list = await asyncio.to_thread(get_repos)
            
            if not repo_list:
                return "No repositories found"
                
            return "Your GitHub repositories:\n" + "\n".join(repo_list)

        except Exception as e:
            return f"Error accessing GitHub: {str(e)}"


if __name__ == "__main__":
    # Test the tool
    async def test():
        tool = GetAListOfMyGithubRepositories(include_private=True)
        print(await tool.run())

        tool = GetAListOfMyGithubRepositories(include_private=False)
        print(await tool.run())
    
    asyncio.run(test())
