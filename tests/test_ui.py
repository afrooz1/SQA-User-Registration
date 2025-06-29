
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from datetime import datetime

class RegistrationBlackBoxTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.base_url = "http://localhost:5000"
        
        
        cls.evidence_dir = "test_evidence"
        os.makedirs(cls.evidence_dir, exist_ok=True)
        
        
        cls.action_delay = 2.0  
        cls.message_delay = 1.5  

    def clear_input_fields(self):
        """Clear form fields between tests"""
        self.driver.find_element(By.ID, "name").clear()
        self.driver.find_element(By.ID, "email").clear()
        time.sleep(self.action_delay/2)

    def capture_message_only(self, test_name):
        """
        Capture screenshot of just the message area
        Hides sensitive input data
        """
        
        self.driver.execute_script(
            "document.getElementById('name').style.display='none';"
            "document.getElementById('email').style.display='none';"
            "document.querySelector('button[type=\"submit\"]').style.display='none';"
        )
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.evidence_dir}/{test_name}_message_{timestamp}.png"
        self.driver.save_screenshot(filename)
        
        
        self.driver.execute_script(
            "document.getElementById('name').style.display='block';"
            "document.getElementById('email').style.display='block';"
            "document.querySelector('button[type=\"submit\"]').style.display='block';"
        )
        
        print(f"Message captured: {filename}")
        time.sleep(self.message_delay)

    def slow_type(self, element, text):
        """Type text slowly character by character"""
        actions = ActionChains(self.driver)
        for character in text:
            actions.send_keys_to_element(element, character)
            actions.perform()
            time.sleep(self.action_delay/len(text))

    def submit_form(self, name, email):
        """Submit registration form with controlled speed"""
        self.driver.get(self.base_url)
        time.sleep(self.action_delay)
        
        name_field = self.driver.find_element(By.ID, "name")
        email_field = self.driver.find_element(By.ID, "email")
        
        self.slow_type(name_field, name)
        self.slow_type(email_field, email)
        
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        time.sleep(self.action_delay)

    
    def test_01_valid_registration(self):
        """Test successful registration with valid data"""
        test_name = "Test User"
        test_email = f"test_{datetime.now().strftime('%H%M%S')}@example.com"
        
        self.submit_form(test_name, test_email)
        
       
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success")))
        self.capture_message_only("valid_registration")
        
        success_msg = self.driver.find_element(By.CLASS_NAME, "alert-success").text
        self.assertEqual(success_msg, "Registration successful!")
        self.clear_input_fields()

    def test_02_invalid_email_format(self):
        """Test registration with invalid email format"""
        self.submit_form("Invalid Email User", "not-an-email")
        
        
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-error")))
        self.capture_message_only("invalid_email")
        
        error_msg = self.driver.find_element(By.CLASS_NAME, "alert-error").text
        self.assertEqual(error_msg, "Invalid email format!")
        self.clear_input_fields()

    def test_03_duplicate_email(self):
        """Test registration with duplicate email"""
        
        test_name = "Original User"
        test_email = "duplicate_test@example.com"
        self.submit_form(test_name, test_email)
        time.sleep(self.action_delay)
        
        
        self.submit_form("Duplicate User", test_email)
        
        
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-error")))
        self.capture_message_only("duplicate_email")
        
        error_msg = self.driver.find_element(By.CLASS_NAME, "alert-error").text
        self.assertEqual(error_msg, "Email already exists!")
        self.clear_input_fields()

    def test_04_empty_fields(self):
        """Test registration with empty fields"""
        self.driver.get(self.base_url)
        time.sleep(self.action_delay)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(self.action_delay)
        
        
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-error")))
        self.capture_message_only("empty_fields")
        
        error_msg = self.driver.find_element(By.CLASS_NAME, "alert-error").text
        self.assertEqual(error_msg, "Name and email are required!")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()