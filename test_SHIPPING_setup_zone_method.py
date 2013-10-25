from lib.ui_lib import *

#Desription : Check setting up of shippment zone and shippmnet method to the store from control panel
#             Verify shippment zone and shippment method saving sucessfully


def test_SHIPPING_setup_zone_method(browser, url, username, password):
	""" Check setting up of shippment zone and shippmnet method to the store from control panel
	    Verify shippment zone and shippment method saving sucessfully """
	    
	#initialise browser and login with valid credentials
	go_to_admin(browser, url, username, password)

	#Enter store address details and saving it
	setup_store_location(browser, country, state, postcode)

	#Create new shipping zone for the store
	try:	
		
		browser.find_element_by_id('tab1').click()
		browser.find_element_by_xpath('//input[@value = "Add a Shipping Zone..."]').click()
		browser.find_element_by_xpath('//input[@id = "zonename"]').send_keys(zonename)
		browser.find_element_by_xpath('//label[@for = "zonetype_country"]').click()
		time.sleep(3)
		browser.find_element_by_xpath('//label[@for = "ISSelectzonetype_country_list_13_input"]').click()
		browser.find_element_by_xpath('//label[@for = "ISSelectzonetype_country_list_99_input"]').click()
		browser.find_element_by_name('SubmitButton1').click()

	except NoSuchElementException:
		browser.save_screenshot('Nosuchelement.png')
		raise

	
	except TimeoutException:
		browser.save_screenshot('timeout.png')
		raise

	# Other exceptions
	except Exception:
		browser.save_screenshot('other_exception.png')
	        raise

	# Verify successfull submission of shipping zone details
	verify_and_assert_success_message(browser, "The shipping zone has been created successfully.", ".alert-success")
	
	# Setup  new shipping method for created shipping zone 
	try:
		browser.find_element_by_xpath('//input[@value="Add a Shipping Method..."]').click()
		time.sleep(5)
		browser.find_element_by_xpath('//span[text()="Australia Post"]').click()
	
	except NoSuchElementException:
		browser.save_screenshot('Nosuchelement.png')
		raise

	#Select all Australia Post Settings	
	element = wait_until_element_present(browser,'Select All','LINK')
	element.click()

	try:
		#Save shipping method	
		browser.find_element_by_name('SubmitButton1').click()
		
	except NoSuchElementException:
		browser.save_screenshot('Nosuchelement.png')
		raise

	except Exception:
		browser.save_screenshot('other_exception.png')
		raise

	#verify successfull creation of shipping method	
	verify_and_assert_success_message(browser, "The shipping method has been created successfully.", ".alert-success")


#Test Data 
country = 'Australia'
state = 'New South Wales'
postcode = '2000'
zonename = 'Australia India'
