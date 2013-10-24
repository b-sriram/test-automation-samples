from lib.ui_lib import *

#Create an Order in Control Panel
def test_add_order_for_customer(browser, url, username, password):
	go_to_admin(browser, url, username, password)

	#Adding an order
	element = wait_until_element_present(browser, 'Orders', "LINK")
	element.click()
	browser.find_element_by_link_text('Add an Order').click()
	element = wait_until_element_present(browser, '//label[@for = "check-new-customer"]', "XPATH")
	element.click()

	#Customer Info
	browser.find_element_by_id('FormField_1').send_keys(Emailid)
	browser.find_element_by_id('FormField_2').send_keys(paswd)
	browser.find_element_by_id('FormField_3').send_keys(confirmpaswd)
	select_dropdown_value(browser, 'accountCustomerGroup', '-- Do not assign to any group --')
	browser.find_element_by_id('FormField_4').send_keys(FirstName)
	browser.find_element_by_id('FormField_5').send_keys(LastName)
	browser.find_element_by_id('FormField_6').send_keys(CompanyName)
	browser.find_element_by_id('FormField_7').send_keys(PhoneNumber)
	browser.find_element_by_id('FormField_8').send_keys(Addressline1)
	browser.find_element_by_id('FormField_9').send_keys(Addressline1)
	browser.find_element_by_id('FormField_10').send_keys(city)
	select_dropdown_value(browser, 'FormField_11', country)
	select_dropdown_value(browser, 'FormField_12', state)
	clear_field(browser,'FormField_13')
	browser.find_element_by_id('FormField_13').send_keys(postcode)
	browser.find_element_by_xpath('//button[text() = "Next"]').click()


	#Searching an item in an order
	element = wait_until_element_present(browser, 'quote-item-search', "ID")
	element.send_keys(Search)
	browser.find_element_by_id("quote-item-search").send_keys(Keys.RETURN)
	for handle in browser.window_handles:
		browser.switch_to_window(handle)
	element = wait_until_element_present(browser, 'searchQuery', "ID")
	element.send_keys(Search)
	element = wait_until_element_present(browser, '//option[text() = "'+Search+'"]', "XPATH")
	element.click()
	browser.find_element_by_xpath('//input[@value = "Select"]').click()
	for handle in browser.window_handles:
		browser.switch_to_window(handle)
	clear_field(browser,'qty')
	for handle in browser.window_handles:
		browser.switch_to_window(handle)
	element = wait_until_element_present(browser, '//button[text() = "Ok"]', "XPATH")
	element.click()
	browser.find_element_by_name('quantity').send_keys(qty)
	browser.find_element_by_xpath('//button[text() = "Next"]').click()



	#Selecting Shipping address
	browser.find_element_by_xpath('//label[@for = "shipping-single"]').click()
	browser.find_element_by_xpath('//button[text() = "Next"]').click()
	


	#Selecting Payment method
	select_dropdown_value(browser, 'paymentMethod', 'Manual Payment')
	browser.find_element_by_name('paymentField[custom][custom_name]').send_keys(Manualpayment_name)
	browser.find_element_by_xpath('//button[@class = "btn btn-primary orderMachineSaveButton orderSaveButton"]').click()
	

	#Asserting the success message   
	browser_success_msg = wait_until_element_present(browser, '//div[@class = "alert alert-success"]/p', "XPATH").text
	if order_success_msg in browser_success_msg:
		print "I found my order success message successfully"
		assert True
	else:
		print "Order success message could not found"
		assert False

#Test Data	
Emailid='nagajyothi+test1@bigcommerce.com'
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
