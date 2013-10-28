from lib.ui_lib import *

# -------------------- Work in Progress

#*********************************************************************************
# Description: Verify and Assert "Edit an Order" functionality in control panel
# Select Order menu-->View Order-->Select an Order and Edit an Order
# Verify and Assert Edit Order Functionality.
# Author: Jyothi   Email: nagajyothi.noubadi@bigcommerce.com
#*********************************************************************************

def test_ORDERS_editOrder(browser, url, username, password):
	""" Verify and Assert 'Edit an Order' functionality in control panel"""
	
	# Initialise browser and pass credentials
	go_to_admin(browser, url, username, password)
	element = wait_until_element_present(browser, 'Orders', "LINK")
	
	
	try:
		#Go to "Orders"
		element.click()
		# Go to view orders page
		browser.find_element_by_link_text('View Orders').click()
		WebDriverWait(browser, time).until(lambda s: s.find_element_by_xpath("//tr[contains(., '" + orderID + "')]").is_displayed())
		
		
		# Select specific order to edit by providing orderID
		browser.find_element_by_xpath("//tr[contains(., '" + orderID + "')]").find_element_by_css_selector('.dropdown-trigger').click()
		
		# Edit order by clearing the fileds and entering the respective values
		browser.find_element_by_link_text('Edit Order').click()
		browser.find_element_by_id('FormField_4').clear()
		browser.find_element_by_id('FormField_4').send_keys(FirstName)
		browser.find_element_by_id('FormField_5').clear()
		browser.find_element_by_id('FormField_5').send_keys(LastName)
		browser.find_element_by_id('FormField_6').clear()
		browser.find_element_by_id('FormField_6').send_keys(CompanyName)
		browser.find_element_by_id('FormField_7').clear()
		browser.find_element_by_id('FormField_7').send_keys(PhoneNumber)
		browser.find_element_by_id('FormField_8').clear()
		browser.find_element_by_id('FormField_8').send_keys(Addressline1)
		browser.find_element_by_id('FormField_9').clear()
		browser.find_element_by_id('FormField_9').send_keys(Addressline1)
		browser.find_element_by_id('FormField_10').clear()
		browser.find_element_by_id('FormField_10').send_keys(city)
	except NoSuchElementException:
		browser.save_screenshot('NoSuchElementException.png')
		raise
	except TimeoutException:
		browser.save_screenshot('timeout.png')
		raise
	except WebDriverException:
		browser.save_screenshot('webdriverexception.png')
		raise

	# Any other exception
	except Exception:
		browser.save_screenshot('exception.png')
		raise		

	# Select Country and State options
	select_dropdown_value(browser, 'FormField_11', country)
	select_dropdown_value(browser, 'FormField_12', state)
	

	try:
		browser.find_element_by_id('FormField_13').clear()
		browser.find_element_by_id('FormField_13').send_keys(postcode)
		
		# Select Next button to enter Quantity of an edited order
		browser.find_element_by_xpath('//button[text() = "Next"]').click()
		WebDriverWait(browser, time).until(lambda s: s.find_element_by_name('quantity').is_displayed())
		browser.find_element_by_name('quantity').clear()
		
	except NoSuchElementException:
		browser.save_screenshot('NoSuchElementException.png')
		raise
	except TimeoutException:
		browser.save_screenshot('timeout.png')
		raise
	except WebDriverException:
		browser.save_screenshot('webdriverexception.png')
		raise

	# Any other exception
	except Exception:
		browser.save_screenshot('exception.png')
		raise				
	

	try:
		# Quantity field validation Pop-up handler
		WebDriverWait(browser, time).until(lambda s: s.find_element_by_xpath('//button[text() = "Ok"]').is_displayed())
		element = browser.find_element_by_xpath('//button[text() = "Ok"]')
		element.click()
	except NoSuchElementException:
		pass
	except WebDriverException:
		browser.save_screenshot('webdriverexception.png')
		raise
	except TimeoutException:
		browser.save_screenshot('timeout.png')
		raise
		
	try:
		# Provide order quantity and go to next step
		browser.find_element_by_name('quantity').send_keys(qty)
		WebDriverWait(browser, time).until(lambda s: s.find_element_by_xpath('//button[text() = "Next"]').is_displayed())
		browser.find_element_by_xpath('//button[text() = "Next"]').click()
		WebDriverWait(browser, time).until(lambda s: s.find_element_by_xpath('//label[@for = "shipping-billing"]').is_displayed())

		# Navigate Shipping, Payment sections and Save the order
		browser.find_element_by_xpath('//label[@for = "shipping-billing"]').click()
		browser.find_element_by_xpath('//button[text() = "Next"]').click()
		WebDriverWait(browser, time).until(lambda s: s.find_element_by_xpath('//button[@class = "btn btn-primary orderMachineSaveButton orderSaveButton"]').is_displayed())
		browser.find_element_by_xpath('//button[@class = "btn btn-primary orderMachineSaveButton orderSaveButton"]').click()
		WebDriverWait(browser, time).until(lambda s: s.find_element_by_xpath('//div[@class = "alert alert-success"]/p').is_displayed())
		

		# Assert the success message   
		browser_success_msg = wait_until_element_present(browser, '//div[@class = "alert alert-success"]/p', "XPATH").text
	
		if order_success_msg in browser_success_msg:
			# print/log "Edit Order Working Successfully"
			assert True
		else:
			# print/log "Edit Order Unsuccessfull"
			assert False

	except NoSuchElementException:
		browser.save_screenshot('NoSuchElementException.png')
		raise
	except TimeoutException:
		browser.save_screenshot('timeout.png')
		raise
	except WebDriverException:
		browser.save_screenshot('webdriverexception.png')
		raise

	# Any other exception
	except Exception:
		browser.save_screenshot('exception.png')
		raise				



# Test Data	
time=30
FirstName='Naga Jyothi'
LastName='N'
CompanyName='Bigcommerce'
PhoneNumber='9876868979'
Addressline1='Hyd'
Addressline2='Hyd'
city='Hyd'
country='India'
state='Andhra Pradesh'
postcode='500054'
Search='Blue ear rings'
qty='3'
orderID='114'
order_success_msg= "The order #%s has been updated successfully." % orderID

