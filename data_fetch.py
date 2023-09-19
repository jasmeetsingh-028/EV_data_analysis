import requests
from bs4 import BeautifulSoup
import pandas as pd


url = 'https://ev-database.org/#sort:path~type~order=.rank~number~desc|range-slider-range:prev~next=0~1200|range-slider-acceleration:prev~next=2~23|range-slider-topspeed:prev~next=110~350|range-slider-battery:prev~next=10~200|range-slider-towweight:prev~next=0~2500|range-slider-fastcharge:prev~next=0~1500|paging:currentPage=0|paging:number=9'
response = requests.get(url)

# Checking if the request was successful (status code 200)
if response.status_code == 200:
    print('Response: Success!')
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Finding all the div elements with class "list-item"
    items = soup.find_all('div', class_='list-item')
    

    titles = []
    battery_sizes = []
    top_speeds = []
    ranges = []
    efficiencies = []
    fastcharges = []
    price = []
    
    for item in items:
        title = item.find('h2').text.strip()
        battery_size = item.find('span', class_='battery').text.strip()
        top_speed = item.find('span', class_='topspeed').text.strip()
        range = item.find('span', class_='erange_real').text.strip()
        efficiency = item.find('span', class_='efficiency').text.strip()
        fastcharge = item.find('span', class_='fastcharge_speed_print').text.strip()
        price_uk = item.find('span', class_='country_uk').text.strip()
        price_uk_cleaned = price_uk.replace('*', '')
        price_uk_cleaned = price_uk_cleaned.replace('£', '')
        
        titles.append(title)
        battery_sizes.append(battery_size)
        top_speeds.append(top_speed)
        ranges.append(range)
        efficiencies.append(efficiency)
        fastcharges.append(fastcharge)
        price.append(price_uk_cleaned)
    
    #creating dataframe
    data = {
        'Title': titles,
        'Battery Size (kWh)': battery_sizes,
        'Top Speed (km/h)': top_speeds,
        'Range (km)': ranges,
        'Efficiency (Wh/km)': efficiencies,
        'Fastcharge Speed (km/h)': fastcharges,
        'price': price
    }
    
    df = pd.DataFrame(data)
    print(df)
    
    df.to_csv('ev_data1.csv')
    
else:
    print('Failed to retrieve the webpage. Status code:', response.status_code)
