import time, re

class Utility:

    # --- Navigation Helpers ---
    @staticmethod
    def navigate_to_page(page, url, timeout=15000):
        try:
            page.goto(url, timeout=timeout)
            page.wait_for_load_state('domcontentloaded', timeout=timeout)
            page.wait_for_load_state('networkidle', timeout=timeout)
            return True
        except Exception as e:
            print(f"[ERROR] Navigation failed to {url}: {e}")
            return False

    @staticmethod
    def safe_wait_and_interact(page, selector, action, value=None, timeout=15000, retries=3):
        for attempt in range(retries):
            try:
                page.wait_for_selector(selector, timeout=timeout, state="visible")
                element = page.locator(selector)
                element.wait_for(state="visible", timeout=timeout)
                if action == "click":
                    element.click()
                elif action == "fill":
                    element.fill(value)
                elif action == "type":
                    element.type(value)
                return True
            except Exception as e:
                print(f"[WARN] Attempt {attempt + 1} failed for {selector}: {e}")
                if attempt == retries - 1:
                    return False
                time.sleep(1)
        return False

    @staticmethod
    def wait_for_element_state(page, selector, state="visible", timeout=15000):
        try:
            element = page.locator(selector)
            element.wait_for(state=state, timeout=timeout)
            return True
        except Exception as e:
            print(f"[ERROR] Element state wait failed for {selector}: {e}")
            return False

    # --- Data Validation Helpers ---
    @staticmethod
    def validate_and_convert_data(data, target_type):
        try:
            if target_type == str:
                return str(data) if data is not None else ""
            elif target_type == int:
                return int(data) if data not in [None, ""] else 0
            elif target_type == float:
                return float(data) if data not in [None, ""] else 0.0
            else:
                return data
        except (ValueError, TypeError) as e:
            print(f"[ERROR] Data conversion failed: {e}")
            return None

    # --- Retry Helpers ---
    @staticmethod
    def retry_assertion(assertion_func, retries=3, delay=1000):
        for attempt in range(retries):
            try:
                assertion_func()
                return True
            except AssertionError as e:
                if attempt == retries - 1:
                    raise e
                time.sleep(delay / 1000)
        return False

    # --- Element Text Retrieval ---
    @staticmethod
    def get_element_text(page, selector: str, timeout: int = 15000) -> str:
        try:
            locator = page.locator(selector)
            locator.wait_for(state="visible", timeout=timeout)
            return locator.inner_text()
        except Exception as e:
            print(f"[ERROR] Failed to get text from {selector}: {e}")
            return ""

    # --- Logging Utilities ---
    @staticmethod
    def log_console_message(msg):
        print(f"[CONSOLE] {msg.text}")

    @staticmethod
    def log_test_step(step_desc):
        print(f"[STEP] {step_desc}")

    @staticmethod
    def log_test_result(result, details):
        print(f"[RESULT] {result}: {details}")

    @staticmethod
    def log_error(error_msg):
        print(f"[ERROR] {error_msg}")

    @staticmethod
    def log_element_state(element_name, locator, timeout=15000):
        try:
            from playwright.sync_api import expect
            expect(locator).to_be_visible(timeout=timeout)
            print(f"[INFO] {element_name} is visible.")
        except Exception as e:
            print(f"[WARN] {element_name} is NOT visible: {e}")
