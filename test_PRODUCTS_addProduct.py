from lib.ui_lib import *

#Desciption: Check "Add a product" in the control panel
#            Veirfy successfull checking out as a guest for the created product from storefront  


def test_PRODUCTS_addProduct(browser, url, username, password):
	""""Check "Add a product" in the control panel
		Veirfy successfull checking out as a guest for the created product from storefront  """
		
	#initialise browser and login with valid credentials
	go_to_admin(browser,url,username,password)

	try:
		# Select "Add a Product" link from "Products" menu
		browser.find_element_by_link_text('Products').click()
		browser.find_element_by_link_text('Add a Product').click()

	except NoSuchElementException:
		browser.save_screenshot('Nosuchelement.png')
		raise	

	#Provide Details of the product
	element = wait_until_element_present(browser, 'product-name', 'ID')
	element.send_keys('Testing')

	try:
		browser.find_element_by_id('product-price').send_keys("10.45")
		browser.find_element_by_xpath('//li[@title = "'+category_name+'"]/a[text()="'+category_name+'"]').click()
		browser.find_element_by_id('product-weight').send_keys("1")
		browser.find_element_by_id('product-sku').send_keys(SKU)
	except NoSuchElementException:
		browser.save_screenshot('Nosuchelement.png')
		raise 	

	try:
		browser.execute_script("tinyMCE.activeEditor.dom.remove(tinyMCE.activeEditor.dom.select('p'));")
		browser.execute_script("tinymce.activeEditor.execCommand('mceInsertContent', true, \"TEST AUTOMATION BANNER\");")
	except WebDriverException:
		browser.find_element_by_id('wysiwyg').clear()
		browser.find_element_by_id('wysiwyg').send_keys('TEST AUTOMATION BANNER')

	try:	
		browser.find_element_by_id('product-width').send_keys("1")
		browser.find_element_by_id('product-height').send_keys("1")
		browser.find_element_by_id('product-depth').send_keys("1")
	except NoSuchElementException:
		browser.save_screenshot('Nosuchelement.png')
		raise 
		
	Upload "Image and Video" of the product
	try:
		browser.find_element_by_link_text('Images & Videos').click()
		file = browser.find_element_by_xpath('//input[@class = "file-upload"]')
		file.send_keys(product_img_path)
		time.sleep(15)
		browser.find_element_by_id('product-videos-search-query').send_keys(product_video_url)

	except NoSuchElementException:
		browser.save_screenshot('Nosuchelement.png')
		raise	

	element=wait_until_element_present(browser,'product-videos-search','ID')
	element.click()

	try:
		time.sleep(15)	
		browser.find_element_by_xpath('//label[@for = "'+product_video_label+'"]').click()

		#Provide "Inventory" detials of the product
		browser.find_element_by_link_text('Inventory').click()
		browser.find_element_by_xpath('//label[@for = "product-inventory-tracking-1"]').click()
		clear_field(browser,'inventory-level')
		browser.find_element_by_id('inventory-level').send_keys("123")
		clear_field(browser,'inventory-warning-level')
		browser.find_element_by_id('inventory-warning-level').send_keys("123")

	except NoSuchElementException:
		browser.save_screenshot('Nosuchelement.png')
		raise	

		
	try:	
		#Select Product Delivery details
		browser.find_element_by_link_text('Delivery/Event Date').click()
		browser.find_element_by_xpath('//label[@for = "product-event-date-required"]').click()
		browser.find_element_by_link_text('Details').click()
		browser.find_element_by_name('btn-save').click()

	except NoSuchElementException:
		browser.save_screenshot('Nosuchelement.png')
		raise

	verify_and_assert_success_message(browser, "The new product has been added successfully.", ".alert-success")

	# View newly created Product in control panel
	browser.find_element_by_link_text('Products').click()
	browser.find_element_by_link_text('View Products').click()
	element = wait_until_element_present(browser,'search-query','ID')
	element.send_keys(SKU)
	browser.find_element_by_xpath('//button[@class = "btn btn-secondary filter-button"]').click()
	time.sleep(15)
	browser.find_element_by_xpath("//tr[contains(.,'" + SKU + "')]").find_element_by_css_selector('.dropdown-trigger').click()
	browser.find_element_by_link_text('View').click()
 
    #Switching to cart window 
	for handle in browser.window_handles:
				browser.switch_to_window(handle)

	#Provide required delivery date
	try:
		wait_until_element_present(browser,'EventDateMonth','ID')
		select_dropdown_value(browser, 'EventDateMonth', 'Jan')
		select_dropdown_value(browser, 'EventDateDay', '1')
		select_dropdown_value(browser, 'EventDateYear', '2013')

	except NoSuchElementException:
		browser.save_screenshot('Nosuchelement.png')
		raise
			
	element = wait_until_element_present(browser, '//input[contains(@src,"AddCartButton.gif")]', 'XPATH')
	element.click()

	#Proceeding to checkout as guest
	time.sleep(15)
	wait_until_element_present(browser, '//a[@title = "Click here to proceed to checkout"]', 'XPATH').click()
	element = wait_until_element_present(browser, 'checkout_type_guest', 'ID')
	element.click()
	element = wait_until_element_present(browser, 'CreateAccountButton', 'ID')
	element.click()
	wait_until_element_present(browser, 'FormField_1', 'ID')

	#Provide Billing Details and proceed further
	try:
		browser.find_element_by_id('FormField_1').clear()
		browser.find_element_by_id('FormField_1').send_keys('Virendra.brahnbhatt+test001@bigcommerce.com')
		browser.find_element_by_id('FormField_4').clear()
		browser.find_element_by_id('FormField_4').send_keys('Virendra')
		browser.find_element_by_id('FormField_5').clear()
		browser.find_element_by_id('FormField_5').send_keys('Brahmbhatt')
		browser.find_element_by_id('FormField_7').clear()
		browser.find_element_by_id('FormField_7').send_keys('234234423234')
		browser.find_element_by_id('FormField_8').clear()
		browser.find_element_by_id('FormField_8').send_keys('George Street')
		browser.find_element_by_id('FormField_10').clear()
		browser.find_element_by_id('FormField_10').send_keys('Sydney')
		select_dropdown_value(browser, 'FormField_11', 'Australia')
		select_dropdown_value(browser, 'FormField_12', 'New South Wales')
		browser.find_element_by_id('FormField_13').clear()
		browser.find_element_by_id('FormField_13').send_keys('2000')
		browser.find_element_by_css_selector('.Submit .billingButton').click()

	except NoSuchElementException:
		browser.save_screenshot('Nosuchelement.png')
		raise		


	# Select shipping method
	element = wait_until_element_present(browser, "//input[contains(@id, 'shippingCheck')]", 'XPATH')
	element.click()
	browser.find_element_by_xpath("//div[@class='ML20']/input[@type='submit' and contains(@value,'Continue')]").click()

	# Proceed to payment
	try:
		wait_until_element_present(browser, 'bottom_payment_button', 'ID')
		browser.find_element_by_id('bottom_payment_button').click()

	except NoSuchElementException:
		browser.save_screenshot('Nosuchelement.png')
		raise	

	#Provide Credit Card Details
	try:
		wait_until_element_present(browser,'creditcard_cctype','ID')
		select_dropdown_value(browser, 'creditcard_cctype', 'Visa')
		browser.find_element_by_id('creditcard_name').send_keys('test')
		browser.find_element_by_id('creditcard_ccno').send_keys('4242424242424242')
		select_dropdown_value(browser, 'creditcard_ccexpm', 'Jan')
		select_dropdown_value(browser, 'creditcard_ccexpy', '2014')
		browser.find_element_by_id('creditcard_cccvd').send_keys('234')
		browser.find_element_by_xpath('//input[@value = "Pay for Order"]')
		
	except NoSuchElementException:
		browser.save_screenshot('Nosuchelement.png')
		raise	

    # Assert the succes message of Order Creation
	order_success_msg = 'YOUR ORDER NUMBER IS'
	browser_success_msg = browser.find_element_by_xpath('//div[@class = "alert alert-success"]/p').text

	if order_success_msg in browser_success_msg:
		print "I found my text"
		assert True
	else:
		print "No text"
		assert False



#Test Data    
category_name="Fruits"
SKU = "T001"
product_img_path="/home/sravan/Desktop/download.jpg"
product_video_url="http://www.youtube.com/watch?v=RY09M9wg1is"
product_video_label="video-9yHl24QynOM"





