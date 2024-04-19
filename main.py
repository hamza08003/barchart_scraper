import json
import time
from datetime import datetime
import pytz
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from bs4 import BeautifulSoup
import re
import mysql.connector
import schedule

keyword_mapping = {
    "Euro": "EUR", "U.S. Dollar": "USD", "Australian Dollar": "AUD",
    "British Pound": "GBP", "Canadian Dollar": "CAD", "Swiss Franc": "CHF",
    "Japanese Yen": "JPY", "New Zealand Dollar": "NZD", "Chinese Yuan": "CNY",
    "Hong Kong Dollar": "HKD", "Singapore Dollar": "SGD", "Mexican Peso": "MXN",
    "Brazilian Real": "BRL", "Russian Ruble": "RUB", "Turkish Lira": "TRY",
    "Saudi Riyal": "SAR",
}


def load_db_creds(filename):
    with open(filename) as file_obj:
        return json.load(file_obj)


def connect_to_db(db_config_filename):
    db_config = load_db_creds(db_config_filename)
    conn = mysql.connector.connect(**db_config)
    print("Connected to database....!\n")
    cursor = conn.cursor(buffered=True, dictionary=True)
    return conn, cursor


def init_chrome_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    return driver, wait


def convert_to_cst(timezone_aware_datetime):
    cst = pytz.timezone('America/Chicago')
    return timezone_aware_datetime.astimezone(cst)


def scrape_data(driver, wait, url):
    try:
        driver.get(url)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'bc-table-scrollable-inner')))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        symbol_div = soup.find('div', class_='symbol-name')
        if symbol_div:
            symbol_name = symbol_div.find('span', class_='symbol').text.strip() + ' ' + symbol_div.find('span', class_='symbol').find_next_sibling().text.strip()

        opinion_status = soup.find('div', class_='opinion-status')

        overall_average = {}

        if opinion_status:
            percent_class = opinion_status.find(lambda tag: tag.name == 'span' and 'opinion-percent' in tag.get('class', []))['class'][1]
            signal_class = opinion_status.find(lambda tag: tag.name == 'span' and 'opinion-signal' in tag.get('class', []))['class'][0]
            percent_value = opinion_status.find('span', class_=percent_class).text.strip()
            signal_value = opinion_status.find('span', class_=signal_class).text.strip()

            overall_average['Overall Percentage'] = percent_value
            overall_average['Overall Signal'] = signal_value

        tables = soup.find_all('table')

        data = []

        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 5:
                    try:
                        indicator_name = cells[1].text.strip()
                        signal = cells[2].text.strip()
                        strength = cells[3].text.strip()
                        direction = cells[4].text.strip()

                        data.append({
                            'Symbol': symbol_name,
                            'Indicator Name': indicator_name,
                            'Signal': signal,
                            'Strength': strength,
                            'Direction': direction
                        })
                    except IndexError:
                        print("IndexError occurred while processing a row.")

    except (NoSuchElementException, StaleElementReferenceException) as e:
        print(f"An exception occurred: {e}")
        return {}

    return {'overall_average': overall_average, 'barchart_opinion': data}


def map_currency(string, mapping_dict):
    components = string.split('/')
    mapped_components = []

    for component in components:
        mapped_component = None
        for keyword, code in mapping_dict.items():
            if keyword in component:
                mapped_component = code
                break
        if mapped_component:
            mapped_components.append(mapped_component)

    if len(mapped_components) == 2:
        return '_'.join(mapped_components)
    elif len(mapped_components) == 1:
        return mapped_components[0]
    else:
        return None


def is_single_currency(url):
    currency_code = url.split('/quotes/')[-1].split('/')[0]
    if re.search(r'[A-Z]{6,}', currency_code):
        return False
    return True


def get_or_create_id(cursor, conn, table_name, column_name, value):
    cursor.execute(f"SELECT id FROM {table_name} WHERE {column_name} = %s", (value,))
    result = cursor.fetchone()
    if result:
        return result['id']
    else:
        cursor.execute(f"INSERT INTO {table_name} ({column_name}) VALUES (%s)", (value,))
        conn.commit()
        return cursor.lastrowid


def save_to_database(cursor, conn, data):
    # Get current time in CST
    cst_time = convert_to_cst(datetime.now(pytz.utc))
    current_time_str = cst_time.strftime('%Y-%m-%d %H:%M:%S')

    signal_value_overall = data['overall_average']['Overall Signal'].upper()
    percent_value_overall = round(float(data['overall_average']['Overall Percentage'].replace('%', '')))
    signal_id = None

    for entry in data['barchart_opinion']:
        currency_short = map_currency(entry['Symbol'], keyword_mapping)
        indicator_name = entry['Indicator Name']
        strength = entry['Strength']
        direction = entry['Direction']

        # Determining 'ind_signal' based on percent value
        if percent_value_overall < 50:
            signal_id = 6  # STAY-OUT
        elif 50 <= percent_value_overall <= 70:
            signal_id = 5 if signal_value_overall == 'BUY' else 4  # BUY or SELL
        elif 71 <= percent_value_overall <= 85:
            signal_id = 1 if signal_value_overall == 'BUY' else 2  # BUY SOON or SELL SOON
        elif 86 <= percent_value_overall <= 100:
            signal_id = 7 if signal_value_overall == 'BUY' else 8  # BUY NOW or SELL NOW

        # Check for the values in the database and get the ID, if not exists, insert the new value and get its ID
        currency_id = get_or_create_id(cursor, conn, "currency", "currency_name", currency_short)
        indicator_id = get_or_create_id(cursor, conn, "ind_name", "ind_name", indicator_name)
        signal_dir_id = get_or_create_id(cursor, conn, "barchart_strength_direction", "signal_type", direction)
        signal_str_id = get_or_create_id(cursor, conn, "barchart_strength_direction", "signal_type", strength)

        # Check if the same data exists for the last 15 minutes
        cursor.execute("""
            SELECT * FROM barchart WHERE currency_id = %s AND ind_name_id = %s AND strength_id = %s AND direction_id = %s
            AND ind_signal_id = %s AND end_time >= DATE_SUB(%s, INTERVAL 15 MINUTE)
        """, (currency_id, indicator_id, signal_str_id, signal_dir_id, signal_id, current_time_str)
        )

        existing_record = cursor.fetchone()

        # If exists, update the end_time and overall_percentage, if not, insert the new record
        if existing_record:
            cursor.execute("""
                UPDATE barchart SET end_time = %s, overall_percentage = %s WHERE id = %s
            """, (current_time_str, percent_value_overall, existing_record['id'])
            )
        else:
            cursor.execute("""
                INSERT INTO barchart (currency_id, ind_name_id, strength_id, direction_id, ind_signal_id, start_time, end_time, overall_percentage)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (currency_id, indicator_id, signal_str_id, signal_dir_id, signal_id, current_time_str, current_time_str, percent_value_overall)
            )

        conn.commit()


with open('links.txt') as f:
    links = f.readlines()
    links = [x.strip() for x in links]


# def save_to_json(data, filename):
#     with open(filename, 'w', encoding='utf-8') as jsonfile:
#         json.dump(data, jsonfile, ensure_ascii=False, indent=4)


def run_job():
    conn, cursor = connect_to_db('db_config.json')
    driver, wait = init_chrome_driver()

    with open('links.txt') as file_obj:
        url_list = [line.strip() for line in file_obj.readlines()]

    for idx, url in enumerate(url_list):
        if is_single_currency(url):
            print(f"Scraping data from URL # {idx + 1}")
            data = scrape_data(driver, wait, url)
            print(f"Data scraped from URL # {idx + 1}")
            print("Saving data to the database....")
            save_to_database(cursor, conn, data)
            print("Data saved to the database....\n")
            print("------------------------------------------\n")
        else:
            print(f"Skipping URL # {idx + 1} as it is not a single currency URL\n")
            print("------------------------------------------\n")

    driver.quit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    run_job()
    # schedule.every(15).minutes.do(run_job)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1.5)

