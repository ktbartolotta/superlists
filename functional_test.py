from selenium import webdriver
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
        self.fail("Finish the test!")

        # I am invited to enter a to-do item straigt away

        # I type "Buy peacock feathers" into a textbox

        # When I hit enter, the page updates, and now the page lists "1: 
        # Buy peacock
        # feathers" as an item in a to-do list

        # There is still a textbox inviting me to adda another item.
        # I enter "Use peacock feathers to make a fly"

        # The page updates again, and now shows both items on my list

        # I see that the site has generated a unique URL for my list and an 
        # explanation that this is to get back to this list

        # I visit the URL and my to-list is still there


if __name__ == "__main__":
    unittest.main(warnings="ignore")
