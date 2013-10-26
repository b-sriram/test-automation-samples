from lib.ui_lib import *

#*********************************************************************************
# Description: Verify Shipping item option from View Orders table
# Author: Sravan    EmailID:sravan.kumar@bigcommerce.com
#*********************************************************************************

def test_ORDERS_shipitem(browser, url, username, password):
	""" Verify Shipping item option from View Orders table """
	
	# Initialise browser, provide credentials and select Orders menu 
	go_to_admin(browser, url, username, password)
	element = wait_until_element_present(browser, 'Orders', "LINK")
	element.click()
	
	try:
		# Select Order to be shipped among list of orders and proceed to ship items
		browser.find_element_by_link_text('View Orders').click()
		browser.find_element_by_xpath("//tr[contains(., '" + orderID + "')]").find_element_by_css_selector('.dropdown-trigger').click()
		time.sleep(4)
		browser.find_element_by_link_text('Ship Items').click()
		
		# Select shipping module and provide respective shipping options to create shipment
		select_dropdown_value(browser, 'shipping_module', shipping_module)
		browser.find_element_by_id('shipmethod').send_keys(shipmethod_desc)
		browser.find_element_by_id('shiptrackno').send_keys(shiptrack_no)
		browser.find_element_by_id('shipcomments').send_keys(ship_comments)
		browser.find_element_by_name('CreateShiptment').click()
		time.sleep(4)
		browser.find_element_by_link_text('Shipped').click()
		browser.find_element_by_xpath("//tr[contains(., '" + orderID + "')]")



	except NoSuchElementException:
		browser.save_screenshot('Nosuchelement.png')
		raise



# Test Data
orderID='119'
shipping_module='Australia Post'
shipmethod_desc='My ship desc'
shiptrack_no='8768790'
ship_comments='Ship these items'