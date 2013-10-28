from lib.ui_lib import *
from selenium.webdriver.support.ui import WebDriverWait

#*********************************************************************************
# Description: Verify Shipping item option from View Orders table
# Select order menu -> view orders -> select ship item of an order 
# Verify that shipped item's order id exists in the list
# Author: Sravan    EmailID:sravan.kumar@bigcommerce.com
#*********************************************************************************

def test_ORDERS_shipitem(browser, url, username, password):
	""" Verify Shipping item option from View Orders table """
	
	# Initialise browser, provide credentials and select Orders menu 
	go_to_admin(browser, url, username, password)
	element = wait_until_element_present(browser, 'Orders', "LINK")
		
	# Assumption: Any exceptions thrown will be caught by test framework
	try:
		# Go to orders 
		element.click()

		# Select Order to be shipped among list of orders and proceed to ship items
		browser.find_element_by_link_text('View Orders').click()
		WebDriverWait(browser, time).until(lambda s: s.find_element_by_xpath("//tr[contains(., '" + orderID + "')]").is_displayed())
		browser.find_element_by_xpath("//tr[contains(., '" + orderID + "')]").find_element_by_css_selector('.dropdown-trigger').click()
		browser.find_element_by_link_text('Ship Items').click()
		
		# Select shipping module and provide respective shipping options to create shipment
		select_dropdown_value(browser, 'shipping_module', shipping_module)
		browser.find_element_by_id('shipmethod').send_keys(shipmethod_desc)
		browser.find_element_by_id('shiptrackno').send_keys(shiptrack_no)
		browser.find_element_by_id('shipcomments').send_keys(ship_comments)
		browser.find_element_by_name('CreateShiptment').click()
		
		# This wait function waits for 30 seconds (standard being used in other test code)
		WebDriverWait(browser,time).until(lambda s: s.find_element_by_link_text('Custom Views').is_displayed())
		browser.find_element_by_link_text('Shipped').click()
		WebDriverWait(browser,time).until(lambda s: s.find_element_by_xpath("//tr[contains(., '" + orderID + "')]").is_displayed())
				
		# Check if orderID is present in the list of shipped items
		# If order found this browser.find element returns true
		# Assumption is that a TRUE assertion will be taken by test framework as test pass & vice versa

		if (browser.find_element_by_xpath("//tr[contains(., '" + orderID + "')]")):
			assert True
			# print/log.... test passed			
		else:
			assert False
			# Print/log... test failed, order id 128 is not found in the shipment list
		print odd
			
	except NoSuchElementException:
		browser.save_screenshot('Nosuchelement.png')
		raise
	
	except TimeoutException:
		browser.save_screenshot('timeout.png')
		raise

	except WebDriverException:
		browser.save_screenshot('WebDriverException.png')




# Test Data
time=30
orderID='119'
shipping_module='Australia Post'
shipmethod_desc='My ship desc'
shiptrack_no='8768790'
ship_comments='Ship these items'
success_msg='orders matched your search criteria and are shown below.'