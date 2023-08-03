
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
import time

class CookieClickerBot:
    def __init__(self, chrome_driver_path):
        options = ChromeOptions()
        options.add_experimental_option("detach", True)
        ser = Service(chrome_driver_path)
        self.driver = webdriver.Chrome(service=ser, options=options)
        self.driver.get('http://orteil.dashnet.org/experiments/cookie/')
        
    def click_cookie(self):
        cookie = self.driver.find_element(By.ID, value='cookie')
        cookie.click()
    
    def get_store_items(self):
        items = self.driver.find_elements(By.CSS_SELECTOR, "#store div")
        item_ids = [item.get_property("id") for item in items if item.find_elements(By.CSS_SELECTOR, "b")]
        return item_ids
    
    def get_item_prices(self):
        all_prices = self.driver.find_elements(By.CSS_SELECTOR, value='#store div b')
        item_prices = []
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)
        return item_prices
    
    def get_cash(self):
        cash = self.driver.find_element(By.ID, value='money').text
        if ',' in cash:
            cash = cash.replace(',', '')
        cash = int(cash)
        return cash
    
    def purchase_item(self, item_id):
        self.driver.find_element(By.ID, value=item_id).click()
            
            
    def run(self, duration=5*60):
        timeout = time.time() + 5
        five_min = time.time() + duration

        while True:
            current_time = time.time()
            self.click_cookie()
            
            if current_time > timeout:
                print('5 Second arrived.')

                item_ids = self.get_store_items()
                item_prices = self.get_item_prices()
                cash = self.get_cash()
                
                upgrade_dict = {price: item_id for price, item_id in zip(item_prices, item_ids)}
                
                affordable_items = {price: item_id for price, item_id in upgrade_dict.items() if cash > price}
                
                if affordable_items:
                    highest_price_affordable_upgrade = max(affordable_items)
                    print(highest_price_affordable_upgrade)
                    to_purchase_id = affordable_items[highest_price_affordable_upgrade]
                    print('here: ',to_purchase_id)
                    self.purchase_item(to_purchase_id)
                
                timeout = time.time() + 5

            if current_time > five_min:
                cookie_per_s = self.driver.find_element(By.ID, value="cps").text
                print(cookie_per_s)
                break

        self.driver.quit()

if __name__ == "__main__":
    chrome_driver_path = '/Users/lcy/Development/chromedriver'
    bot = CookieClickerBot(chrome_driver_path)
    bot.run()

