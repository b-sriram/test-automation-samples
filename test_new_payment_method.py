from mylib_lib import *


#Adding Secure Pay as a Payment Provider from controlpanel
def test_create_payment_method(browser, url, username, password):

	try:
		# Initialising browser and entering username and password
		go_to_admin(browser, url, username, password)

		# Clicking on setup & Tools and payments
		go_to_payment_setting(browser)

		#Clicking on a checkbox of securepay
		element = wait_until_element_present(browser, checkbox, "XPATH")
		element.click()

		#Clicking on Save
		browser.find_element_by_xpath(save).click()

		#Verifying and asserting the securepay success message
		verify_and_assert_success_message(browser, securepay_success_message, ".alert-success")

		#Clicking on securepay tab
		browser.find_element_by_link_text(securepay).click()

		#Entering Merchant id
		browser.find_element_by_id(merchantID).send_keys(merchantid)

		#Entering Merchant Password
		browser.find_element_by_id(merchantpwd).send_keys(password)

		#Selecting a value 'Yes' from dropdown box
		select_dropdown_value(browser, testmode, test_mode)

		#Clicking on save button
		browser.find_element_by_xpath(save).click()

		#Verifying and asserting the payment type save success message
		verify_and_assert_success_message(browser, payment_success_message, ".alert-success")

	#Handling exceptions

	#Handles when element is not present	
	except NoSuchElementException as errorMessage:
		print errorMessage.msg
	#Handles when time out error
	except TimeoutException as timeerror:
		print timeerror.msg
	#Handles when other exception errors
	except Exception as e:
		print e.msg
	 
	

#Test Data	
merchantid='ABC0001'
password = 'abc123'
test_mode = 'Yes'


#Xpath Data
checkbox='//label[@for = "ISSelectcheckoutproviders_checkout_securepay_input"]'
save='//input[@value = "Save"]'
securepay='SecurePay'
merchantID='checkout_securepay_merchantid'
merchantpwd='checkout_securepay_password'
testmode='checkout_securepay_testmode'
securepay_success_message='The modified payment settings have been saved successfully. If you enabled a new payment provider you can configure it by clicking its tab below.'
payment_success_message='The modified payment settings have been saved successfully.'