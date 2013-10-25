from lib.ui_lib import *


#*********************************************************************************
# Description: Verify "Adding an Order" functionality in control panel
# Author: Jyothi   Email: nagajyothi.noubadi@bigcommerce.com
#*********************************************************************************


def test_ORDERS_addOrder(browser, url, username, password):
	""" Verify 'Adding an Order' functionality in control panel """
	# Initialise browser and enter credentials
	go_to_admin(browser, url, username, password)

	# Select "Orders" menu
	element = wait_until_element_present(browser, 'Orders', "LINK")
	element.click()

	
	try:
		#Select "Add an Order" in "Orders" menu
		browser.find_element_by_link_text('Add an Order').click()
	
	except NoSuchElementException:
		browser.save_screenshot('NoSuchElementException.png')
		raise


	# Select "NewCustomer" radio button in customer info
	element = wait_until_element_present(browser, '//label[@for = "check-new-customer"]', "XPATH")
	element.click()

	try:
		#Provide customer information
		browser.find_element_by_id('FormField_1').send_keys(Emailid)
		browser.find_element_by_id('FormField_2').send_keys(paswd)
		browser.find_element_by_id('FormField_3').send_keys(confirmpaswd)

	except NoSuchElementException:
		browser.save_screenshot('FieldNotFound.png')
		raise

	#Select customer group
	select_dropdown_value(browser, 'accountCustomerGroup', '-- Do not assign to any group --')

	try:
		#Provide Billing Information
		browser.find_element_by_id('FormField_4').send_keys(FirstName)
		browser.find_element_by_id('FormField_5').send_keys(LastName)
		browser.find_element_by_id('FormField_6').send_keys(CompanyName)
		browser.find_element_by_id('FormField_7').send_keys(PhoneNumber)
		browser.find_element_by_id('FormField_8').send_keys(Addressline1)
		browser.find_element_by_id('FormField_9').send_keys(Addressline1)
		browser.find_element_by_id('FormField_10').send_keys(city)

	except NoSuchElementException:
		browser.save_screenshot('FieldNotFound.png')
		raise

	#Select country and state
	select_dropdown_value(browser, 'FormField_11', country)
	select_dropdown_value(browser, 'FormField_12', state)

	try:
		# Provide zip/postal code
		clear_field(browser,'FormField_13')
		browser.find_element_by_id('FormField_13').send_keys(postcode)

		# Proceed to next step
		browser.find_element_by_xpath('//button[text() = "Next"]').click()
		time.sleep(5)

	except NoSuchElementException:
		browser.save_screenshot('PostcodeNotFound.png')
		raise


		# Browse categories by passing product name
	element = wait_until_element_present(browser, 'quote-item-search', "ID")
	element.send_keys(Search)
		
	try:
		browser.find_element_by_id("quote-item-search").send_keys(Keys.RETURN)
		#Switch the control to pop-up window
		for handle in browser.window_handles:
			browser.switch_to_window(handle)

		# Search required product
		element = wait_until_element_present(browser, 'searchQuery', "ID")
		element.send_keys(Search)

		# Select the required product and proceed
		element = wait_until_element_present(browser, '//option[text() = "'+Search+'"]', "XPATH")
		element.click()
		browser.find_element_by_xpath('//input[@value = "Select"]').click()

		#Switch control to main window
		for handle in browser.window_handles:
			time.sleep(5)
			browser.switch_to_window(handle)
		time.sleep(3)

		# Enter required quantity and proceed further
		clear_field(browser,'qty')
		time.sleep(5)
		element = wait_until_element_present(browser, '//button[text() = "Ok"]', "XPATH")
		element.click()
		browser.find_element_by_name('quantity').send_keys(qty)
		browser.find_element_by_xpath('//button[text() = "Next"]').click()

		# Shipping address section and proceed further
		browser.find_element_by_xpath('//label[@for = "shipping-single"]').click()
		browser.find_element_by_xpath('//button[text() = "Next"]').click()
		
		# Select Manual Payment and provide Name
		select_dropdown_value(browser, 'paymentMethod', 'Manual Payment')
		browser.find_element_by_name('paymentField[custom][custom_name]').send_keys(Manualpayment_name)
		browser.find_element_by_xpath('//button[@class = "btn btn-primary orderMachineSaveButton orderSaveButton"]').click()
		

		# Verify and Assert the success message as the order is created succesfully.
		browser_success_msg = wait_until_element_present(browser, '//div[@class = "alert alert-success"]/p', "XPATH").text
		if order_success_msg in browser_success_msg:
			print "I found my order success message successfully"
			assert True
		else:
			print "Order success message could not found"
			assert False


	except NoSuchElementException:
		browser.save_screenshot('Nosuchelement.png')
		raise
	
	except TimeoutException:
		browser.save_screenshot('timeout.png')
		raise

	except ElementNotVisibleException:
		browser.save_screenshot('ElementNotVisibleException.png')
		raise

	# Any other exception
	except Exception:
		browser.save_screenshot('exception.png')
		raise



#Test Data	
Emailid='nagajyothi+test5@bigcommerce.com'
paswd='vsspl678'
confirmpaswd='vsspl678'
FirstName='Jyothi'
LastName='N'
CompanyName='My company'
PhoneNumber='9876785868'
Addressline1='Hyd'
Addressline2='Hyd'
city='Hyd'
country='India'
state='Andhra Pradesh'
postcode='500054'
Search='Blue ear rings'
qty='2'
Manualpayment_name='Jyothi'
order_success_msg="has been created successfully."
