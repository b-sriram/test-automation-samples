from lib.ui_lib import *
country = 'Australia'
state = 'New South Wales'
postcode = '2000'
zonename = 'Australia India'


def test_shipment_zone_method(browser, url, username, password):
	go_to_admin(browser, url, username, password)
	setup_store_location(browser, country, state, postcode)

	#Adding new shipping zone in admin panel
	browser.find_element_by_id('tab1').click()
	browser.find_element_by_xpath('//input[@value = "Add a Shipping Zone..."]').click()
	browser.find_element_by_xpath('//input[@id = "zonename"]').send_keys(zonename)
	browser.find_element_by_xpath('//label[@for = "zonetype_country"]').click()
	browser.find_element_by_xpath('//label[@for = "ISSelectzonetype_country_list_13_input"]').click()
	browser.find_element_by_xpath('//label[@for = "ISSelectzonetype_country_list_99_input"]').click()
	browser.find_element_by_name('SubmitButton1').click()
	verify_and_assert_success_message(browser, "The shipping zone has been created successfully.", ".alert-success")
	
	#Adding new shipping method
	browser.find_element_by_xpath('//input[@value="Add a Shipping Method..."]').click()
	browser.find_element_by_xpath('//span[text()="Australia Post"]').click()
	element = wait_until_element_present(browser, 'Select All', 'LINK')
	element.click()
	browser.find_element_by_name('SubmitButton1').click()
	verify_and_assert_success_message(browser, "The shipping method has been created successfully.", ".alert-success")



