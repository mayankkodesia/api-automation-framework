
from Globals import logs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display
import time
import traceback
from selenium.common.exceptions import NoSuchElementException      
import commands
import os
import threading
from logging import thread


class Browser(object):
    '''
    This class consume all selenium methods to interact with browsers.
    '''
   
    def __init__(self, displayAvailable=True): 
        self.displayAvailable = displayAvailable
        if not displayAvailable:
            self.display = Display(visible=0, size=(1920, 1080))
            self.display.start()
    
    def openBrowser(self, browserType, driverPath, url,profilePath=None):
        try:
            if hasattr(self, "driver"):
                self.goToURL(url)
                return
#                 
            if browserType=="chrome":
                if profilePath:
                    options = webdriver.ChromeOptions() 
                    options.add_argument("user-data-dir="+ profilePath) #Path to your chrome profile
                    self.driver = webdriver.Chrome(driverPath,chrome_options=options)
                else:
                    self.driver = webdriver.Chrome(driverPath)
                    
            elif browserType == "firefox":
                if profilePath:
                    profile = webdriver.FirefoxProfile(profile_directory=profilePath)
                    os.environ['PATH'] = os.environ['PATH']+ ":" + driverPath
                    self.driver = webdriver.Firefox(firefox_profile=profile)
                else:
                    os.environ['PATH'] = os.environ['PATH']+ ":" + driverPath
                    self.driver = webdriver.Firefox()
                    
            self.driver.maximize_window()
#             t = threading.Thread(target=self.goToURL,args=(url,))
#             t.start()
            self.goToURL(url)            
        except Exception as e:
            traceback.print_exc()
            logs.error("Unable to open browser: " + browserType )              
     
    def goToURL(self, url):
        logs.debug("Navigating to URL: "+ url)
        if url:
            print "opening {}".format(url)
#             url = "http://www.google.com"
            self.driver.get(url)
            print "opened"
            
         
    def getDriver(self):
        return self.driver
    
    def click_on_visible_element(self, value):
        driver = self.driver
        webelements = driver.find_elements(By.XPATH, value)
        for element in webelements:
            if element.is_displayed():
                element.click()
                break
    
    def captureScreenshot(self, filename):
        self.driver.save_screenshot("../report/"+ filename)
    
    def closeBrowser(self):
        try:
            self.driver.quit()
            if not self.displayAvailable:
                self.display.stop()
        except Exception as e:
            print " Unable to close browser ", format(e)
    
    def selectTextFromAutoGenList(self, htmlID, text):
        self.driver.find_element_by_id(htmlID).send_keys(text)
        time.sleep(2)
        self.click_on_visible_element('//div[text()="' + text + '"]')    
    
    def inputTextInIframe(self, frameID, text):
        current = self.driver.current_window_handle
        self.driver.switch_to_frame(frameID)
        self.driver.find_element_by_tag_name("body").send_keys(text)
        self.driver.switch_to_window(current)

    def expandfoldableHeaderLink(self, linkName, id):
        driver = self.driver
        webelements = driver.find_elements(By.CLASS_NAME, "foldableHeaderLink")
        for element in webelements:
            if linkName in element.text:
                element.click()
                time.sleep(2)
                if not driver.find_element_by_id(id).is_displayed():
                    element.click()
                break
    
    def acceptAlert(self):
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
            self.driver.switch_to_alert().accept()
            print "alert accepted"
        except:
            print "no alert"
            
    def dismissedAlert(self):
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
            self.driver.switch_to_alert().dismiss()
            print "alert dismissed"
            time.sleep(10)
        except:
            print "no alert"
    
    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True
    
    def switchToTabs(self, tabIndex=0):
        # might not work on chrome, and work in firefox known issue in chrome
        windowName = self.driver.window_handles
        self.driver._switch_to.window(windowName[tabIndex])
        
    def switchToActiveWindow(self):
        windowName = self.driver.window_handles
        self.driver._switch_to.window(windowName[-1])
        
    
    def getWindowHandles(self):
        ''' return a list of window handles'''
        return self.driver.window_handles
     
# class TestSingleton(object):
#     
#     __instance = None
#     
#     def __init__(self):    
#         pass
#         
#     @staticmethod
#     def get_instance():
#         if not TestSingleton.__instnace:
#             TestSingleton.__instnace = TestSingleton()
#         return TestSingleton.__instnace
#     
    
    