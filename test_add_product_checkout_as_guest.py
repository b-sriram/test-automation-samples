from lib.ui_lib import *
category_name="Fruits"
SKU = "T001"
product_img_path="/home/sravan/Desktop/download.jpg"
product_video_url="http://www.youtube.com/watch?v=RY09M9wg1is"
product_video_label="video-9yHl24QynOM"


def test_add_product_checkout_as_guest(browser, url, username, password):
	go_to_admin(browser,url,username,password)

	#Adding a product in admin panel
	browser.find_element_by_link_text('Products').click()
	browser.find_element_by_link_text('Add a Product').click()
	#Entering Details of the product
	element = wait_until_element_present(browser, 'product-name', 'ID')
	element.send_keys('Testing')
	browser.find_element_by_id('product-price').send_keys("10.45")
	browser.find_element_by_xpath('//li[@title = "'+category_name+'"]/a[text()="'+category_name+'"]').click()
	browser.find_element_by_id('product-weight').send_keys("1")
	browser.find_element_by_id('product-sku').send_keys(SKU)
	try:
		browser.execute_script("tinyMCE.activeEditor.dom.remove(tinyMCE.activeEditor.dom.select('p'));")
		browser.execute_script("tinymce.activeEditor.execCommand('mceInsertContent', true, \"Test Product\");")
	except WebDriverException:
	    browser.find_element_by_id('wysiwyg').clear()
	    browser.find_element_by_id('wysiwyg').send_keys('Test Product')
	browser.find_element_by_id('product-width').send_keys("1")
	browser.find_element_by_id('product-height').send_keys("1")
	browser.find_element_by_id('product-depth').send_keys("1")
	#Adding Image and Video to the product
	browser.find_element_by_link_text('Images & Videos').click()
	file = browser.find_element_by_xpath('//input[@class = "file-upload"]')
	file.send_keys(product_img_path)
	time.sleep(10)
	browser.find_element_by_id('product-videos-search-query').send_keys(product_video_url)
	element=wait_until_element_present(browser,'product-videos-search','ID')
	element.click()
	browser.find_element_by_xpath('//label[@for = "'+product_video_label+'"]').click()
	#Adding product Inventary details
	browser.find_element_by_link_text('Inventory').click()
	browser.find_element_by_xpath('//label[@for = "product-inventory-tracking-1"]').click()
	clear_field(browser,'inventory-level')
	browser.find_element_by_id('inventory-level').send_keys("123")
	clear_field(browser,'inventory-warning-level')
	browser.find_element_by_id('inventory-warning-level').send_keys("123")
	#Adding Product Delivery details and Saving the product
	browser.find_element_by_link_text('Delivery/Event Date').click()
	browser.find_element_by_xpath('//label[@for = "product-event-date-required"]').click()
	browser.find_element_by_link_text('Details').click()
	browser.find_element_by_name('btn-save').click()
	verify_and_assert_success_message(browser, "The new product has been added successfully.", ".alert-success")
	#Viewing the Product from control panel
	browser.find_element_by_link_text('Products').click()
	browser.find_element_by_link_text('View Products').click()
	element = wait_until_element_present(browser,'search-query','ID')
	element.send_keys(SKU)
	browser.find_element_by_xpath('//button[@class = "btn btn-secondary filter-button"]').click()
	time.sleep(5)
	browser.find_element_by_xpath('//button[@type = "button"]/span[text()="Options"]').click()
	browser.find_element_by_link_text('View').click()
 
    #Switching to cart window 
	for handle in browser.window_handles:
				browser.switch_to_window(handle)
	#Adding product to the cart
	wait_until_element_present(browser,'EventDateMonth','ID')
	select_dropdown_value(browser, 'EventDateMonth', 'Jan')
	select_dropdown_value(browser, 'EventDateDay', '1')
	select_dropdown_value(browser, 'EventDateYear', '2013')
	element = wait_until_element_present(browser, '//input[contains(@src,"AddCartButton.gif")]', 'XPATH')
	element.click()
	#Proceeding to checkout
	wait_until_element_present(browser, '//a[@title = "Click here to proceed to checkout"]', 'XPATH').click()
	#Checkout as guest
	element = wait_until_element_present(browser, 'checkout_type_guest', 'ID')
	element.click()
	element = wait_until_element_present(browser, 'CreateAccountButton', 'ID')
	element.click()

	# Addresses
	wait_until_element_present(browser, 'FormField_1', 'ID')
	## Email address
	browser.find_element_by_id('FormField_1').clear()
	browser.find_element_by_id('FormField_1').send_keys('Virendra.brahnbhatt+test001@bigcommerce.com')
	## First name
	browser.find_element_by_id('FormField_4').clear()
	browser.find_element_by_id('FormField_4').send_keys('Virendra')
	## Last name
	browser.find_element_by_id('FormField_5').clear()
	browser.find_element_by_id('FormField_5').send_keys('Brahmbhatt')
	## Phone number
	browser.find_element_by_id('FormField_7').clear()
	browser.find_element_by_id('FormField_7').send_keys('234234423234')
	## Address
	browser.find_element_by_id('FormField_8').clear()
	browser.find_element_by_id('FormField_8').send_keys('George Street')
	## Suburb
	browser.find_element_by_id('FormField_10').clear()
	browser.find_element_by_id('FormField_10').send_keys('Sydney')
	## Country
	select_dropdown_value(browser, 'FormField_11', 'Australia')
	## State/Province
	select_dropdown_value(browser, 'FormField_12', 'New South Wales')
	## Postcode
	browser.find_element_by_id('FormField_13').clear()
	browser.find_element_by_id('FormField_13').send_keys('2000')
	## Submit
	browser.find_element_by_css_selector('.Submit .billingButton').click()


	# Select shipping method
	element = wait_until_element_present(browser, "//input[contains(@id, 'shippingCheck')]", 'XPATH')
	element.click()
	browser.find_element_by_xpath("//div[@class='ML20']/input[@type='submit' and contains(@value,'Continue')]").click()

	# Proceed to payment
	wait_until_element_present(browser, 'bottom_payment_button', 'ID')
	browser.find_element_by_id('bottom_payment_button').click()

	#Credit Card Details
	wait_until_element_present(browser,'creditcard_cctype','ID')
	select_dropdown_value(browser, 'creditcard_cctype', 'Visa')
	browser.find_element_by_id('creditcard_name').send_keys('test')
	browser.find_element_by_id('creditcard_ccno').send_keys('4242424242424242')
	select_dropdown_value(browser, 'creditcard_ccexpm', 'Jan')
	select_dropdown_value(browser, 'creditcard_ccexpy', '2014')
	browser.find_element_by_id('creditcard_cccvd').send_keys('234')
	browser.find_element_by_xpath('//input[@value = "Pay for Order"]')

     #Asserting the succes message
	order_success_msg = 'YOUR ORDER NUMBER IS'
	browser_success_msg = browser.find_element_by_xpath('//div[@class = "alert alert-success"]/p').text
	if order_success_msg in browser_success_msg:
		print "I found my text"
		assert True
	else:
		print "No text"
		assert False
    #verify_and_assert_success_message(browser, "Order has been created successfully.", ".alert-success")
	#time.sleep(10)
 




