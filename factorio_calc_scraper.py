# Factorio Calc Scraper - Marshall Ferguson - 8/2020

# TODO: (DONE) Figure out template for url to get different results from calc

# base url =    https://kirkmcdonald.github.io/calc.html

# data set =    #data="inset data set"
# data set determines which version of Factorio the recipe is for
# data set should be kept up to date in case of recipe changes

# item =        &items="inset item name"
# item determines which item the recipe is for
# item names will name to exactly match a specific syntax

# factories =   :f:"inset number of factories"
# factories determines the number of factories (assembly machines) working on the recipe
# factories syntax defaults to assembly machine 1, another change to url is needed for assembly machines 2 and 3

# rate =        :r:"inset rate"
# rate determines the rate at which the recipe is worked on
# rate defaults to items/minute, another change to url is needed for items/seond and items/hour

# example url = https://kirkmcdonald.github.io/calc.html#data=1-0-0&items=electronic-circuit:f:1
# example url syntax = base url + data set + items + factories OR rate

# In the future, this script will be able to handle different levels of assembly machines and rates, but for now it will focus on the defaults

# Imports
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from urllib.request import urlopen
import mechanicalsoup
import time
import math

# Output a menu to guide user's input

print("Welcome to the Factorio Calc Scraper!")
time.sleep(1)
print("This script will scrape the site of the Factorio Calculator to calculate how many factories you need in total for a recipe.")
time.sleep(2)
print("All you have to do is answer the following prompts.")
time.sleep(2)
item_input = input("What item do you want to make? (If multiple words, must be in following syntax: word1-word2)    ") 
# item_input = "space-science-pack"
factories_or_rate = input("Would you like to go by number of factories or rate of item per minute? (factories or rate)     ")
# factories_or_rate = "factories"
# factories_input = "1"
# rate_input = "3000"
if factories_or_rate == "factories":
    factories_input = input("How many factories will be making the item?     ")
elif factories_or_rate == "rate":
    rate_input = input("At what rate do you want to make the item? (in items per minute)     ")
else:
    print("")

# TODO: (DONE) Request web page

example_url = "https://kirkmcdonald.github.io/calc.html#data=1-0-0&items=electronic-circuit:f:1"
# base_url = "https://kirkmcdonald.github.io/calc.html"
# data_set = "#data=1.0.0"
# # This will be a variable input from the prompt later on, but for now will be hard coded as this version
# item = "&items=" + item_input
# factories = ":f:" + factories_input
# rate = ":r:" + rate_input                                  

# browser = mechanicalsoup.StatefulBrowser()
# url = base_url + data_set + item + factories
url = example_url
# print(url)
# page = browser.get(url)
# print(page)
# print(page.soup)

# TODO: (DONE) Automate inputting info into calc site 

PATH = "C:\\Program Files (x86)\\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get(url)
driver.implicitly_wait(10)
actions = ActionChains(driver)

# Not sure why this code doesn't work while the dropdownWrapper selection and clicking does.....

# csv_link = driver.find_element_by_link_text("CSV")
# print(csv_link)
# print(type(csv_link))
# driver.implicitly_wait(5)
# actions.click(csv_link).perform()

# Find the desired HTML elements on the website with selenium

item_dropdown = driver.find_elements_by_class_name("dropdownWrapper")[0]
# print(item_dropdown)
# print(type(item_dropdown))
ActionChains(driver).click(item_dropdown).perform()
ActionChains(driver).reset_actions()

search_bar = driver.find_element_by_class_name("search")
# print(search_bar)
# print(type(search_bar))
ActionChains(driver).send_keys(item_input).perform()
ActionChains(driver).reset_actions()

item_link = driver.find_element_by_xpath('//img[@alt="' + item_input + '"]')
# print(item_link)
# print(type(item_link))
ActionChains(driver).click(item_link).perform()
ActionChains(driver).reset_actions()

factories_input_field = driver.find_element_by_xpath("/html/body/table/tbody/tr/td[@id='targetparent']/ul[@id='targets']/li[@class='target']/input[1]")
rate_input_field = driver.find_element_by_xpath("/html/body/table/tbody/tr/td[@id='targetparent']/ul[@id='targets']/li[@class='target']/input[2]")
# print(factories_input_field)
# print(type(factories_input_field))
# print(rate_input_field)
# print(type(rate_input_field))

# Input the user supplied input into a search bar

if factories_or_rate == "factories":
    actions.send_keys_to_element(factories_input_field, u'\ue005')
    actions.send_keys_to_element(factories_input_field, factories_input)
    actions.send_keys_to_element(factories_input_field, u'\ue007')
    actions.perform()
    actions.reset_actions()
elif factories_or_rate == "rate":
    actions.send_keys_to_element(rate_input_field, u'\ue005')
    actions.send_keys_to_element(rate_input_field, rate_input)
    actions.send_keys_to_element(rate_input_field, u'\ue007')
    actions.perform()
    actions.reset_actions()
else:
    print("")

# TODO: (DONE) Parse through HTML to get total number of assembly machinces needed
    # Figure out how to loop through all the XPaths and put the WebElements in a list
    # Figure out how to extract the text from the html of a list of WebElements 

# Create lists of WebElements

rates_elem_list = []
rates_elem_list.extend(driver.find_elements_by_xpath("//table[@id='totals']/tr/td[2]/tt"))
# print(all_rates_elem_list)
# print(len(all_rates_elem_list))
factory_elem_list = []
factory_elem_list.extend(driver.find_elements_by_xpath("//td[@class='factory right-align'][1]/tt"))
# print(factory_elem_list)
# print(len(factory_elem_list))
factory_img_elem_list = []
factory_img_elem_list.extend(driver.find_elements_by_xpath("//td[@class='pad factory right-align leftmost']/img[@class='icon display']"))
# print(factory_img_elem_list)
# print(len(factory_img_elem_list))
item_img_elem_list = []
item_img_elem_list.extend(driver.find_elements_by_xpath("//td[@class='right-align']/img"))
# print(item_img_elem_list)
# print(len(item_img_elem_list))

# Loop through lists of WebElements and create lists of innerHTML(str's)

rates_innerHTML_list = []
for i in rates_elem_list:
    rates_innerHTML_list.append(i.get_attribute("innerHTML"))
# print("rates_innerHTML_list is:")
# print(rates_innerHTML_list)
# print(len(rates_innerHTML_list))

factory_elem_str_list = []
for i in factory_elem_list:
    factory_elem_str_list.append(i.get_attribute("innerHTML"))
# print("factory_elem_str_list is:")
# print(factory_elem_str_list)
# print(len(factory_elem_str_list))

# Clean out empty str's from list

factory_elem_str_list = ' '.join(factory_elem_str_list).split()

# Loop through list of str's, remove encoding characters, and coerce to float

factory_elem_float_list = []
for i in factory_elem_str_list:
    i = i.rstrip("&nbsp;")
    factory_elem_float_list.append(float(i))
# print("factory_elem_float_list is:")
# print(factory_elem_float_list)
# print(len(factory_elem_float_list))

# Loop through list of floats and coerce to rounded up ints

factory_elem_int_list = []
for i in factory_elem_float_list:
    factory_elem_int_list.append(int(math.ceil(i)))
# print("factory_elem_int_list is:")
# print(factory_elem_int_list)
# print(len(factory_elem_int_list))

# Loop through list of str's, remove encoding characters, and coerce to float

rate_float_list = []
for i in rates_innerHTML_list:
    i = i.rstrip("&nbsp;")
    rate_float_list.append(float(i))
# print("rate_float_list is:")
# print(rate_float_list)
# print(len(rate_float_list))

# Loop through lists of WebElements and create lists of img alt text (str's)

factory_img_elem_alt_text_list = []
for i in factory_img_elem_list:
    factory_img_elem_alt_text_list.append(i.get_attribute("alt"))
# print("factory_img_elem_alt_text_list is:")
# print(factory_img_elem_alt_text_list)
# print(len(factory_img_elem_alt_text_list))

item_img_elem_alt_text_list = []
for i in item_img_elem_list:
    item_img_elem_alt_text_list.append(i.get_attribute("alt"))
# print("item_img_elem_alt_text_list is:")
# print(item_img_elem_alt_text_list)
# print(len(item_img_elem_alt_text_list))

# Create an empty dictionary and use it to add the keys to the actual dictionary

empty_dict = {}
item_dict = empty_dict.fromkeys(item_img_elem_alt_text_list)
# print(item_dict)

# Add values to dictionary from various lists

for a, b, c, d in zip(item_img_elem_alt_text_list, factory_img_elem_alt_text_list, factory_elem_float_list, rate_float_list):
    item_dict[a] = [b, c, d]
# print(item_dict)

# Loop through dictionary and print desired output to user
    # TEMPLATE: "You will need {number_of_factories} {name_of_factories}'s making {item_name} at rate of {rate} items per minute"
    #           "You will need {total_number_of_factories} factories in total to make {desired_item}"

oil_in_dict = False

if 'crude-oil' in item_dict:
    oil_in_dict = True
    oil_rate = rate_float_list[-1]
    item_dict.pop('crude-oil')

driver.quit()

for i in item_dict:
    print(f"You will need {item_dict.get(i)[1]} {item_dict.get(i)[0]}'s making {i} at a rate of {item_dict.get(i)[2]} items per minute")
if oil_in_dict:
    print(f"You will need to produce crude-oil at a rate of {oil_rate} items per minute")
print(f"You will need {sum(factory_elem_int_list)} factories in total to make {item_input}")

# TODO: (DONE) Clean up output
# Format - "You will need {num_of_assemblers} to create {item}" repeat for item and each subitem and then "You will need a total of {tot_num_of_assemblers}"
    # TODO: (DONE) Cycle through item and subitem names similar to number of assemblers
        # TODO: (DONE) Cycle through assembler_elem_list and check to make sure it is not a liquid
        # Something like for item and subitem names but with image before assembler_count
# TODO: (DONE) Feature - change the assembler count or rate with input from prompt
# TODO: (DONE) Feature - ouput includes how many miners, furnaces, chemical plants, and oil refineries neeeded for recipe    
    # Step 1: Chemical Plants
    # Step 2: Furnaces
    # Step 3: Miners
    # Step 4: Oil Refineries
# TODO: Feature - ouput includes how much power each subrecipe will take and how much power the recipe will take in total
# TODO: Feature - ouput includes how many belts of each material each subrecipe needs and how many belts of the item will be produced
# TODO: (DONE) Feature - output includes rate at which each subitem will be made in order to supply recipe for main item
# TODO: Add crude oil into output

# zach was here
# twice