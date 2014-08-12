from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # I order to view a to-do app, I go to the to-list app's homepage
        self.browser.get(self.live_server_url)

        # I notice the page title and header mention to-do-lists
        self.assertIn("To-Do", self.browser.title)
        
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        # I am invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(
                inputbox.get_attribute("placeholder"),
                "Enter a to-do item"
        )

        # I type "Buy peacock feathers" into a textbox
        inputbox.send_keys("Buy peacock feathers")

        # When I hit enter, I am taken to a new URL, 
        #and now the page lists "1: 
        # Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        my_list_url = self.browser.current_url
        self.assertRegex(my_list_url, "/lists/.+")
        self.check_for_row_in_list_table("1: Buy peacock feathers")

        # There is still a textbox inviting me to add a another item.
        # I enter "Use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on my list
        self.check_for_row_in_list_table("1: Buy peacock feathers")
        self.check_for_row_in_list_table(
                "2: Use peacock feathers to make a fly")
        
        # Now a new user comes along to the site

        ## We use a new browser session to make sure that no information
        ## of mine is coming through from cookies, etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # The new user visits the home page.  There is no sign of my list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)

        # The new user starts a new list by entering a new item.
        # He is less interesting than me...
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)
        
        # The new user get his own URL
        new_user_url = self.browser.current_url
        self.assertRegex(new_user_url, "/lists/.+")
        self.assertNotEqual(new_user_url, my_list_url)

        # Again, there is no trace of my list
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)

        #self.fail("Finish the test!")
        # I visit the URL and my to-list is still there

    def layout_and_styling(self):
        # I go to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # I notice that the input box is centered
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertAlmostEqual(
                inputbox.location["x"] + inputbox.size["width"] / 2,
                512,
                delta=5
        )

        # I start a new list and see the input is nicely
        # centered there too
        inputbox.send_keys("testing\n")
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertAlmostEqual(
                inputbox.location["x"] + inputbox.size["width"] / 2,
                512,
                delta=5
        )
