# Coding Commands

The following defines the commands that a developer can ask of you to perform common development tasks. These commands and guidelines are designed to be used in the context of a code editor, such as Visual Studio Code.

## This role responds to the following commands wich are designated by a hashtag:

- "#comment" - Comment the code for new software engineers to understand the code. Only for the files you have loaded.

- "#strip-comments" - Remove all comments from the code. Only for the files you have loaded.

- "#analyze" - Analyze the code for improvements. DO NOT remove things you perceive as humorous. Make suggestions for improvements in small increments. List them in order of importance and ask the user to choose the one they want to implement by the number on the list. DO NOT modify any files.

- "#refactor" - Refactor the code to improve its design and maintainability

- "#simplify" - Simplify the code to make it easier to understand and increase maintainability

- "#simplify-suggest"
  - Make sugggestions to simplify the code to make it easier to understand and increase maintainability.
  - Do not under any circumestances modify any files.
  - Number each of the suggestions and ask the user to choose the one they want to implement.

=========================

## Guidelines for Creating Tools

### 1. Create tools

Tools are the specific actions that agents can perform. They are defined in the `tools` folder.

When creating a tool, you are defining a new class that extends `BaseTool` from `agency_swarm.tools`. This process involves several key steps, outlined below.

#### 1. Import Necessary Modules

Start by importing `BaseTool` from `agency_swarm.tools` and `Field` from `pydantic`. These imports will serve as the foundation for your custom tool class. Import any additional packages necessary to implement the tool's logic based on the user's requirements. Import `load_dotenv` from `dotenv` to load the environment variables.

#### 2. Define Your Tool Class

Create a new class that inherits from `BaseTool`. This class will encapsulate the functionality of your tool. `BaseTool` class inherits from the Pydantic's `BaseModel` class.

#### 3. Specify Tool Fields

Define the fields your tool will use, utilizing Pydantic's `Field` for clear descriptions and validation. These fields represent the inputs your tool will work with, including only variables that vary with each use. Define any constant variables globally.

#### 4. Implement the `run` Method

The `run` method is where your tool's logic is executed. Use the fields defined earlier to perform the tool's intended task. It must contain the actual fully functional correct python code. It can utilize various python packages, previously imported in step 1.

### Best Practices

- **Identify Necessary Packages**: Determine the best packages or APIs to use for creating the tool based on the requirements.
- **Documentation**: Ensure each class and method is well-documented. The documentation should clearly describe the purpose and functionality of the tool, as well as how to use it.
- **Code Quality**: Write clean, readable, and efficient code. Adhere to the PEP 8 style guide for Python code.
- **Web Research**: Utilize web browsing to identify the most relevant packages, APIs, or documentation necessary for implementing your tool's logic.
- **Use Python Packages**: Prefer to use various API wrapper packages and SDKs available on pip, rather than calling these APIs directly using requests.
- **Expect API Keys to be defined as env variables**: If a tool requires an API key or an access token, it must be accessed from the environment using os package within the `run` method's logic.
- **Use global variables for constants**: If a tool requires a constant global variable, that does not change from use to use, (for example, ad_account_id, pull_request_id, etc.), define them as constant global variables above the tool class, instead of inside Pydantic `Field`.
- **Add a test case at the bottom of the file**: Add a test case for each tool in if **name** == "**main**": block.

### Example of a Tool

```python
from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv

load_dotenv() # always load the environment variables

account_id = "MY_ACCOUNT_ID"
api_key = os.getenv("MY_API_KEY") # or access_token = os.getenv("MY_ACCESS_TOKEN")

class MyCustomTool(BaseTool):
    """
    A brief description of what the custom tool does.
    The docstring should clearly explain the tool's purpose and functionality.
    It will be used by the agent to determine when to use this tool.
    """
    # Define the fields with descriptions using Pydantic Field
    example_field: str = Field(
        ..., description="Description of the example field, explaining its purpose and usage for the Agent."
    )

    def run(self):
        """
        The implementation of the run method, where the tool's main functionality is executed.
        This method should utilize the fields defined above to perform the task.
        """
        # Your custom tool logic goes here
        # Example:
        # do_something(self.example_field, api_key, account_id)

        # Return the result of the tool's operation as a string
        return "Result of MyCustomTool operation"

if __name__ == "__main__":
    tool = MyCustomTool(example_field="example value")
    print(tool.run())
```

Remember, each tool code snippet you create must be fully ready to use. It must not contain any placeholders or hypothetical examples.
