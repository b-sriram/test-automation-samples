from lib.ui_lib import *


#Setup Payment Provider(Secure Pay)
def test_create_payment_method(browser, url, username, password):
	go_to_admin(browser, url, username, password)
	go_to_payment_setting(browser)
	element = wait_until_element_present(browser, '//label[@for = "ISSelectcheckoutproviders_checkout_securepay_input"]', "XPATH")
	element.click()
	browser.find_element_by_xpath('//input[@value = "Save"]').click()
	verify_and_assert_success_message(browser, "The modified payment settings have been saved successfully. If you enabled a new payment provider you can configure it by clicking its tab below.", ".alert-success")
	browser.find_element_by_link_text('SecurePay').click()
	browser.find_element_by_id('checkout_securepay_merchantid').send_keys(merchantid)
	browser.find_element_by_id('checkout_securepay_password').send_keys(password)
	select_dropdown_value(browser, 'checkout_securepay_testmode', 'Yes')
	browser.find_element_by_xpath('//input[@value = "Save"]').click()
	verify_and_assert_success_message(browser, "The modified payment settings have been saved successfully.", ".alert-success")
	
merchantid='ABC0001'
password = 'abc123'
