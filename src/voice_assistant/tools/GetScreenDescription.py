import asyncio
import base64
import io
import os
import sys
import tempfile
from typing import ClassVar, Optional, Tuple

import aiohttp
import pygame
from agency_swarm.tools import BaseTool
from dotenv import load_dotenv
from PIL import Image
from PIL.Image import Resampling
from pydantic import Field
from rich.console import Console

from voice_assistant.models import ModelName


class ScreenCaptureError(Exception):
    """Raised when screen capture fails"""
    pass

class WindowBoundsError(Exception):
    """Raised when unable to get window bounds"""
    pass

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class GetScreenDescription(BaseTool):
    """Get a text description of the user's active window."""

    SCREENSHOT_FORMAT: ClassVar[str] = ".png"
    SCREENSHOT_TIMEOUT: ClassVar[int] = 10  # seconds
    MAX_SCREENSHOT_SIZE: ClassVar[int] = 10 * 1024 * 1024  # 10MB

    prompt: str = Field(..., description="Prompt to analyze the screenshot")
    debug_output: bool = True

    async def run(self) -> str:
        """
        Execute the screen description tool.
        
        Returns:
            str: Analysis of the screenshot
            
        Raises:
            ScreenCaptureError: If screenshot capture fails
            RuntimeError: If image analysis fails
        """
        screenshot_path = None
        try:
            screenshot_path = self.take_screenshot()
            if screenshot_path is None:
                raise ScreenCaptureError("Screenshot capture failed")
            file_content = await asyncio.to_thread(self._read_file, screenshot_path)
            resized_content = await asyncio.to_thread(self._resize_image, file_content)
            encoded_image = base64.b64encode(resized_content).decode("utf-8")
            return await self.analyze_image(encoded_image)
        
        finally:
            if screenshot_path and os.path.exists(screenshot_path):
                await asyncio.to_thread(os.remove, screenshot_path)

    # async def take_screenshot(self) -> str:
    #     """
    #     Capture a screenshot of the active window.
        
    #     Returns:
    #         str: Path to the temporary screenshot file
            
    #     Raises:
    #         WindowBoundsError: If unable to get active window bounds
    #         ScreenCaptureError: If screenshot capture fails
    #         OSError: If file operations fail
    #     """
    #     try:
    #         c = Console()
    #         if self.debug_output:
    #             c.print("Taking screenshot...")

    #         # Create temporary file
    #         with tempfile.NamedTemporaryFile(suffix=self.SCREENSHOT_FORMAT, delete=False) as tmp_file:
    #             screenshot_path = tmp_file.name
    #             if self.debug_output:
    #                 c.print(f"Screenshot file: {screenshot_path}")

            

    #         # Get window bounds
    #         bounds = await self._get_active_window_bounds()
    #         if not bounds:
    #             raise WindowBoundsError("Failed to retrieve active window bounds")

    #         # Validate bounds
    #         self._validate_bounds(bounds)

    #         x, y, width, height = bounds
    #         if self.debug_output:
    #             c.print(f"Window bounds: {x}, {y}, {width}, {height}")
            
    #         # Execute screenshot command
    #         cmd = self._get_screenshot_command(x, y, width, height)
    #         if self.debug_output:
    #             c.print(f"Executing screenshot command: {cmd}")
    #         process = await asyncio.create_subprocess_exec(
    #             *cmd,
    #             screenshot_path,
    #             stdout=asyncio.subprocess.PIPE,
    #             stderr=asyncio.subprocess.PIPE,
    #         )

    #         try:
    #             stdout, stderr = await asyncio.wait_for(
    #                 process.communicate(), 
    #                 timeout=self.SCREENSHOT_TIMEOUT
    #             )
    #         except asyncio.TimeoutError:
    #             process.kill()
    #             raise ScreenCaptureError("Screenshot capture timed out")

    #         if process.returncode != 0:
    #             error_msg = stderr.decode().strip()
    #             raise ScreenCaptureError(f"Screenshot capture failed: {error_msg}")

    #         if not os.path.exists(screenshot_path):
    #             raise ScreenCaptureError(f"Screenshot file not created at {screenshot_path}")

    #         file_size = os.path.getsize(screenshot_path)
    #         if file_size == 0:
    #             raise ScreenCaptureError("Screenshot file is empty")
    #         if file_size > self.MAX_SCREENSHOT_SIZE:
    #             raise ScreenCaptureError("Screenshot file too large")

    #         Console().print(f"Screenshot created successfully at {screenshot_path}")
    #         return screenshot_path

    #     except (WindowBoundsError, ScreenCaptureError) as e:
    #         # Clean up file if it exists
    #         if 'screenshot_path' in locals() and os.path.exists(screenshot_path):
    #             await asyncio.to_thread(os.remove, screenshot_path)
    #         raise

    #     except Exception as e:
    #         # Clean up file if it exists
    #         if 'screenshot_path' in locals() and os.path.exists(screenshot_path):
    #             await asyncio.to_thread(os.remove, screenshot_path)
    #         Console().print("Unexpected error during screenshot capture")
    #         raise ScreenCaptureError(f"Screenshot capture failed: {str(e)}") from e


    def take_screenshot(self):

        c = Console()

        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix=self.SCREENSHOT_FORMAT, delete=False) as tmp_file:
            screenshot_path = tmp_file.name
            if self.debug_output:
                c.print(f"Screenshot file: {screenshot_path}")
        
        # Detect platform and take screenshot
        try:
            import platform
            system = platform.system().lower()
            
            if system == "windows":
                import pyautogui
                screenshot = pyautogui.screenshot(imageFilename=screenshot_path)
            else:  # Linux, MacOS
                import pyscreenshot
                pyscreenshot.grab_to_file(screenshot_path)

            return screenshot_path
            
        except Exception as e:
            print(f"Error taking screenshot: {str(e)}")
            return None

    async def _get_active_window_bounds(self) -> Optional[Tuple[int, int, int, int]]:
        """
        Retrieve the bounds of the active window across different platforms.
        
        Returns:
            Tuple[int, int, int, int]: (x, y, width, height) or None if failed
        """
        try:
            if sys.platform == "darwin":  # macOS
                return await self._get_macos_window_bounds()
            elif sys.platform == "win32":  # Windows
                return await self._get_windows_window_bounds()
            elif sys.platform.startswith("linux"):  # Linux
                return await self._get_linux_window_bounds()
            else:
                raise NotImplementedError(f"Platform {sys.platform} not supported")
        except Exception as e:
            if self.debug_output:
                print(f"Error getting window bounds: {e}")
            return None

    async def _get_macos_window_bounds(self) -> Optional[Tuple[int, int, int, int]]:
        """Get active window bounds for macOS using AppleScript."""
        script = """
        tell application "System Events"
            set frontApp to first application process whose frontmost is true
            tell frontApp
                try
                    set win to front window
                    set {x, y} to position of win
                    set {w, h} to size of win
                    return {x, y, w, h}
                on error
                    return {}
                end try
            end tell
        end tell
        """
        process = await asyncio.create_subprocess_exec(
            "osascript",
            "-e",
            script,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()
        if self.debug_output:
            c = Console()
            c.print(f"[bold green]stdout: {stdout.decode()}[/bold green]")
            c.print(f"[bold red]stderr: {stderr.decode()}[/bold red]")

        if process.returncode != 0:
            return None

        output = stdout.decode().strip()
        if not output:
            return None

        try:
            bounds = eval(output)
            return bounds if isinstance(bounds, tuple) and len(bounds) == 4 else None
        except Exception as e:
            print(f"Error parsing bounds: {e}")
            return None

    async def _get_windows_window_bounds(self) -> Optional[Tuple[int, int, int, int]]:
        """Get active window bounds for Windows using Win32 API."""
        try:
            import win32con  # noqa: F401 # type: ignore
            import win32gui  # type: ignore
        except ImportError:
            if self.debug_output:
                print("pywin32 not installed. Install with: pip install pywin32")
            return None

        def get_window_bounds():
            hwnd = win32gui.GetForegroundWindow()
            rect = win32gui.GetWindowRect(hwnd)
            x = rect[0]
            y = rect[1]
            w = rect[2] - x
            h = rect[3] - y
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            return x, y, w, h

        # Run in threadpool since win32gui is not async
        return await asyncio.to_thread(get_window_bounds)

    def _validate_bounds(self, bounds: Tuple[int, int, int, int]) -> None:
        """
        Validate window bounds are reasonable.
        
        Args:
            bounds: Tuple of (x, y, width, height)
            
        Raises:
            WindowBoundsError: If bounds are invalid
        """
        x, y, width, height = bounds
        if width <= 0 or height <= 0:
            raise WindowBoundsError("Invalid window dimensions")
        if x < 0 or y < 0:
            raise WindowBoundsError("Invalid window position")

    def _get_screenshot_command(self, x: int, y: int, width: int, height: int) -> Tuple[str, ...]:
        """Generate screenshot command for current platform."""
        return (
            "screencapture",
            "-R",
            f"{x},{y},{width},{height}"
        )

    async def _get_linux_window_bounds(self) -> Optional[Tuple[int, int, int, int]]:
        """Get active window bounds for Linux using xdotool."""
        try:
            process = await asyncio.create_subprocess_exec(
                "xdotool", "getactivewindow", "getwindowgeometry",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                if self.debug_output:
                    print("xdotool not installed. Install with: sudo apt-get install xdotool")
                return None
                
            # Parse xdotool output
            # Example output:
            # Window 123456789 (focused window):
            #   Position: 100,200 (screen: 0)
            #   Geometry: 800x600
            output = stdout.decode()
            
            position_line = [line for line in output.split('\n') if "Position:" in line][0]
            geometry_line = [line for line in output.split('\n') if "Geometry:" in line][0]
            
            x, y = map(int, position_line.split(':')[1].split('(')[0].strip().split(','))
            w, h = map(int, geometry_line.split(':')[1].strip().split('x'))
            
            return x, y, w, h
            
        except Exception as e:
            if self.debug_output:
                print(f"Error getting Linux window bounds: {e}")
            return None

    
    async def analyze_image(self, base64_image: str) -> str:
        """Send the encoded image and prompt to the OpenAI API for analysis."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}",
        }

        payload = {
            "model": ModelName.FAST_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert at analyzing screenshots and describing their content. Your output should be a concise and informative description of the screenshot, focusing on the aspects mentioned in the user's prompt. Pay close attention to the specific questions or elements the user is asking about.",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Analyze this screenshot, paying particular attention to the following prompt: {self.prompt}",
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                        },
                    ],
                },
            ],
            "max_tokens": 500,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
            ) as response:
                if response.status != 200:
                    error = await response.text()
                    raise RuntimeError(f"OpenAI API error: {error}")
                result = await response.json()
                return result["choices"][0]["message"]["content"]

    def _read_file(self, path: str) -> bytes:
        """Read and return the content of a file."""
        with open(path, "rb") as image_file:
            return image_file.read()

    def _resize_image(self, image_data: bytes) -> bytes:
        """Resize the image to reduce payload size while preserving aspect ratio."""
        with Image.open(io.BytesIO(image_data)) as img:
            img.thumbnail((1600, 1200), Resampling.BICUBIC)
            with io.BytesIO() as output:
                img.save(output, format="PNG")
                return output.getvalue()


if __name__ == "__main__":

    async def test_tool():
        #clear the console
        # import os
        # os.system('cls' if os.name == 'nt' else 'clear') # clear the screen
        
        tool = GetScreenDescription(prompt="What do you see in this screenshot? Describe the main elements.")
        try:
            result = await tool.run()
            print(result)
        except Exception as e:
            print(f"Error during test: {e}")

    asyncio.run(test_tool())
