from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # I order to view a to-do app, I go to the to-list app's homepage
        self.browser.get("http://localhost:8000")

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

        # When I hit enter, the page updates, and now the page lists "1: 
        # Buy peacock
        # feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn("1: Buy peacock feathers", [row.text for row in rows])

        # There is still a textbox inviting me to add a another item.
        # I enter "Use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on my list
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn("1: Buy peacock feathers", [row.text for row in rows])
        self.assertIn("2: Use peacock feathers to make a fly", 
            [row.text for row in rows])
        
        # I see that the site has generated a unique URL for my list and an 
        # explanation that this is to get back to this list
        self.fail("Finish the test!")
        # I visit the URL and my to-list is still there


if __name__ == "__main__":
    unittest.main(warnings="ignore")
