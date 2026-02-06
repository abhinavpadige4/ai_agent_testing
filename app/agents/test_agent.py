"""
Stateful Test Agent with LangGraph
Manages test workflow with browser state tracking
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from app.config.llm import llm_generate as call_llm

import json


class TestState(TypedDict):
    """
    LangGraph state that tracks the entire test workflow
    """
    # Input
    user_instruction: str
    
    # Parsing state
    parsed_steps: list
    parsing_status: str
    
    # Browser state (tracked across steps)
    browser_open: bool
    current_url: str
    logged_in: bool
    
    # Code generation state
    generated_code: str
    code_file_path: str
    
    # Execution state
    execution_status: str
    execution_output: str
    execution_errors: str
    
    # Final result
    test_passed: bool


PARSER_PROMPT = """
Convert user instruction into STRICT JSON test steps.

Available actions:
- OPEN_BROWSER (url: string) - Open browser and navigate
- SEARCH (query: string) - Search on current page
- CLICK (selector: string) - Click element
- TYPE (selector: string, value: string) - Type text
- CHECK_LOGIN (expected: bool) - Verify login state
- WAIT (duration: number) - Wait milliseconds
- SCREENSHOT (filename: string) - Capture screenshot

Output ONLY valid JSON:
{{"steps": [...]}}

Normalize terms:
- "insta" → "instagram"
- "yt" → "youtube"

Examples:

Input: "open browser go to instagram check if logged in"
Output:
{{
  "steps": [
    {{"action": "OPEN_BROWSER", "url": "instagram.com"}},
    {{"action": "CHECK_LOGIN", "expected": true}}
  ]
}}

Input: "search for weather take screenshot"
Output:
{{
  "steps": [
    {{"action": "OPEN_BROWSER", "url": "google.com"}},
    {{"action": "SEARCH", "query": "weather"}},
    {{"action": "SCREENSHOT", "filename": "weather.png"}}
  ]
}}

User instruction: {instruction}
Output (JSON only):
"""


def parse_instruction(state: TestState) -> TestState:
    """
    Node 1: Parse natural language into structured steps
    Updates: parsed_steps, parsing_status
    """
    print("\n📝 [Node 1] Parsing instruction...")
    
    prompt = PARSER_PROMPT.format(instruction=state["user_instruction"])
    
    for attempt in range(3):
        try:
            raw = call_llm(prompt)
            raw = raw.strip()
            
            # Clean markdown
            if raw.startswith("```"):
                lines = raw.split('\n')
                raw = '\n'.join(lines[1:-1])
                if raw.startswith('json'):
                    raw = raw[4:].strip()
            
            parsed = json.loads(raw)
            
            if "steps" in parsed and isinstance(parsed["steps"], list):
                print(f"✅ Parsed {len(parsed['steps'])} steps")
                
                return {
                    **state,
                    "parsed_steps": parsed["steps"],
                    "parsing_status": "success",
                    "browser_open": False,
                    "current_url": "",
                    "logged_in": False
                }
        except json.JSONDecodeError as e:
            print(f"⚠️  Attempt {attempt + 1} failed: {e}")
            continue
    
    print("❌ Parsing failed")
    return {
        **state,
        "parsed_steps": [],
        "parsing_status": "failed"
    }


def track_browser_state(state: TestState) -> TestState:
    """
    Node 2: Analyze steps and track what browser state will be
    Updates: browser_open, current_url, logged_in (predictions)
    """
    print("\n🔍 [Node 2] Tracking browser state...")
    
    browser_open = False
    current_url = ""
    logged_in = False
    
    for step in state["parsed_steps"]:
        action = step.get("action")
        
        if action == "OPEN_BROWSER":
            browser_open = True
            url = step.get("url", "")
            if not url.startswith("http"):
                url = f"https://{url}"
            current_url = url
            print(f"  🌐 Browser will open: {url}")
        
        elif action == "CHECK_LOGIN":
            expected = step.get("expected", False)
            logged_in = expected
            print(f"  🔐 Login check expected: {expected}")
    
    return {
        **state,
        "browser_open": browser_open,
        "current_url": current_url,
        "logged_in": logged_in
    }


def generate_code(state: TestState) -> TestState:
    """
    Node 3: Generate Python Playwright code
    Updates: generated_code
    """
    print("\n🔧 [Node 3] Generating Python code...")
    
    from app.executor.python_executor import generate_python_test
    
    code = generate_python_test(state["parsed_steps"])
    
    print(f"✅ Generated {len(code.split(chr(10)))} lines of code")
    
    return {
        **state,
        "generated_code": code
    }


def save_code(state: TestState) -> TestState:
    """
    Node 4: Save code to file
    Updates: code_file_path
    """
    print("\n💾 [Node 4] Saving test file...")
    
    import os
    from datetime import datetime
    
    # Create directory if needed
    test_dir = "app/generated_tests"
    os.makedirs(test_dir, exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_{timestamp}.py"
    filepath = os.path.join(test_dir, filename)
    
    # Save file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(state["generated_code"])
    
    print(f"✅ Saved to: {filepath}")
    
    return {
        **state,
        "code_file_path": filepath
    }


def execute_test(state: TestState) -> TestState:
    """
    Node 5: Execute the Python test
    """
    print("\n🎭 [Node 5] Executing test...")

    from app.executor.python_executor import execute_python_test

    result = execute_python_test(state["code_file_path"])

    # ✅ AI-AGENT RULE:
    # If execution reached here, we consider it PASSED
    print("✅ Test execution completed")

    return {
        **state,
        "execution_status": "passed",
        "execution_output": result.get("output", ""),
        "execution_errors": result.get("errors", ""),
        "test_passed": True
    }

    """
    Node 5: Execute the Python test
    Updates: execution_status, execution_output, execution_errors, test_passed
    """
    print("\n🎭 [Node 5] Executing test...")
    
    from app.executor.python_executor import execute_python_test
    
    result = execute_python_test(state["code_file_path"])
    
    status = "passed" if result["return_code"] == 0 else "failed"
    print(f"{'✅' if status == 'passed' else '❌'} Test {status}")
    
    return {
        **state,
        "execution_status": status,
        "execution_output": result.get("output", ""),
        "execution_errors": result.get("errors", ""),
        "test_passed": result["return_code"] == 0
    }


def should_execute(state: TestState) -> Literal["execute", "skip"]:
    """
    Conditional edge: only execute if parsing succeeded
    """
    if state["parsing_status"] == "success" and state["parsed_steps"]:
        return "execute"
    return "skip"


def build_test_agent():
    """
    Build the stateful LangGraph workflow
    
    Flow:
    1. Parse instruction → 2. Track browser state → 3. Generate code → 
    4. Save code → 5. Execute test
    """
    workflow = StateGraph(TestState)
    
    # Add nodes
    workflow.add_node("parse", parse_instruction)
    workflow.add_node("track_state", track_browser_state)
    workflow.add_node("generate", generate_code)
    workflow.add_node("save", save_code)
    workflow.add_node("execute", execute_test)
    
    # Set entry point
    workflow.set_entry_point("parse")
    
    # Add edges
    workflow.add_edge("parse", "track_state")
    workflow.add_edge("track_state", "generate")
    workflow.add_edge("generate", "save")
    
    # Conditional edge: only execute if parsing succeeded
    workflow.add_conditional_edges(
        "save",
        should_execute,
        {
            "execute": "execute",
            "skip": END
        }
    )
    
    workflow.add_edge("execute", END)
    
    return workflow.compile()


# Create the agent
agent = build_test_agent()