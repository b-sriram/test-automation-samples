from lib.ui_lib import *

#*********************************************************************************
#Description: Checks the paymentmethod functionality in control panel  *
# Verify "Securepay" can be added as a payment provider from  control panel    *
#*********************************************************************************


def test_PAYMENTS_create_paymentmethod(browser, url, username, password):
	""" Checks the paymentmethod functionality in control panel """
	
	# Initialise browser and enter credentials
	go_to_admin(browser, url, username, password)

	# Select "setup & Tools" --> "Payments"
	go_to_payment_setting(browser)

	# Select Securepay in checkbox
	element = wait_until_element_present(browser, checkbox, "XPATH")
	element.click()

	try:	
		
		
		browser.find_element_by_xpath(save).click()

		#Verifying and asserting the securepay success message
		verify_and_assert_success_message(browser, securepay_success_message, ".alert-success")
		
		#Proceed to  securepay tab
		browser.find_element_by_link_text(securepay).click()

		# Provide and Save SecurePay settings
		browser.find_element_by_id(merchantID).send_keys(merchantid)
		browser.find_element_by_id(merchantpwd).send_keys(password)
		select_dropdown_value(browser, testmode, test_mode)
		browser.find_element_by_xpath(save).click()

		# Verify and assert the payment settings save success message
		verify_and_assert_success_message(browser, payment_success_message, ".alert-success")

	except NoSuchElementException:
		browser.save_screenshot('Nosuchelement.png')
		raise
	
	except TimeoutException:
		browser.save_screenshot('timeout.png')
		raise

	# Any other exception
	except Exception:
		browser.save_screenshot('exception.png')
		raise
	 
	

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
