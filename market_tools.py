import pandas as pd 
import difflib 
import json 
import requests
import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
from io import StringIO

#
def _get_apmc_by_commodity(Comm):
    MSAMB_URL = "https://www.msamb.com/ApmcDetail/APMCPriceInformation" # Replace with actual URL
    brave_path = '/opt/brave.com/brave/brave'

    # 1. OPTIMIZE BROWSER OPTIONS FOR SPEED
    options = webdriver.ChromeOptions()
    options.binary_location = brave_path
    options.add_argument('--headless=new')           # Do not open a visible browser window
    options.add_argument('--disable-gpu')            # Disable GPU hardware acceleration
    options.add_argument('--no-sandbox')             # Bypass OS security model (required for headless on Linux)
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
    options.add_argument('--blink-settings=imagesEnabled=false') # Do not load images (Huge speed boost)
    options.page_load_strategy = 'eager'             # Don't wait for CSS/Images to fully load

    # Initialize WebDriver
    service = Service()
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        print("🚀 Loading page...")
        driver.get(MSAMB_URL)
        
        # 2. HANDLE LANGUAGE SELECTION
        lang_element = wait.until(EC.element_to_be_clickable((By.ID, "language")))
        lang_select = Select(lang_element)
        
        if "English" not in lang_select.first_selected_option.text:
            print("🌐 Switching to English...")
            # Get a reference to the dropdown BEFORE changing language
            drp_commodities = driver.find_element(By.ID, "drpCommodities")
            lang_select.select_by_visible_text("English")
            
            # Wait until the old dropdown is destroyed (meaning the page reloaded/updated)
            wait.until(EC.staleness_of(drp_commodities))
            
            # Wait for the new dropdown to be clickable
            wait.until(EC.element_to_be_clickable((By.ID, "drpCommodities")))

        # 3. SELECT COMMODITY & WAIT FOR AJAX REFRESH
        print("🌾 Selecting commodity...")
        drp_element = wait.until(EC.presence_of_element_located((By.ID, "drpCommodities")))
        dropdown = Select(drp_element)
        
        crop_name = Comm
        found = False
        
        for opt in dropdown.options:
            if crop_name.upper() in opt.text.upper():
                # Grab a reference to the CURRENT table before we click
                old_table = driver.find_element(By.CSS_SELECTOR, "table.table.custom-table")
                
                dropdown.select_by_visible_text(opt.text)
                found = True
                
                # THE MAGIC WAIT: Wait until the old table disappears from the DOM 
                # This guarantees the AJAX request finished and the new data is rendering
                wait.until(EC.staleness_of(old_table))
                break

        if not found:
            print(f"❌ Crop '{crop_name}' not found in dropdown.")
        else:
            # 4. EXTRACT DATA
            print("📊 Extracting table...")
            # Wait for the NEW table to be present
            table_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table.custom-table")))
            table_html = table_element.get_attribute('outerHTML')
            
            df = pd.read_html(StringIO(table_html))[0]
            return df
            
            # print(df.head())

    finally:
        # Always close the browser, even if the code crashes, to prevent memory leaks
        driver.quit()
        
        
#TODO: add this for the trending data 
def _get_commodities_by_district(District):
    pass

def __clean_market_data(df):
    """Cleans the messy MSAMB data using fast vectorized forward-fill."""
    
    # Extract dates and forward fill
    date_series = pd.to_datetime(df.iloc[:, 0], format="%d/%m/%Y", errors='coerce')
    df['Date'] = date_series
    df['Date'] = df['Date'].ffill()
    
    # Drop header garbage and rename
    clean = df[date_series.isna() & df.iloc[:, 0].notna()].copy()
    clean.rename(columns={
        0: 'APMC', 1: 'Variety', 2: 'Unit', 3: 'Quantity',
        4: 'Min_Price', 5: 'Max_Price', 6: 'Modal_Price'
    }, inplace=True)
    
    # Typecast text to numbers
    for col in ['Quantity', 'Min_Price', 'Max_Price', 'Modal_Price']:
        clean[col] = pd.to_numeric(clean[col].astype(str).str.replace(",", ""), errors='coerce')
        
    return clean

def get_market_price(crop_name: str, location: str) -> str:
    
    """
    Gets the best market price for the crop
    
    :param crop_name: Description
    :type crop_name: str
    :param location: Description
    :type location: str
    :return: Description
    :rtype: str
    """
    
    df = _get_apmc_by_commodity(crop_name)
    df = __clean_market_data(df)
    
    if df.empty:
        return f"no data found for {crop_name}"
    
    available_apmcs = df['APMC'].unique().tolist()

    exact_matches = [apmc for apmc in available_apmcs if str(location).upper() in str(apmc).upper()]
    if exact_matches:
        best_match = exact_matches[0]
    else:
        fuzzy = difflib.get_close_matches(str(location).upper(), available_apmcs, n=1, cutoff=0.6)
        if fuzzy:
            best_match = fuzzy[0]
            
    # 2. RESULT GENERATION
    if best_match:
        # Isolate all historical data for this specific market
        market_history = df[df['APMC'] == best_match]
        
        # Find the absolute latest date this market reported data
        latest_market_date = market_history['Date'].max()
        
        # Filter down to just that day and grab the variety with the highest arrivals
        latest_data = market_history[market_history['Date'] == latest_market_date]
        best_row = latest_data.loc[latest_data['Quantity'].idxmax()]
        
        date_str = pd.to_datetime(latest_market_date).strftime('%d-%b-%Y')
        
        return (
            f"💰 **Rate in {best_row['APMC']}** (Last updated: {date_str}):\n"
            f"- **Modal Price:** ₹{int(best_row['Modal_Price'])}per {best_row['Unit']}\n"
            f"- **Arrivals:** {int(best_row['Quantity'])} {best_row['Unit']}"
        )

    else:
        # --- THE STATE BENCHMARK FALLBACK ---
        # If the market isn't found anywhere in the dataset, get the absolute latest date overall
        absolute_latest_date = df['Date'].max()
        today_df = df[df['Date'] == absolute_latest_date]
        
        # Find the market with the highest volume on that day
        major = today_df.loc[today_df['Quantity'].idxmax()]
        date_str = pd.to_datetime(absolute_latest_date).strftime('%d-%b-%Y')
        
        return (
            f"⚠️ **{location} not found** in the recent market data.\n"
            f"📈 **State Benchmark ({major['APMC']} on {date_str}):** ₹{int(major['Modal_Price'])} "
            f"(Arrivals: {int(major['Quantity'])} {major['Unit']})"
        )

#TODO: create function are test other tools with UI 
def get_trending_crops(Loc):
    pass