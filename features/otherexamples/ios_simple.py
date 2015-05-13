"""
Simple iOS tests, showing accessing elements and getting/setting text from them.
"""
import unittest
import os
from random import randint
from appium import webdriver
from time import sleep

class SimpleIOSTests(unittest.TestCase):

    def setUp(self):
        # set up appium
        app = os.path.join(os.path.dirname(__file__),
                           '../../apps/TestApp/build/Release-iphone',
                           'TestApp.app')
        app = os.path.abspath(app)
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723/wd/hub',
            desired_capabilities={
                'app': app,
                'platformName': 'iOS',
                'platformVersion': '8.3',
                'deviceName': 'iPhone 6'
                # 'deviceName' : None,
                # 'udid' : '03ecba20f42e7fef25632d9b30cd0c8a5b447e92'
            })

    def tearDown(self):
        self.driver.quit()

    def _populate(self):
        # populate text fields with two random numbers
        # els = self.driver.find_elements_by_ios_uiautomation('elements()')
        els = [self.driver.find_element_by_name('TextField1'),
               self.driver.find_element_by_name('TextField2')]

        self._sum = 0
        for i in range(2):
            rnd = randint(0, 10)
            els[i].send_keys(rnd)
            self._sum += rnd

    def test_ui_computation(self):
        # populate text fields with values
        self._populate()

        # trigger computation by using the button
        self.driver.find_element_by_accessibility_id('ComputeSumButton').click()

        # is sum equal ?
        # sauce does not handle class name, so get fourth element
        sum = self.driver.find_element_by_name('Answer').text
        self.assertEqual(int(sum), self._sum)

    def test_scroll(self):
        els = self.driver.find_elements_by_class_name('UIAButton')
        els[5].click()


        sleep(2)
        try:
            el = self.driver.find_element_by_accessibility_id('OK')
            el.click()
            sleep(2)
        except:
            pass

        el = self.driver.find_element_by_xpath('//UIAMapView[1]')

        location = el.location
        self.driver.swipe(start_x=location['x'], start_y=location['y'], end_x=0.5, end_y=location['y'], duration=800)




if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleIOSTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
