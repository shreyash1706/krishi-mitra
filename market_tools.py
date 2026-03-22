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

def __fetch_table(selector, type):
    MSAMB_URL = "https://www.msamb.com/ApmcDetail/APMCPriceInformation" 
    import platform
    import shutil
    import os

    # 1. OPTIMIZE BROWSER OPTIONS FOR SPEED
    options = webdriver.ChromeOptions()
    
    # Auto-detect browser: use Chrome by default (works cross-platform)
    # Only set binary_location if Brave is found on Linux
    if platform.system() == "Linux":
        brave_path = shutil.which("brave-browser") or '/opt/brave.com/brave/brave'
        if os.path.exists(brave_path):
            options.binary_location = brave_path
    # On Windows: just use system Chrome (no binary_location needed)
    
    options.add_argument('--headless=new')           # Do not open a visible browser window
    options.add_argument('--disable-gpu')            # Disable GPU hardware acceleration
    options.add_argument('--no-sandbox')             # Bypass OS security model (required for headless on Linux)
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
    options.add_argument('--blink-settings=imagesEnabled=false') # Do not load images (Huge speed boost)
    options.page_load_strategy = 'eager'             # Don't wait for CSS/Images to fully load

    # Initialize WebDriver
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
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
            
        title_element = wait.until(EC.element_to_be_clickable((By.ID, "APMCTitle")))
        title_element.click()
        time.sleep(1)
        option_element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, type)))
        option_element.click()
        time.sleep(1)

        # 3. SELECT COMMODITY & WAIT FOR AJAX REFRESH
        print("🌾 Selecting value")
        if type == "Commodity- District Wise":
            drp_element = wait.until(EC.presence_of_element_located((By.ID, "drpCommodityDistrict")))
        else:
            drp_element = wait.until(EC.presence_of_element_located((By.ID, "drpDistrictCommodity")))
            
        dropdown = Select(drp_element)
            
        selector_name = selector
        found = False
        
        for opt in dropdown.options:
            if selector_name.upper() in opt.text.upper():
                dropdown.select_by_visible_text(opt.text)
                found = True
                
                # --- THE BULLETPROOF AJAX WAIT ---
                print("⏳ Waiting for MSAMB server data to load...")
                time.sleep(1) # Brief pause to let the website trigger the loading screen
                
                # Determine which loading overlay to watch
                if type == "Commodity- District Wise":
                    loading_id = "OdivCommodityDistrictGird"
                else:
                    loading_id = "OdivDistrictCommodityGird"
                
                # Wait up to 10 seconds for the "Data is loading..." text to DISAPPEAR
                wait.until(EC.invisibility_of_element_located((By.ID, loading_id)))
                
                # Add one final tiny sleep just to let the browser paint the HTML table
                time.sleep(0.5) 
                break

        if not found:
            print(f"❌ Selector '{selector_name}' not found in dropdown.")
        else:
            # 4. EXTRACT DATA
            print("📊 Extracting table...")
            # Wait for the NEW table to be present
            if type == "Commodity- District Wise":
                target_div_id = "CommodityDistrictGird"
            else:
                target_div_id = "DistrictCommodityGird"
                
            # 2. Build a CSS Selector that looks INSIDE that specific Div
            table_selector = f"div#{target_div_id} table.custom-table"
            
            # 3. Wait for and grab that exact table
            table_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, table_selector)))
            table_html = table_element.get_attribute('outerHTML')
            
            # 4. Convert to Pandas
            from io import StringIO
            df = pd.read_html(StringIO(table_html))[0]
            
            return df
            
            # print(df.head())
            
    except Exception as e:
        raise e

    finally:
        # Always close the browser, even if the code crashes, to prevent memory leaks
        driver.quit()

#
def _get_districts_by_commodity(Comm):
    return __fetch_table(Comm, "Commodity- District Wise")
    
        
        
#TODO: add this for the trending data 
def _get_commodities_by_district(District):
    return __fetch_table(District, "District- Commodity Wise")

def __clean_market_data(df, entity_col_name="Entity"):
    """Cleans the messy MSAMB data dynamically based on the table type."""
    
    # 1. Extract dates and forward fill
    date_series = pd.to_datetime(df.iloc[:, 0], format="%d/%m/%Y", errors='coerce')
    df['Date'] = date_series
    df['Date'] = df['Date'].ffill()
    
    # 2. Filter out header garbage, date rows, AND "State Total" rows
    mask = (
        date_series.isna() & 
        df.iloc[:, 0].notna() & 
        ~df.iloc[:, 0].astype(str).str.contains('Total|Date', case=False, na=False)
    )
    clean = df[mask].copy()
    
    # 3. Force overwrite columns. The first column becomes whatever we pass in!
    clean.columns = [entity_col_name, 'Variety', 'Unit', 'Quantity', 'Min_Price', 'Max_Price', 'Modal_Price', 'Date']
    
    # 4. Typecast text to numbers safely
    for col in ['Quantity', 'Min_Price', 'Max_Price', 'Modal_Price']:
        clean[col] = pd.to_numeric(clean[col].astype(str).str.replace(",", ""), errors='coerce')
        
    # Drop any rows that accidentally became empty during parsing
    clean = clean.dropna(subset=[entity_col_name, 'Quantity', 'Modal_Price'])
        
    return clean

def get_market_price(crop_name: str, district: str) -> str:
    
    """
    Gets the best market price for the crop
    
    :param crop_name: Description
    :type crop_name: str
    :param district: Description
    :type district: str
    :return: Description
    :rtype: str
    """
    
    df = _get_districts_by_commodity(crop_name)
    df = __clean_market_data(df, entity_col_name="District")
    
    if df.empty:
        return f"no data found for {crop_name}"
    
    available_districts = df['District'].unique().tolist()

    best_match = None
    location_upper = str(district).upper().strip()
    
    # 1. Substring Match
    exact_matches = [apmc for apmc in available_districts if location_upper in str(apmc).upper()]
    
    if exact_matches:
        best_match = exact_matches[0]
    else:
        # 2. Strict Fuzzy Match (85% similarity required)
        import difflib
        fuzzy = difflib.get_close_matches(location_upper, available_districts, n=1, cutoff=0.85)
        if fuzzy:
            best_match = fuzzy[0]   # 2. RESULT GENERATION
    if best_match:
        # Isolate all historical data for this specific market
        market_history = df[df['District'] == best_match]
        
        # Find the absolute latest date this market reported data
        latest_market_date = market_history['Date'].max()
        
        # Filter down to just that day and grab the variety with the highest arrivals
        latest_data = market_history[market_history['Date'] == latest_market_date]
        best_row = latest_data.loc[latest_data['Quantity'].idxmax()]
        
        date_str = pd.to_datetime(latest_market_date).strftime('%d-%b-%Y')
        
        return (
            f"💰 **Rate in {best_row['District']}** (Last updated: {date_str}):\n"
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
            f"⚠️ **{district} not found** in the recent market data.\n"
            f"📈 **State Benchmark ({major['District']} on {date_str}):** ₹{int(major['Modal_Price'])} "
            f"(Arrivals: {int(major['Quantity'])} {major['Unit']})"
        )

#TODO: create function after test other tools with UI 
def get_trending_crops(district: str) -> str:
    """
    Finds trending crops based on Price Growth (Momentum) AND Volume (Arrivals).
    """
    print(f"📈 [TRENDING] Fetching smart market trends for: {district}")
    
    try:
        df_raw = _get_commodities_by_district(district)
    except Exception as e:
        return f"❌ Error fetching data for {district}."
        
    if df_raw is None or df_raw.empty:
        return f"❌ No market data found for district: {district}"
        
    df = __clean_market_data(df_raw, entity_col_name="Commodity")
    
    if df.empty:
        return f"❌ No valid market data available for {district}."

    # 1. Identify our timeline
    latest_date = df['Date'].max()
    earliest_date = df['Date'].min()
    
    # If there is only 1 day of data, fallback to just volume
    if latest_date == earliest_date:
        today_df = df.groupby('Commodity').agg({'Quantity': 'sum', 'Modal_Price': 'mean', 'Unit': 'first'}).reset_index()
        top_vol = today_df.sort_values(by='Quantity', ascending=False).head(3)
        
        result = f"📊 **Market Snapshot for {district.upper()}** ({latest_date.strftime('%d-%b')}):\n"
        for _, row in top_vol.iterrows():
            result += f"- **{row['Commodity']}**: ₹{int(row['Modal_Price'])}/{row['Unit']} ({int(row['Quantity'])} arrived)\n"
        return result

    # 2. Group data by Commodity for the Latest and Earliest dates
    latest_df = df[df['Date'] == latest_date].groupby('Commodity').agg({'Modal_Price': 'mean', 'Quantity': 'sum', 'Unit': 'first'}).reset_index()
    earliest_df = df[df['Date'] == earliest_date].groupby('Commodity').agg({'Modal_Price': 'mean'}).reset_index()

    # 3. Merge them to compare prices
    merged = pd.merge(latest_df, earliest_df, on='Commodity', suffixes=('_latest', '_earliest'))
    
    # 4. Calculate Price Momentum (Percentage Growth)
    merged['Price_Growth_%'] = ((merged['Modal_Price_latest'] - merged['Modal_Price_earliest']) / merged['Modal_Price_earliest']) * 100
    
    # 5. Filter out low-volume noise (e.g., must have at least 50 units arriving to be considered a "trend")
    valid_trends = merged[merged['Quantity'] > 50].copy()

    # --- GENERATE THE TWO-PART RESPONSE ---
    date_str = latest_date.strftime('%d-%b-%Y')
    days_span = (latest_date - earliest_date).days
    
    result = f"📈 **Market Trends in {district.upper()}** (Over the last {days_span} days, ending {date_str}):\n\n"

    # PART 1: Top Price Surges (The profitable stuff)
    top_growth = valid_trends.sort_values(by='Price_Growth_%', ascending=False).head(3)
    if not top_growth.empty:
        result += "🚀 **Highest Price Surges:**\n"
        for _, row in top_growth.iterrows():
            growth = row['Price_Growth_%']
            trend_icon = "🟩 UP" if growth > 0 else "🟥 DOWN"
            
            # Only show it if it actually grew, otherwise ignore
            if growth > 0:
                result += (
                    f"- **{row['Commodity']}**: ₹{int(row['Modal_Price_latest'])}/{row['Unit']} "
                    f"({trend_icon} {growth:.1f}%)\n"
                )

    # PART 2: Highest Volume (The staples)
    top_volume = valid_trends.sort_values(by='Quantity', ascending=False).head(3)
    if not top_volume.empty:
        result += "\n📦 **Highest Arrivals (Flooding the Market):**\n"
        for _, row in top_volume.iterrows():
             result += (
                f"- **{row['Commodity']}**: {int(row['Quantity'])} {row['Unit']} arrived "
                f"(Current Rate: ₹{int(row['Modal_Price_latest'])})\n"
            )

    return result