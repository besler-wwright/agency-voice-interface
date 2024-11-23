import asyncio
import os
import subprocess
from typing import Optional

from agency_swarm.tools import BaseTool
from rich.console import Console


class GetGitRepoName(BaseTool):
    """A tool to get the name of the current git repository."""

    async def run(self) -> str:
        """
        Gets the name of the current git repository.
        
        Returns:
            str: Repository name or error message if not in a git repo
        """
        try:
            # Get the git root directory
            root_dir = await self._get_git_root()
            if not root_dir:
                return "Not a git repository"

            # Get the remote URL
            remote_url = await self._get_remote_url()
            if not remote_url:
                # If no remote, use the directory name
                return os.path.basename(root_dir)

            # Extract repo name from remote URL
            repo_name = self._parse_repo_name(remote_url)
            return repo_name or os.path.basename(root_dir)

        except Exception as e:
            Console().print(f"[bold red]Error getting repository name: {str(e)}[/bold red]")
            return f"Error: {str(e)}"

    async def _get_git_root(self) -> Optional[str]:
        """Gets the root directory of the git repository."""
        try:
            process = await asyncio.create_subprocess_exec(
                'git', 'rev-parse', '--show-toplevel',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, _ = await process.communicate()
            if process.returncode == 0:
                return stdout.decode().strip()
            return None
        except Exception:
            return None

    async def _get_remote_url(self) -> Optional[str]:
        """Gets the remote URL of the git repository."""
        try:
            process = await asyncio.create_subprocess_exec(
                'git', 'config', '--get', 'remote.origin.url',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, _ = await process.communicate()
            if process.returncode == 0:
                return stdout.decode().strip()
            return None
        except Exception:
            return None

    def _parse_repo_name(self, remote_url: str) -> Optional[str]:
        """
        Extracts repository name from remote URL.
        
        Args:
            remote_url: Git remote URL
            
        Returns:
            str: Repository name without .git extension
        """
        # Handle SSH URLs (git@github.com:username/repo.git)
        if remote_url.startswith('git@'):
            parts = remote_url.split(':')[-1].split('/')
            if len(parts) >= 1:
                return parts[-1].replace('.git', '')

        # Handle HTTPS URLs (https://github.com/username/repo.git)
        if remote_url.startswith('http'):
            parts = remote_url.split('/')
            if len(parts) >= 1:
                return parts[-1].replace('.git', '')

        return None


if __name__ == "__main__":
    async def test_tool():
        tool = GetGitRepoName()
        result = await tool.run()
        print(f"Repository name: {result}")

    asyncio.run(test_tool())
