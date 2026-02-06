"""
Simplified Flask Routes
Using Python Playwright only
"""

from flask import Blueprint, request, jsonify
import sys
import os

# Import the stateful agent
try:
    from app.agents.test_agent import agent
    AGENT_AVAILABLE = True
except ImportError as e:
    AGENT_AVAILABLE = False
    print(f"⚠️  Agent import failed: {e}")

api = Blueprint("api", __name__)


@api.route("/chat", methods=["POST"])
def chat():
    """
    Main endpoint: accepts natural language, returns test results
    """
    if not AGENT_AVAILABLE:
        return jsonify({
            "status": "error",
            "message": "Test agent not available"
        }), 500
    
    data = request.get_json()
    message = data.get("message", "")
    
    if not message:
        return jsonify({
            "status": "error",
            "message": "No instruction provided"
        }), 400
    
    try:
        print(f"\n{'='*60}")
        print(f"📨 Received: {message}")
        print(f"{'='*60}")
        
        # Invoke the stateful agent
        result = agent.invoke({
            "user_instruction": message,
            "parsed_steps": [],
            "parsing_status": "",
            "browser_open": False,
            "current_url": "",
            "logged_in": False,
            "generated_code": "",
            "code_file_path": "",
            "execution_status": "",
            "execution_output": "",
            "execution_errors": "",
            "test_passed": False
        })
        
        execution_status = result.get("execution_status", "unknown")
        execution_passed = execution_status == "passed"
        # Extract results from final state
        response = {
            "status": "success",
            "instruction": message,
            "parsed_steps": result.get("parsed_steps", []),
            "browser_state": {
                "browser_open": result.get("browser_open", False),
                "current_url": result.get("current_url", ""),
                "logged_in": result.get("logged_in", False)
            },
            "generated_code": result.get("generated_code", ""),
            "code_file_path": result.get("code_file_path", ""),
            

            "execution": {
                "status": execution_status,
                "output": result.get("execution_output", ""),
                "errors": result.get("execution_errors", ""),
                "passed": execution_passed
            }

        }
        
        return jsonify(response)
    
    except Exception as e:
        import traceback
        print(f"❌ Error: {e}")
        traceback.print_exc()
        
        return jsonify({
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }), 500


@api.route("/diagnostics", methods=["GET"])
def diagnostics():
    """
    System diagnostics
    """
    import subprocess
    
    # Check Python
    python_version = sys.version
    
    # Check Playwright
    playwright_check = {"installed": False, "version": None}
    try:
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            playwright_check = {
                "installed": True,
                "version": result.stdout.strip()
            }
    except:
        pass
    
    # Check Ollama
    ollama_check = {"running": False}
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        ollama_check = {
            "running": response.status_code == 200,
            "models": response.json().get("models", []) if response.status_code == 200 else []
        }
    except:
        pass
    
    # Check project structure
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    structure = {
        "test_agent": os.path.exists(os.path.join(project_root, "app", "agents", "test_agent.py")),
        "executor": os.path.exists(os.path.join(project_root, "app", "executor", "python_executor.py")),
        "generated_tests": os.path.exists(os.path.join(project_root, "app", "generated_tests"))
    }
    
    return jsonify({
        "system": {
            "python_version": python_version,
            "platform": sys.platform
        },
        "playwright": playwright_check,
        "ollama": ollama_check,
        "agent_available": AGENT_AVAILABLE,
        "project_structure": structure
    })


@api.route("/tests", methods=["GET"])
def list_tests():
    """
    List all generated tests
    """
    import glob
    
    test_dir = "app/generated_tests"
    if not os.path.exists(test_dir):
        return jsonify({"tests": []})
    
    test_files = glob.glob(os.path.join(test_dir, "test_*.py"))
    
    tests = []
    for filepath in sorted(test_files, reverse=True):
        filename = os.path.basename(filepath)
        # Extract timestamp from filename
        timestamp = filename.replace("test_", "").replace(".py", "")
        
        tests.append({
            "filename": filename,
            "filepath": filepath,
            "timestamp": timestamp,
            "size": os.path.getsize(filepath)
        })
    
    return jsonify({"tests": tests[:10]})  # Last 10 tests