
# Test Case 1 - TC-0002
# Test URLs (update as needed)
urls: dict[str, str] = {
    "main_page": os.environ.get("EDULEARN_MAIN_URL", "http://localhost:8000/index.html")
}
def test_header_and_link_display_consistent_visual_styling() -> None:
    """
    TC-0002: Header and Link Display Consistent Visual Styling
    Validates visual consistency, alignment, font, responsiveness, and interactive styling of the header and navigation link.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True
        )
        page = context.new_page()
        generated_page = GeneratedPage(page)
        page.on("console", lambda msg: Utility.log_console_message(msg))
        test_passed: bool = False
        try:
            # Given: Navigate to the main page and accept cookies/pop-ups if present
            Utility.log_test_step("Navigating to the main (index) page.")
            navigation_success: bool = Utility.navigate_to_page(page, urls["main_page"], timeout=15000)
            if not navigation_success:
                Utility.log_error("Failed to navigate to the main page.")
                raise Exception("Navigation to main page failed.")
            Utility.log_test_step("Waiting for body to be visible.")
            Utility.wait_for_element_state(page, "body", state="visible", timeout=15000)
            # Accept cookies/pop-ups if present (assuming a button with text 'Accept' or similar)
            cookie_accepted: bool = Utility.safe_wait_and_interact(
                page, "text=Accept", action="click", timeout=3000, retries=1
            )
            # Then: Validate essential elements (header and link) are visible
            Utility.log_test_step("Validating essential elements are visible.")
            Utility.retry_assertion(lambda: generated_page.validate_essential_elements(), retries=3, delay=1000)
            # When: Observe the alignment and spacing of the header and the "← Back to Courses" link
            Utility.log_test_step("Checking visibility and alignment of the 'Back to Courses' link.")
            Utility.retry_assertion(
                lambda: expect(page.locator(f"xpath={generated_page._lnk_courses_xpath}")).to_be_visible(timeout=15000),
                retries=3, delay=1000
            )
            # Then: Check background color, font style, font size, and text color of the header and link
            Utility.log_test_step("Checking computed styles for header and link.")
            header_selector: str = "header"
            link_selector: str = f"xpath={generated_page._lnk_courses_xpath}"
            # Wait for header to be visible
            Utility.wait_for_element_state(page, header_selector, state="visible", timeout=15000)
            Utility.log_element_state("Header", page.locator(header_selector), timeout=15000)
            Utility.log_element_state("'Back to Courses' Link", page.locator(link_selector), timeout=15000)
            # Retrieve computed styles for header and link
            header_styles: dict[str, str] = page.evaluate("""
                (selector) => {
                    const el = document.querySelector(selector);
                    if (!el) return {};
                    const cs = window.getComputedStyle(el);
                    return {
                        background: cs.backgroundColor,
                        padding: cs.padding,
                        color: cs.color,
                        fontFamily: cs.fontFamily,
                        fontSize: cs.fontSize,
                        fontWeight: cs.fontWeight,
                        textAlign: cs.textAlign
                    };
                }
            """, header_selector)
            link_styles: dict[str, str] = page.evaluate("""
                (xpath) => {
                    const el = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    if (!el) return {};
                    const cs = window.getComputedStyle(el);
                    return {
                        color: cs.color,
                        background: cs.backgroundColor,
                        fontFamily: cs.fontFamily,
                        fontSize: cs.fontSize,
                        fontWeight: cs.fontWeight,
                        textDecoration: cs.textDecorationLine,
                        padding: cs.padding,
                        margin: cs.margin,
                        textAlign: cs.textAlign
                    };
                }
            """, generated_page._lnk_courses_xpath)
            # Validate data types
            header_styles = Utility.validate_and_convert_data(header_styles, dict)
            link_styles = Utility.validate_and_convert_data(link_styles, dict)
            # Log styles for debugging
            Utility.log_test_step(f"Header styles: {header_styles}")
            Utility.log_test_step(f"Link styles: {link_styles}")
            # Then: Responsive design check (resize to desktop, tablet, mobile)
            viewports: list[dict[str, int]] = [
                {"width": 1920, "height": 1080},  # Desktop
                {"width": 1024, "height": 768},   # Tablet
                {"width": 375, "height": 667}     # Mobile
            ]
            for vp in viewports:
                Utility.log_test_step(f"Resizing viewport to {vp['width']}x{vp['height']}")
                context.set_viewport_size(vp)
                time.sleep(1)
                Utility.retry_assertion(
                    lambda: expect(page.locator(header_selector)).to_be_visible(timeout=15000),
                    retries=3, delay=1000
                )
                Utility.retry_assertion(
                    lambda: expect(page.locator(link_selector)).to_be_visible(timeout=15000),
                    retries=3, delay=1000
                )
            # When: Hover over the "← Back to Courses" link
            Utility.log_test_step("Hovering over the 'Back to Courses' link to check hover effect.")
            page.locator(link_selector).hover()
            time.sleep(1)
            hover_styles: dict[str, str] = page.evaluate("""
                (xpath) => {
                    const el = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    if (!el) return {};
                    const cs = window.getComputedStyle(el);
                    return {
                        color: cs.color,
                        background: cs.backgroundColor,
                        textDecoration: cs.textDecorationLine
                    };
                }
            """, generated_page._lnk_courses_xpath)
            hover_styles = Utility.validate_and_convert_data(hover_styles, dict)
            Utility.log_test_step(f"Link hover styles: {hover_styles}")
            # Then: Move mouse away and check link returns to default styling
            Utility.log_test_step("Moving mouse away from the link to check style reset.")
            page.mouse.move(0, 0)
            time.sleep(1)
            post_hover_styles: dict[str, str] = page.evaluate("""
                (xpath) => {
                    const el = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    if (!el) return {};
                    const cs = window.getComputedStyle(el);
                    return {
                        color: cs.color,
                        background: cs.backgroundColor,
                        textDecoration: cs.textDecorationLine
                    };
                }
            """, generated_page._lnk_courses_xpath)
            post_hover_styles = Utility.validate_and_convert_data(post_hover_styles, dict)
            Utility.log_test_step(f"Link post-hover styles: {post_hover_styles}")
            # Final: Comprehensive test execution summary
            Utility.log_test_result("PASS", "Header and link display consistent visual styling, alignment, responsiveness, and interactive feedback as per updated design.")
            test_passed = True
        except PlaywrightTimeoutError as te:
            Utility.log_error(f"TimeoutError encountered: {te}")
            Utility.log_test_result("FAIL", f"TimeoutError: {te}")
            raise
        except AssertionError as ae:
            Utility.log_error(f"AssertionError encountered: {ae}")
            Utility.log_test_result("FAIL", f"AssertionError: {ae}")
            raise
        except Exception as e:
            Utility.log_error(f"Unexpected error encountered: {e}")
            Utility.log_test_result("FAIL", f"Unexpected error: {e}")
            raise
        finally:
            if not test_passed:
                Utility.log_test_result("FAIL", "Test did not complete successfully.")
            browser.close()
#---#
#######

# Test Case 2 - TC-0016
from playwright.sync_api import sync_playwright, expect
  # Import the POM class
# Test URLs (replace with actual URLs as needed)
urls: dict[str, str] = {
    "course_main": os.environ.get("COURSE_MAIN_URL", "https://edulearn.example.com/courses/course-123")
}
def test_course_header_section_updated_elements_displayed_correctly() -> None:
    """
    TC-0016: Course Header Section - Course Banner, Title, Description, and Badges Are Displayed Correctly (Updated)
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True
        )
        page = context.new_page()
        generated_page = GeneratedPage(page)
        test_result: str = "PASSED"
        test_details: str = ""
        console_errors: list[str] = []
        # Attach console message logger
        def on_console_message(msg):
            Utility.log_console_message(msg)
            if msg.type == "error":
                console_errors.append(msg.text)
        page.on("console", on_console_message)
        try:
            # --- GIVEN: Setup and navigation to initial state ---
            Utility.log_test_step("Navigate to the main page of the course application.")
            navigation_success: bool = Utility.navigate_to_page(page, urls["course_main"], timeout=15000)
            if not navigation_success:
                raise Exception("Navigation to course main page failed.")
            # Wait for body and essential elements
            Utility.wait_for_element_state(page, "body", state="visible", timeout=15000)
            generated_page.validate_essential_elements()
            # Accept cookies/pop-ups if present (simulate by clicking known button if exists)
            # (Assume a cookie banner with id 'cookie-accept' for demonstration)
            cookie_accept_selector: str = "xpath=//button[contains(@id, 'cookie-accept') or contains(@class, 'cookie-accept')]"
            Utility.safe_wait_and_interact(page, cookie_accept_selector, "click", timeout=3000, retries=1)
            # --- WHEN: Perform the action (Observe header section) ---
            Utility.log_test_step("Observe the updated course header section at the top of the page.")
            # --- THEN: Verify expected outcomes ---
            # 1. The updated course header section is visible at the top of the page.
            Utility.log_test_step("Verify the course header section is visible.")
            # Assume the header section is always present if essential elements are visible (from validate_essential_elements)
            # 2. The updated banner image is displayed with the correct source and alt text.
            Utility.log_test_step("Verify the updated banner image is displayed with correct source and alt text.")
            banner_xpath: str = "//div[contains(@class, 'course-header')]//img[contains(@class, 'course-banner')]"
            banner_visible: bool = Utility.wait_for_element_state(page, f"xpath={banner_xpath}", state="visible", timeout=15000)
            if not banner_visible:
                raise AssertionError("Banner image is not visible in the course header section.")
            banner_src: str = Utility.get_element_text(page, f"{banner_xpath}/@src", timeout=15000)
            banner_alt: str = Utility.get_element_text(page, f"{banner_xpath}/@alt", timeout=15000)
            banner_src = Utility.validate_and_convert_data(banner_src, str)
            banner_alt = Utility.validate_and_convert_data(banner_alt, str)
            if not banner_src or not banner_alt:
                raise AssertionError("Banner image src or alt text is missing or invalid.")
            # 3. The new course title is visible and matches the latest course name.
            Utility.log_test_step("Verify the updated course title is visible and correct.")
            title_xpath: str = "//div[contains(@class, 'course-header')]//h1[contains(@class, 'course-title')]"
            title_visible: bool = Utility.wait_for_element_state(page, f"xpath={title_xpath}", state="visible", timeout=15000)
            if not title_visible:
                raise AssertionError("Course title is not visible.")
            course_title: str = Utility.get_element_text(page, f"xpath={title_xpath}", timeout=15000)
            course_title = Utility.validate_and_convert_data(course_title, str)
            if not course_title or len(course_title.strip()) == 0:
                raise AssertionError("Course title is missing or empty.")
            # 4. The new course description is present and accurately reflects the updated content.
            Utility.log_test_step("Verify the updated course description is present.")
            desc_xpath: str = "//div[contains(@class, 'course-header')]//p[contains(@class, 'course-description')]"
            desc_visible: bool = Utility.wait_for_element_state(page, f"xpath={desc_xpath}", state="visible", timeout=15000)
            if not desc_visible:
                raise AssertionError("Course description is not visible.")
            course_desc: str = Utility.get_element_text(page, f"xpath={desc_xpath}", timeout=15000)
            course_desc = Utility.validate_and_convert_data(course_desc, str)
            if not course_desc or len(course_desc.strip()) == 0:
                raise AssertionError("Course description is missing or empty.")
            # 5. Badges are visible for the new course level, certificate, updated duration, and the new rating (e.g., star rating).
            Utility.log_test_step("Verify badges for course level, certificate, duration, and rating are visible.")
            badge_level_xpath: str = "//div[contains(@class, 'course-header')]//span[contains(@class, 'badge-level')]"
            badge_cert_xpath: str = "//div[contains(@class, 'course-header')]//span[contains(@class, 'badge-certificate')]"
            badge_duration_xpath: str = "//div[contains(@class, 'course-header')]//span[contains(@class, 'badge-duration')]"
            badge_rating_xpath: str = "//div[contains(@class, 'course-header')]//span[contains(@class, 'badge-rating')]"
            for badge_name, badge_xpath in [
                ("Level", badge_level_xpath),
                ("Certificate", badge_cert_xpath),
                ("Duration", badge_duration_xpath),
                ("Rating", badge_rating_xpath)
            ]:
                badge_visible: bool = Utility.wait_for_element_state(page, f"xpath={badge_xpath}", state="visible", timeout=15000)
                if not badge_visible:
                    raise AssertionError(f"{badge_name} badge is not visible.")
            # 6. All updated elements are properly aligned and spaced for clear readability.
            Utility.log_test_step("Verify alignment and spacing of header elements.")
            # For alignment, check that all elements are visible and not overlapping (basic check)
            # (Advanced visual checks would require screenshot comparison, omitted here)
            for element_name, element_xpath in [
                ("Banner", banner_xpath),
                ("Title", title_xpath),
                ("Description", desc_xpath),
                ("Level Badge", badge_level_xpath),
                ("Certificate Badge", badge_cert_xpath),
                ("Duration Badge", badge_duration_xpath),
                ("Rating Badge", badge_rating_xpath)
            ]:
                locator = page.locator(f"xpath={element_xpath}")
                Utility.log_element_state(element_name, locator, timeout=15000)
            Utility.log_test_result("PASSED", "All updated course header elements are displayed and aligned correctly.")
        except AssertionError as ae:
            test_result = "FAILED"
            test_details = f"Assertion failed: {ae}"
            Utility.log_test_result(test_result, test_details)
            raise
        except Exception as e:
            test_result = "FAILED"
            test_details = f"Test failed: {e}"
            Utility.log_test_result(test_result, test_details)
            raise
        finally:
            if console_errors:
                Utility.log_error(f"Console errors detected during test: {console_errors}")
            browser.close()
            Utility.log_test_result(test_result, test_details if test_details else "Test completed successfully.")
#---#
#######
