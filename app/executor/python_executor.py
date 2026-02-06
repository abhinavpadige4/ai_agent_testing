import subprocess
import sys
import time
from typing import Dict, List


def generate_python_test(steps: List[Dict]) -> str:
    lines = []

    lines.append('"""\nAuto-generated Playwright test (VISIBLE MODE)\n"""\n\n')
    lines.append('from playwright.sync_api import sync_playwright\n')
    lines.append('import time\n')
    lines.append('import sys\n\n')

    lines.append('def run_test():\n')
    lines.append('    print("🎭 Starting test execution...")\n')
    lines.append('    with sync_playwright() as p:\n')
    lines.append('        browser = p.chromium.launch(headless=False, slow_mo=900)\n')
    lines.append('        context = browser.new_context(viewport={"width":1280,"height":720})\n')
    lines.append('        page = context.new_page()\n')
    lines.append('        try:\n')

    for i, step in enumerate(steps, 1):
        action = step.get("action")
        lines.append(f'            print("\\n➡️ Step {i}: {action}")\n')

        # ---------- OPEN ----------
        if action == "OPEN_BROWSER":
            url = step.get("url", "")
            if not url.startswith("http"):
                url = f"https://{url}"

            lines.append(f'            print("🌐 Opening {url}")\n')
            lines.append(f'            page.goto("{url}", wait_until="domcontentloaded")\n')
            lines.append('            time.sleep(3)\n')

        # ---------- SEARCH ----------
        elif action == "SEARCH":
            query = step.get("query", "").replace('"', '\\"')

            lines.append(f'            print("🔍 Searching for: {query}")\n')
            lines.append('            page.mouse.click(300, 300)\n')
            lines.append('            time.sleep(1)\n')

            # cookie consent
            lines.append('            try:\n')
            lines.append('                page.get_by_text("Accept all").click(timeout=3000)\n')
            lines.append('            except:\n')
            lines.append('                pass\n')

            # GOOGLE
            lines.append('            if "google." in page.url:\n')
            lines.append('                print("🌍 Google detected")\n')
            lines.append('                page.wait_for_selector("textarea[name=\\"q\\"], input[name=\\"q\\"]", timeout=30000)\n')
            lines.append(f'                page.fill("textarea[name=\\"q\\"], input[name=\\"q\\"]", "{query}")\n')
            lines.append('                page.keyboard.press("Enter")\n')

            # YOUTUBE (FIXED)
            lines.append('            elif "youtube.com" in page.url:\n')
            lines.append('                print("📺 YouTube detected")\n')
            lines.append('                page.wait_for_selector("input[name=\\"search_query\\"]", timeout=30000)\n')
            lines.append('                page.click("input[name=\\"search_query\\"]")\n')
            lines.append(f'                page.fill("input[name=\\"search_query\\"]", "{query}")\n')
            lines.append('                page.keyboard.press("Enter")\n')

            # AMAZON
            lines.append('            elif "amazon." in page.url:\n')
            lines.append('                print("🛒 Amazon detected")\n')
            lines.append('                page.wait_for_selector("#twotabsearchtextbox", timeout=30000)\n')
            lines.append(f'                page.fill("#twotabsearchtextbox", "{query}")\n')
            lines.append('                page.keyboard.press("Enter")\n')

            lines.append('            else:\n')
            lines.append('                raise Exception("Search not supported for this site")\n')

            lines.append('            page.wait_for_load_state("networkidle")\n')
            lines.append('            time.sleep(5)\n')

        # ---------- TYPE ----------
        elif action == "TYPE":
            selector = step.get("selector")
            value = step.get("value", "").replace('"', '\\"')

            lines.append(f'            print("⌨️ Typing {value} into {selector}")\n')
            lines.append(f'            page.wait_for_selector("{selector}", timeout=20000)\n')
            lines.append(f'            page.click("{selector}")\n')
            lines.append(f'            page.fill("{selector}", "{value}")\n')
            lines.append('            time.sleep(1)\n')

        # ---------- CLICK ----------
        elif action == "CLICK":
            selector = step.get("selector")
            lines.append(f'            print("🖱️ Clicking {selector}")\n')
            lines.append(f'            page.wait_for_selector("{selector}", timeout=20000)\n')
            lines.append(f'            page.click("{selector}")\n')
            lines.append('            time.sleep(3)\n')

        # ---------- WAIT ----------
        elif action == "WAIT":
            duration = step.get("duration", 3000)
            lines.append(f'            print("⏱️ Waiting {duration}ms")\n')
            lines.append(f'            page.wait_for_timeout({duration})\n')

    lines.append('            print("\\n✅ Test COMPLETED successfully")\n')
    lines.append('            print("🛑 Browser stays open for 20 seconds")\n')
    lines.append('            time.sleep(20)\n')
    lines.append('            browser.close()\n')
    lines.append('            return 0\n')

    lines.append('        except Exception as e:\n')
    lines.append('            print(f"❌ Test FAILED: {e}")\n')
    lines.append('            time.sleep(20)\n')
    lines.append('            browser.close()\n')
    lines.append('            return 1\n\n')

    lines.append('if __name__ == "__main__":\n')
    lines.append('    sys.exit(run_test())\n')

    return "".join(lines)


def execute_python_test(test_file_path: str, timeout: int = 180) -> Dict:
    print(f"\n🎭 Executing: {test_file_path}")

    result = subprocess.run(
        [sys.executable, test_file_path],
        stdout=sys.stdout,
        stderr=sys.stderr,
        timeout=timeout
    )

    return {
        "status": "passed" if result.returncode == 0 else "failed",
        "output": "Live output shown in terminal",
        "errors": "",
        "return_code": result.returncode
    }
