from playwright.sync_api import Page, Locator, expect, TimeoutError as PlaywrightTimeoutError

class GeneratedPage:
    """
    Page Object Model for the EduLearn Course page.
    """

    def __init__(self, page: Page, timeout: int = 5000):
        """
        Initializes the GeneratedPage with XPath locators for interactable elements.

        :param page: Playwright Page object.
        :param timeout: Timeout in milliseconds for element interactions.
        """
        self._page = page
        self._timeout = timeout

        self._lnk_courses_xpath = "//a[@href='courses.html']"
        self._btn_enroll_xpath = "//button[@id='btn']"
        self._tab_overview_xpath = "//button[@onclick=\"openTab(event,'overview')\"]"
        self._tab_syllabus_xpath = "//button[@onclick=\"openTab(event,'syllabus')\"]"
        self._tab_resources_xpath = "//button[@onclick=\"openTab(event,'resources')\"]"

    def _safe_click(self, xpath: str):
        """
        Safely clicks an element specified by its XPath.

        :param xpath: XPath string of the element to click.
        """
        locator = self._page.locator(f"xpath={xpath}")
        expect(locator).to_be_visible(timeout=self._timeout)
        locator.click()

    def _safe_fill(self, xpath: str, text: str):
        """
        Safely fills an input or textarea element specified by its XPath.

        :param xpath: XPath string of the element to fill.
        :param text: Text to input.
        """
        locator = self._page.locator(f"xpath={xpath}")
        expect(locator).to_be_visible(timeout=self._timeout)
        locator.clear()
        locator.fill(text)

    def _safe_check(self, xpath: str):
        """
        Safely checks a checkbox or radio button specified by its XPath.

        :param xpath: XPath string of the element to check.
        """
        locator = self._page.locator(f"xpath={xpath}")
        expect(locator).to_be_visible(timeout=self._timeout)
        if not locator.is_checked():
            locator.check()

    def _safe_select(self, xpath: str, value: str):
        """
        Safely selects an option in a select element specified by its XPath.

        :param xpath: XPath string of the select element.
        :param value: Value attribute of the option to select.
        """
        locator = self._page.locator(f"xpath={xpath}")
        expect(locator).to_be_visible(timeout=self._timeout)
        locator.select_option(value)

    def click_courses_link(self):
        """
        Clicks the 'Courses' link in the navbar.
        """
        self._safe_click(self._lnk_courses_xpath)

    def click_enroll_button(self):
        """
        Clicks the 'Enroll' button.
        """
        self._safe_click(self._btn_enroll_xpath)

    def click_overview_tab(self):
        """
        Clicks the 'Overview' tab.
        """
        self._safe_click(self._tab_overview_xpath)

    def click_syllabus_tab(self):
        """
        Clicks the 'Syllabus' tab.
        """
        self._safe_click(self._tab_syllabus_xpath)

    def click_resources_tab(self):
        """
        Clicks the 'Resources' tab.
        """
        self._safe_click(self._tab_resources_xpath)

    def validate_essential_elements(self):
        """
        Validates that all essential elements are visible on the page.
        """
        locator = self._page.locator(f"xpath={self._lnk_courses_xpath}")
        expect(locator).to_be_visible(timeout=self._timeout)

        locator = self._page.locator(f"xpath={self._btn_enroll_xpath}")
        expect(locator).to_be_visible(timeout=self._timeout)

        locator = self._page.locator(f"xpath={self._tab_overview_xpath}")
        expect(locator).to_be_visible(timeout=self._timeout)

        locator = self._page.locator(f"xpath={self._tab_syllabus_xpath}")
        expect(locator).to_be_visible(timeout=self._timeout)

        locator = self._page.locator(f"xpath={self._tab_resources_xpath}")
        expect(locator).to_be_visible(timeout=self._timeout)