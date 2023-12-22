# This is a sample Python script.
from googletrans import Translator
import tkinter as tk
from tkinter import scrolledtext
import threading
import json

translator = Translator()


def translated(text):
    result = translator.translate(text, dest='tr', src='de')
    return result.text

def close_window():
    window.destroy()



def selenium_task(entry, text_price):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.chrome.service import Service
    import time
    import random


    description = ''

    my_id = entry.get()

    # URL of the webpage to scrape
    my_page = "https://suchen.mobile.de/fahrzeuge/details.html?id=" + str(my_id)

    # Geckodriver'ın yolunu belirtin
    geckodriver_path = '/Users/kasimtugrulvural/Downloads/geckodriver'  # Geckodriver'ın indirildiği yeri buraya yazın
    service = Service(executable_path=geckodriver_path)

    # Firefox WebDriver nesnesini oluşturun
    driver = webdriver.Firefox(service=service)

    # Web sayfasını açın
    driver.get(my_page)

    # Wait for the page to load completely
    time.sleep(15)
    # "Einverstanden" butonunu bulun ve tıklayın
    accept_button = driver.find_element(By.CLASS_NAME, "mde-consent-accept-btn")
    accept_button.click()

    time.sleep(random.randint(1, 3))

    # Scroll down the page to simulate user interaction
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.randint(1, 3))

    # Scroll up the page a bit
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(random.randint(1, 3))

    # Find all image elements in the specified div
    image_elements = driver.find_elements(By.CSS_SELECTOR, ".slick-slide img")

    # Extract the image URLs
    image_urls = [img.get_attribute('src') or img.get_attribute('data-lazy') for img in image_elements]

    # `id`'si "ad-title" olan <h1> etiketini bulun
    ad_title_element = driver.find_element(By.ID, "ad-title")

    # Etiketin metnini alın
    ad_title = ad_title_element.text

    # `data-testid="prime-price"` niteliğine sahip elementi bulun
    price_element = driver.find_element(By.CSS_SELECTOR, "span[data-testid='prime-price']")

    # Elementin metnini alın
    product_price = price_element.text
    time.sleep(random.randint(1, 3))

    try:
        # "Impressum & weitere Angaben" linkine tıklayın
        show_more_link = driver.find_element(By.ID, "show-more-link")
        ActionChains(driver).click(show_more_link).perform()
        time.sleep(random.randint(1, 3))
        # `class` niteliği "imprint" olan div elementini bulun
        imprint_element = driver.find_element(By.CLASS_NAME, "imprint")

        # Elementin metnini alın
        imprint_text = imprint_element.text
    except:
        # `class` niteliği "description" olan div elementini bulun
        description_element = driver.find_element(By.CLASS_NAME, "description")

        # Elementin HTML içeriğini alın
        description_html = description_element.get_attribute('innerHTML')

        # HTML etiketlerini temizleyerek düz metin elde edin
        imprint_text = description_html.replace('<br>', '\n').replace('<br/>', '\n')

    time.sleep(random.randint(1, 3))
    # Tüm özellik çiftlerini bulun
    feature_labels = driver.find_elements(By.CSS_SELECTOR, "#td-box .g-row .g-col-6:first-child")
    feature_values = driver.find_elements(By.CSS_SELECTOR, "#td-box .g-row .g-col-6:last-child")

    # Özelliklerin metinlerini alın
    features = {label.text: value.text for label, value in zip(feature_labels, feature_values)}

    driver.close()
    # Close the browser
    driver.quit()

    # Print the URLs or process them as needed
    images = []
    for url in image_urls:
        if 'mo-1024' in url:
            images.append(url)

    title = ad_title
    price = product_price.replace('€', '').strip()
    detail = features
    description = imprint_text
    all_images = images

    all_text = str({
        "pro_id": my_id,
        "title": title,
        "price": price,
        "details": detail,
        "description": description,
        "images": all_images  # Görsel URL'leri burada saklayın
    })



    # Sonucu Tkinter metin alanına yaz
    text_price.configure(state='normal')  # Metin alanını düzenlenebilir yap
    text_price.delete('1.0', tk.END)  # Önceki metni temizle
    text_price.insert(tk.END, all_text)  # Sonucu ekle
    text_price.configure(state='disabled')  # Metin alanını tekrar düzenlenemez yap

    data = {
        "pro_id": my_id,
        "title": title,
        "url": my_page,
        "price": price,
        "details": detail,
        "description": description,
        "images": all_images  # Görsel URL'leri burada saklayın
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


    # Görsel URL'lerini alın ve döndürün
    return data







def start_selenium_thread(entry, text_price):


    text_price.configure(state='normal')
    text_price.delete('1.0', tk.END)
    text_price.insert(tk.END, "Yükleniyor...")
    text_price.configure(state='disabled')


    # Selenium işlemini başka bir thread'de başlat
    threading.Thread(target=selenium_task, args=(entry, text_price), daemon=True).start()




# Tkinter penceresini oluştur
window = tk.Tk()
window.title("Selenium ile Web Scraping")

# Giriş alanı
entry = tk.Entry(window, width=100)
entry.pack()

# Gönderme butonu
submit_button = tk.Button(window, text="Gönder", command=lambda: start_selenium_thread(entry, text_price))
submit_button.pack(pady=(20, 20))



close_button = tk.Button(window, text="Kapat", command=close_window)
close_button.pack(pady=(0, 20))


# Metin alanı
text_price = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=60, height=60, state='disabled')
text_price.pack()


# Pencereyi başlat
window.mainloop()
