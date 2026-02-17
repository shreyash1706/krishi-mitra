import json
import requests
from datetime import datetime, timedelta



def get_agri_forecast(lat, lon):
    """
    Returns 7-day forecast with Agriculture-specific parameters.
    Covers: Spraying conditions, Irrigation needs, Disease risk data.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": [
            "temperature_2m_max", 
            "temperature_2m_min", 
            "precipitation_sum", 
            "et0_fao_evapotranspiration", # Crop water loss (Critical for irrigation)
            "precipitation_probability_max"
        ],
        "hourly": [
            "relative_humidity_2m", # Critical for Pests/Disease
            "wind_speed_10m",       # Critical for Spraying
            "soil_moisture_3_to_9cm" # Critical for Sowing
        ],
        "timezone": "auto"
    }
    
    response = requests.get(url, params=params).json()
    
    # We simplify the hourly data to daily averages for the LLM
    # (LLMs struggle with 168 hours of raw data, so we summarize)
    daily_data = []
    hourly = response.get('hourly', {})
    daily = response.get('daily', {})
    
    for i in range(7):
        # Calculate daily averages from hourly data
        start_idx = i * 24
        end_idx = (i + 1) * 24
        
        avg_humidity = sum(hourly['relative_humidity_2m'][start_idx:end_idx]) / 24
        max_wind = max(hourly['wind_speed_10m'][start_idx:end_idx])
        avg_soil_moisture = sum(hourly['soil_moisture_3_to_9cm'][start_idx:end_idx]) / 24
        
        day_info = {
            "date": daily['time'][i],
            "max_temp": daily['temperature_2m_max'][i],
            "min_temp": daily['temperature_2m_min'][i],
            "rain_mm": daily['precipitation_sum'][i],
            "water_loss_mm": daily['et0_fao_evapotranspiration'][i],
            "avg_humidity": round(avg_humidity, 1),
            "max_wind_kph": max_wind,
            "soil_moisture": round(avg_soil_moisture, 2)
        }
        daily_data.append(day_info)
        
    return daily_data


def get_historical_rainfall(lat, lon, start_date, end_date):
    """
    Fetches total rainfall and max temp for a past date range.
    Useful for comparing seasons (e.g., "Rainfall last June vs this June").
    """
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date, # Format YYYY-MM-DD
        "end_date": end_date,
        "daily": ["precipitation_sum", "temperature_2m_max"],
        "timezone": "auto"
    }

    data = requests.get(url, params=params).json()

    total_rain = sum(data['daily']['precipitation_sum'])
    avg_max_temp = sum(data['daily']['temperature_2m_max']) / len(data['daily']['temperature_2m_max'])

    return {
        "period": f"{start_date} to {end_date}",
        "total_rainfall_mm": round(total_rain, 2),
        "avg_max_temp": round(avg_max_temp, 1)
    }


def get_soil_details(lat, lon):
    """
    Fetches soil data from ISRIC SoilGrids 2.0.
    Fixes:
    1. Requests valid depth slices (0-5, 5-15, 15-30) instead of invalid '0-30cm'.
    2. Performs Weighted Average to get a true 0-30cm Root Zone profile.
    3. Handles 'None' values for coastal/water locations.
    """
    url = "https://rest.isric.org/soilgrids/v2.0/properties/query"
    
    # Standard SoilGrids depths that make up the topsoil
    depths = ["0-5cm", "5-15cm", "15-30cm"]
    
    params = {
        "lat": lat,
        "lon": lon,
        "property": [
            "phh2o", "nitrogen", "soc", "clay", "sand", "silt",
            "cec", "bdod", "wv0033", "wv1500"
        ],
        "depth": depths,
        "value": "mean"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # Check if we landed in the ocean (Empty Layer List)
        layers = data.get('properties', {}).get('layers', [])
        if not layers:
            return "⚠️ No soil data found. Location might be over water or outside mapped area."

        props = {}
        
        # --- WEIGHTED AVERAGING LOGIC ---
        # 0-5cm (Weight 5), 5-15cm (Weight 10), 15-30cm (Weight 15) -> Total 30
        weights = {"0-5cm": 5, "5-15cm": 10, "15-30cm": 15}
        total_weight = 30

        for layer in layers:
            name = layer['name']
            weighted_sum = 0
            valid_depths = 0
            
            for depth_record in layer['depths']:
                label = depth_record['label']
                val = depth_record['values']['mean']
                
                # Only process if we have a value and it's one of our target depths
                if val is not None and label in weights:
                    weighted_sum += val * weights[label]
                    valid_depths += weights[label]
            
            # If we found data for this property, calculate average
            if valid_depths > 0:
                final_val = weighted_sum / valid_depths
                
                # Apply Unit Conversions
                if name == "phh2o": props['pH'] = final_val / 10.0
                elif name == "nitrogen": props['Nitrogen'] = final_val / 100.0 # g/kg
                elif name == "soc": props['Organic_Carbon'] = final_val / 10.0 # g/kg
                elif name == "clay": props['Clay'] = final_val / 10.0 # %
                elif name == "sand": props['Sand'] = final_val / 10.0 # %
                elif name == "silt": props['Silt'] = final_val / 10.0 # %
                elif name == "cec": props['CEC'] = final_val / 10.0
                elif name == "bdod": props['Bulk_Density'] = final_val / 100.0
                elif name == "wv0033": props['Field_Capacity'] = final_val / 10.0
                elif name == "wv1500": props['Wilting_Point'] = final_val / 10.0

        # --- CHECK IF DATA IS EMPTY ---
        if not props:
            return "⚠️ Soil data is NULL for this location (Likely Coastal/Water)."

        # --- DERIVED INTELLIGENCE ---
        clay = props.get('Clay', 0)
        sand = props.get('Sand', 0)
        
        # Texture Class
        if clay >= 40: texture = "Clay (Heavy)"
        elif sand >= 50: texture = "Sandy (Light)"
        elif clay >= 27 and sand <= 50: texture = "Clay Loam"
        else: texture = "Loam (Medium - Ideal)"
        
        # Available Water Capacity
        awc = props.get('Field_Capacity', 0) - props.get('Wilting_Point', 0)
        
        return (
            f"🌱 **Soil Analysis for {lat,lon}(Root Zone 0-30cm):**\n"
            f"- **Type:** {texture} (Clay: {round(clay,1)}% | Sand: {round(sand,1)}%)\n"
            f"- **Health:** pH {round(props.get('pH', 0), 1)} | Organic Carbon: {round(props.get('Organic_Carbon', 0), 1)} g/kg\n"
            f"- **Nutrients:** Nitrogen: {round(props.get('Nitrogen', 0), 2)} g/kg | CEC: {round(props.get('CEC', 0), 1)}\n"
            f"- **Water:** Holds approx {round(awc, 1)}% available water."
        )

    except Exception as e:
        return f"Error fetching soil data: {str(e)}"
