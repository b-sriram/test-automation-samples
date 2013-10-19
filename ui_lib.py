from includes import *

# Login to Admin
def go_to_admin(browser, url, username, password):
	admin = urlparse.urljoin(url, 'admin')
	browser.get(admin)
	try:
		browser.find_element_by_id('username').send_keys(username)
		browser.find_element_by_id('password').send_keys(password)
		browser.find_element_by_xpath('//button').click()
	except NoSuchElementException:
		admin = urlparse.urljoin(url, 'admin')
		browser.get(admin)
	except ElementNotVisibleException:
		pass
	except WebDriverException:
		pass			

	# Slick window comes up only the first time the store is created
	# the following code handles either the first time or the subsequent visits
	# to the store without failing.
	try:
		browser.find_element_by_class_name('slick-close').click()
	except NoSuchElementException:
		pass

	# Once Slick window closed, small popup comes as "Okay, I have got it"
	# Following code handles either the first time or the subsequent to make it pass.	
	try:
		browser.find_element_by_xpath('//button[contains(text(),"Okay")]').click()
	except ElementNotVisibleException:
		pass
	except NoSuchElementException:
		pass

def generate_random_string(size = 10, chars = string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))


def wait_until_element_present(browser, element, searchby, time = 30, first = True):
	try:
		if searchby == "ID":
			WebDriverWait(browser, time).until(lambda s: s.find_element_by_id(element).is_displayed() and s.find_element_by_id(element))
			return browser.find_element_by_id(element)
		elif searchby == "XPATH":
			WebDriverWait(browser, time).until(lambda s: s.find_element_by_xpath(element).is_displayed() and s.find_element_by_xpath(element))
			return browser.find_element_by_xpath(element)
		elif searchby == "NAME":
			WebDriverWait(browser, time).until(lambda s: s.find_element_by_name(element).is_displayed() and s.find_element_by_name(element))
			return browser.find_element_by_name(element)
		elif searchby == "LINK":
			WebDriverWait(browser, time).until(lambda s: s.find_element_by_link_text(element).is_displayed() and s.find_element_by_link_text(element))
			return browser.find_element_by_link_text(element)
		elif searchby == "CSS_SELECTOR":
			WebDriverWait(browser, time).until(lambda s: s.find_element_by_css_selector(element).is_displayed() and s.find_element_by_css_selector(element))
			return browser.find_element_by_css_selector(element)
		elif searchby == "CLASS_NAME":
			WebDriverWait(browser, time).until(lambda s: s.find_element_by_class_name(element).is_displayed() and s.find_element_by_class_name(element))
			return browser.find_element_by_class_name(element)
		elif searchby == "TAGNAME":
			WebDriverWait(browser, time).until(lambda s: s.find_element_by_tag_name(element).is_displayed() and s.find_element_by_tag_name(element))
			return browser.find_element_by_tag_name(element)
		elif searchby == "JQUERY":
			WebDriverWait(browser, time).until(lambda s: s.execute_script(element))
	except TimeoutException:
		browser.save_screenshot('timeout.png')
		raise
	except StaleElementReferenceException:
		if first:
			return wait_until_element_present(browser, element, searchby, time, False)
		else:
			browser.save_screenshot('stale_element.png')
			raise

def select_dropdown_value(browser, dropdown_id, option_text):
    WebDriverWait(browser, 30).until(lambda s: s.find_element_by_id(dropdown_id).is_displayed() and s.find_element_by_id(dropdown_id))
    dropdown_list = browser.find_element_by_id(dropdown_id)
    for option in dropdown_list.find_elements_by_tag_name('option'):
        if option.text == option_text:
            option.click()

def get_dropdown_selected_value(browser, element_id):
    return browser.execute_script("return $('#" + element_id + " option:selected').text()")

def clear_field(browser,element_id):
    WebDriverWait(browser, 30).until(lambda s: s.find_element_by_id(element_id).is_displayed() and s.find_element_by_id(element_id))
    browser.find_element_by_id(element_id).clear()
    
def verify_and_assert_success_message(browser, success_message, classname):
# StaleElementReferenceException: Message: u'Element is no longer attached to the DOM' ; Stacktrace: Method fxdriver.cache.getElementAt threw an error in resource://fxdriver/modules/web_element_cache.js
    try:
		WebDriverWait(browser, 40).until(lambda s: success_message in s.find_element_by_css_selector(classname).text)
		assert success_message in browser.find_element_by_css_selector(classname).text 
    except StaleElementReferenceException:
		WebDriverWait(browser, 40).until(lambda s: success_message in s.find_element_by_css_selector(classname).text)
		assert success_message in browser.find_element_by_css_selector(classname).text 



# ********************************************************* 
# Following Methods are used by Shipping Quotes 
# ********************************************************* 
def setup_store_location(browser, country, state, postcode):
	browser.find_element_by_link_text("Setup & Tools").click()
	browser.find_element_by_link_text('Shipping').click()
	if country not in get_dropdown_selected_value(browser, 'companycountry'):
		clear_field(browser, 'companyname')
		browser.find_element_by_id('companyname').send_keys('Automation Testing')
		clear_field(browser, 'companyaddress')
		browser.find_element_by_id('companyaddress').send_keys('George Street')
		clear_field(browser, 'companycity')
		browser.find_element_by_id('companycity').send_keys('Sydney')
		select_dropdown_value(browser, 'companycountry', country)
		time.sleep(1)
		select_dropdown_value(browser, 'companystate', state)
		clear_field(browser, 'companyzip')
		browser.find_element_by_id('companyzip').send_keys(postcode)
		try:
			browser.find_element_by_css_selector('.SaveButton').click()
		except WebDriverException as e:
			browser.find_element_by_xpath('//input[@value="Save"]').click()
			if "Click succeeded but Load Failed" in e.msg:
				pass
				
		verify_and_assert_success_message(browser, "The modified shipping settings have been saved successfully.", ".alert-success")


def get_quote_in_control_panel(browser, provider, country, state, postcode, expected_service, expected_value):
	browser.execute_script("$('tr tr:contains(" + provider + ") td .dropdown-trigger').last().click()")
	browser.find_element_by_link_text('Get Quote').click()
	time.sleep(1)
	if country not in get_dropdown_selected_value(browser, 'country'):
		select_dropdown_value(browser, 'country', country)
		time.sleep(1)

	if state not in get_dropdown_selected_value(browser, 'state'):
		select_dropdown_value(browser, 'state', state)
	
	browser.find_element_by_id('postcode').send_keys(postcode)
	browser.find_element_by_id('weight').send_keys('1')
	browser.find_element_by_id('width').send_keys('1')
	browser.find_element_by_id('length').send_keys('1')
	browser.find_element_by_id('height').send_keys('1')
	browser.find_element_by_id('GetQuote').click()

	# FedEx service goes down, in that case, we dont want our test to be failed.  
	if provider == "FedEx":
		try:
			verify_and_assert_success_message(browser, expected_service, ".ShippingQuote")
			browser.find_element_by_css_selector('.modalClose').click()
		except TimeoutException:
			verify_and_assert_success_message(browser, "not connect to", ".ShippingQuote")
			browser.find_element_by_css_selector('.modalClose').click()
	else:
		verify_and_assert_success_message(browser, expected_service, ".ShippingQuote")
		verify_and_assert_success_message(browser, expected_value, ".ShippingQuote")
		browser.find_element_by_css_selector('.modalClose').click()


def add_new_shipping_methods(browser):
	browser.find_element_by_id('tab1').click()
	browser.execute_script("$('tr:contains(\"International\") td .dropdown-trigger').last().click()")
	WebDriverWait(browser, 30).until(lambda s: s.find_element_by_link_text('Edit Methods').is_displayed() and s.find_element_by_link_text('Edit Methods'))
	browser.find_element_by_link_text('Edit Methods').click()
	disable_the_shipping_method(browser)
	WebDriverWait(browser, 30).until(lambda s: s.find_element_by_xpath('//input[@value="Add a Shipping Method..."]').is_displayed() and s.find_element_by_xpath('//input[@value="Add a Shipping Method..."]'))
	browser.find_element_by_xpath('//input[@value="Add a Shipping Method..."]').click()


def change_default_currency(browser, url, country, currencycode):
	browser.find_element_by_link_text('Home').click()
	browser.get(browser.current_url + '/index.php?ToDo=settingsEditCurrency&currencyId=1')
	if country not in get_dropdown_selected_value(browser, 'currencyorigin'):
		browser.find_element_by_id('currencyname').clear()
		browser.find_element_by_id('currencyname').send_keys(currencycode + '_Dollar')
		select_dropdown_value(browser, 'currencyorigin', country)
		browser.find_element_by_id('currencycode').clear()
		browser.find_element_by_id('currencycode').send_keys(currencycode)
		browser.find_element_by_xpath('//input[@value="Save"]').click()
		verify_and_assert_success_message(browser, "The selected currency has been updated successfully.", ".alert-success")

def select_dropdown_value_by_css(browser, dropdown_class, option_text):
    WebDriverWait(browser, 30).until(lambda s: s.find_element_by_css_selector(dropdown_class).is_displayed() and s.find_element_by_css_selector(dropdown_class))
    dropdown_list = browser.find_element_by_css_selector(dropdown_class)
    for option in dropdown_list.find_elements_by_tag_name('option'):
        if option.text == option_text:
            option.click()

def get_quote_in_store_front(browser, url, country, state, postcode):
	browser.get(url)
	browser.find_element_by_link_text('HOME').click()
	browser.get(browser.current_url + 'donatello-brown-leather-handbag-with-shoulder-strap')
	browser.find_element_by_xpath('//input[contains(@src,"AddCartButton.gif")]').click()
	WebDriverWait(browser, 30).until(lambda s: s.find_element_by_link_text('View or edit your cart').is_displayed() and s.find_element_by_link_text('View or edit your cart'))
	browser.find_element_by_link_text('View or edit your cart').click()
	WebDriverWait(browser, 30).until(lambda s: s.find_element_by_css_selector('.EstimateShippingLink').is_displayed() and s.find_element_by_css_selector('.EstimateShippingLink'))
	# "The contents of your shopping cart have been updated." message displayed when quantity set to 1, but 
	# Getting exception "Element not found in the cache - perhaps the page has changed since it was looked up"
	try:
		select_dropdown_value_by_css(browser,'.quantityInput', '1' )
	except StaleElementReferenceException:
		pass
	browser.refresh()
	browser.find_element_by_css_selector('.EstimateShippingLink').click()
	select_dropdown_value(browser, 'shippingZoneCountry', country)
	time.sleep(1)
	select_dropdown_value(browser, 'shippingZoneState', state)
	browser.find_element_by_id('shippingZoneZip').clear()
	browser.find_element_by_id('shippingZoneZip').send_keys(postcode)
	browser.find_element_by_xpath('//input[@value="Estimate Shipping & Tax"]').click()

def disable_the_shipping_method(browser):
	try:
		enabled_methods = browser.find_elements_by_xpath("//img[contains(@src,\"tick.gif\")]")
		count = 0
		for tick in enabled_methods:
			count = count + 1

		while count >= 0:
			browser.find_element_by_xpath("//img[contains(@src,\"tick.gif\")]").click()
			count = count - 1
	except Exception:
		pass


def search_and_edit(browser, element_by_xpath, search_keyword):
	element = wait_until_element_present(browser, element_by_xpath, "XPATH")
	element.clear()
	element.send_keys(search_keyword)
	browser.find_element_by_css_selector('.action-divider .filter-button').click()
	element_row = "return $('tr:contains(" + search_keyword + ")  button.dropdown-trigger')"
	wait_until_element_present(browser, element_row, "JQUERY")
	browser.find_element_by_xpath("//tr[contains(., '" + search_keyword + "')]").find_element_by_css_selector('.dropdown-trigger').click()
	try:
		element = wait_until_element_present(browser, "Edit", "LINK")
		element.click()	
	except TimeoutException:
		browser.find_element_by_link_text(search_keyword).click()
	except NoSuchElementException:
		browser.find_element_by_link_text(search_keyword).click()

def edit_without_search(browser, keyword_to_click):
	element_row = "return $('tr:contains(" + keyword_to_click + ")  button.dropdown-trigger')"
	wait_until_element_present(browser, element_row, "JQUERY")
	browser.find_element_by_xpath("//tr[contains(.,'" + keyword_to_click + "')]").find_element_by_css_selector('.dropdown-trigger').click()
	try:
		element = wait_until_element_present(browser,"Edit","LINK")
		element.click()	
	except TimeoutException:
		browser.find_element_by_link_text(keyword_to_click).click()
	except NoSuchElementException:
		browser.find_element_by_link_text(keyword_to_click).click()

# CRUD Coupons
def create_coupon_codes(browser, couponcode, couponname, coupontype, couponamount, min_purchase):
    browser.find_element_by_id('couponcode').clear()
    browser.find_element_by_id('couponcode').send_keys(couponcode)
    browser.find_element_by_id('couponname').clear()
    browser.find_element_by_id('couponname').send_keys(couponname)
    browser.execute_script("$('#" + coupontype + "').prop(\"checked\",true)")
    if browser.find_element_by_id('couponamount').is_displayed() == True:
        browser.find_element_by_id('couponamount').clear()
        browser.find_element_by_id('couponamount').send_keys(couponamount)
    browser.find_element_by_id('couponminpurchase').clear()
    browser.find_element_by_id('couponminpurchase').send_keys(min_purchase)
    browser.find_element_by_name('SaveButton1').click()

def update_coupon_codes(browser, couponname, updatecouponname, min_purchase):
    edit_without_search(browser, couponname)     
    browser.find_element_by_id('couponname').clear()
    browser.find_element_by_id('couponname').send_keys(updatecouponname)
    browser.find_element_by_id('couponminpurchase').clear()
    browser.find_element_by_id('couponminpurchase').send_keys(min_purchase)
    browser.find_element_by_name('SaveButton1').click()

def delete_coupon_codes(browser, couponname):
    browser.execute_script("$('tr:contains(" + couponname + ") td:nth-child(1) [type=\"checkbox\"]').prop(\"checked\",true)")
    browser.find_element_by_id('IndexDeleteButton').click()
    browser.execute_script("$('.btn-primary').last().click()")	



# Checkout / Payments methods
def go_to_payment_setting(browser):
	browser.find_element_by_link_text('Setup & Tools').click()
	browser.find_element_by_link_text('Payments').click()
	element = wait_until_element_present(browser,'summary',"TAGNAME")
	element.click()
	
def se_feature_flag(browser, url, which_feature, flag):
    browser.get(urlparse.urljoin(url, 'admin'))
    browser.get(urlparse.urljoin(browser.current_url, 'index.php?ToDo=' + flag.lower() + '&feature=' + which_feature))
    assert flag in browser.page_source
    admin = urlparse.urljoin(url, 'admin')
    browser.get(admin)

def get_dropdown_values(browser, dropdown_id):
    WebDriverWait(browser, 30).until(lambda s: s.find_element_by_id(dropdown_id).is_displayed() and s.find_element_by_id(dropdown_id))
    dropdown_list = browser.find_element_by_id(dropdown_id)
    option_text = ""
    for option in dropdown_list.find_elements_by_tag_name('option'):
        option_text =  option_text + option.text + ' '
    
    return option_text    	

def set_global_payments(browser, transaction_type = 'Sale'):
	wait_until_element_present(browser,'//label[@for = "ISSelectcheckoutproviders_checkout_globalpayments_input"]',"XPATH")
	browser.find_element_by_xpath('//label[@for = "ISSelectcheckoutproviders_checkout_globalpayments_input"]').click()
	browser.find_element_by_css_selector('.SaveButton').click()
	verify_and_assert_success_message(browser, "The modified payment settings have been saved successfully. If you enabled a new payment provider you can configure it by clicking its tab below.", ".alert-success")
	browser.find_element_by_link_text('Global Payments').click()
	browser.find_element_by_id('checkout_globalpayments_username').send_keys('bigc7659')
	browser.find_element_by_id('checkout_globalpayments_password').send_keys('Beyond40k')
	select_dropdown_value(browser, 'checkout_globalpayments_transaction_type', transaction_type)
	browser.find_element_by_css_selector('.SaveButton').click()
	verify_and_assert_success_message(browser, "The modified payment settings have been saved successfully.", ".alert-success")  


def set_simplify_payments(browser):
	wait_until_element_present(browser,'//label[@for = "ISSelectcheckoutproviders_checkout_simplify_input"]',"XPATH")
	browser.find_element_by_xpath('//label[@for = "ISSelectcheckoutproviders_checkout_simplify_input"]').click()
	browser.find_element_by_css_selector('.SaveButton').click()
	verify_and_assert_success_message(browser, "The modified payment settings have been saved successfully. If you enabled a new payment provider you can configure it by clicking its tab below.", ".alert-success")
	browser.find_element_by_link_text('Simplify').click()
	browser.find_element_by_id('checkout_simplify_public_key').send_keys('sbpb_OGE0MDEyNGMtNjNmYi00NWNmLTgwOTktNzcwZGVlZDY2OGUy')
	browser.find_element_by_id('checkout_simplify_private_key').send_keys('2BmEK8rhZBDanj9F+8aF7QBA/clMR4hI34esM6JYjjp5YFFQL0ODSXAOkNtXTToq')
	browser.find_element_by_css_selector('.SaveButton').click()
	verify_and_assert_success_message(browser, "The modified payment settings have been saved successfully.", ".alert-success")  

def element_not_exists(browser, element, searchby):
    try:
        if searchby == "ID":
            browser.find_element_by_id(element)
        elif searchby == "XPATH":
            browser.find_element_by_xpath(element)
        elif searchby == "NAME":
            browser.find_element_by_name(element)
        elif searchby == "LINK":
            browser.find_element_by_link_text(element)
        elif searchby == "CSS_SELECTOR":
            browser.find_element_by_css_selector(element)
        elif searchby == "CLASS_NAME":
            browser.find_element_by_css_selector(element)
        elif searchby == "TAGNAME":
            browser.find_element_by_tag_name(element)
        elif searchby == "JQUERY":
            browser.execute_script(element)
        return False
    except NoSuchElementException:
        return True
    except Exception:
        return False	

def add_product_and_checkout_as_guest(browser, url):
	# Navigate to Storefront & Add a Product to Cart
	browser.get(urlparse.urljoin(url, 'donatello-brown-leather-handbag-with-shoulder-strap'))
	browser.find_element_by_xpath('//input[contains(@src,"AddCartButton.gif")]').click()
	wait_until_element_present(browser,'//a[contains(@href,"checkout.php")]',"XPATH")
	browser.find_element_by_xpath('//a[contains(@href,"checkout.php")]').click()

	element = wait_until_element_present(browser,'checkout_type_guest',"ID")
	element.click()
	# Checkout as Guest
	# browser.find_element_by_id('checkout_type_guest').click()
	browser.find_element_by_id('CreateAccountButton').click()
	EMAIL = "virendra.brahmbhatt+" + generate_random_string() + "@bigcommerce.com"
	FIRSTNAME = "Viru"
	LASTNAME = "Brahmbhatt"
	COMPANY = "Bigcommerce"
	PHONE = "0111111111"
	ADDRESS1 = "1A"
	ADDRESS2 = "George Street"
	CITY = "Sydney"
	COUNTRY = "Australia"
	STATE = "New South Wales"
	POSTCODE = "2000"

	element = wait_until_element_present(browser,'FormField_1',"ID")
	element.send_keys(EMAIL)
	browser.find_element_by_id('FormField_4').send_keys(FIRSTNAME)
	browser.find_element_by_id('FormField_5').send_keys(LASTNAME)
	browser.find_element_by_id('FormField_6').send_keys(COMPANY)
	browser.find_element_by_id('FormField_7').send_keys(PHONE)
	browser.find_element_by_id('FormField_8').send_keys(ADDRESS1)
	browser.find_element_by_id('FormField_9').send_keys(ADDRESS2)
	browser.find_element_by_id('FormField_10').send_keys(CITY)
	select_dropdown_value(browser, 'FormField_11', 'Australia')
	select_dropdown_value(browser, 'FormField_12', 'New South Wales')
	browser.find_element_by_id('FormField_13').send_keys(POSTCODE)
	browser.find_element_by_css_selector('.Submit .billingButton').click()
	element = wait_until_element_present(browser,'//label[contains(.,"Flat Rate Per Order")]',"XPATH")
	element.click()
	element = wait_until_element_present(browser,'.ML20 input',"CSS_SELECTOR")
	element.click()	
	element = wait_until_element_present(browser,'bottom_payment_button',"ID")
	element.click() 


def enter_credit_card(browser, card_type, cardholder_name, card_number, expiry_month, expiry_year, ccv):
	wait_until_element_present(browser,'creditcard_cctype',"ID")
	select_dropdown_value(browser, 'creditcard_cctype', card_type)
	browser.find_element_by_name('creditcard_name').send_keys(cardholder_name)
	browser.find_element_by_name('creditcard_ccno').send_keys(card_number)
	select_dropdown_value(browser, 'creditcard_ccexpm', expiry_month)
	select_dropdown_value(browser, 'creditcard_ccexpy', expiry_year)
	browser.find_element_by_name('creditcard_cccvd').send_keys(ccv)
	browser.find_element_by_xpath("//input[contains(@value,'Pay for Order')]").click()

def get_order_confirmation_number(browser):
	element = wait_until_element_present(browser, 'order-number', 'ID')
	Order_Id = element.text
	assert Order_Id != ''
	assert "your order number is: " + Order_Id in browser.find_element_by_css_selector('p.order-number').text.lower()	
	return Order_Id

def get_dropdown_values(browser, dropdown_id):
    WebDriverWait(browser, 30).until(lambda s: s.find_element_by_id(dropdown_id).is_displayed() and s.find_element_by_id(dropdown_id))
    dropdown_list = browser.find_element_by_id(dropdown_id)
    option_text = ""
    for option in dropdown_list.find_elements_by_tag_name('option'):
        option_text =  option_text + option.text + ' '
    
    return option_text
    	