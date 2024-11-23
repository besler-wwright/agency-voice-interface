from agency_swarm.tools import BaseTool
from rich.console import Console
from ..utils.git_utils import get_repository_name


class GetGitRepoName(BaseTool):
    """A tool to get the name of the current git repository."""

    async def run(self) -> str:
        """
        Gets the name of the current git repository.
        
        Returns:
            str: Repository name or error message if not in a git repo
        """
        try:
            return await get_repository_name()
        except Exception as e:
            Console().print(f"[bold red]Error getting repository name: {str(e)}[/bold red]")
            return f"Error: {str(e)}"


if __name__ == "__main__":
    import asyncio
    
    async def test_tool():
        tool = GetGitRepoName()
        result = await tool.run()
        print(f"Repository name: {result}")

    asyncio.run(test_tool())
