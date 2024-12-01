import datetime
from datetime import timezone
from crews.enterprise_crew.enterprise_crew import EnterpriseAnalystCrew

# result = IotAnalystCrew().crew().kickoff(inputs={
#     "plant_data": "capscicum, temperature 27 celcius, humidity 66, light intensity 23,000 lux, Co2 levels 500ppm"
# })
import json

# Crop Yield Data
crop_yield_data = '''
{
    "farm_details": {
        "name": "UCIARS",
        "location": "Colombo, Srilanka",
        "total_farm_area": 5.5,
        "total_cultivated_area": 4.2
    },
    "crop_yields": [
        {
            "crop": "Chillies",
            "cultivated_area_hectares": 1.5,
            "expected_yield": 12000,
            "actual_yield": 11500,
            "yield_unit": "kg",
            "avg_price_per_kg": 350
        },
        {
            "crop": "Capsicum",
            "cultivated_area_hectares": 1.2,
            "expected_yield": 9600,
            "actual_yield": 9200,
            "yield_unit": "kg",
            "avg_price_per_kg": 280
        },
        {
            "crop": "Tomatoes",
            "cultivated_area_hectares": 1.5,
            "expected_yield": 15000,
            "actual_yield": 14300,
            "yield_unit": "kg",
            "avg_price_per_kg": 220
        }
    ]
}
'''

# Operational Costs Data
operational_costs_data = '''
{
    "operational_costs": {
        "labor_costs": 450000,
        "seeds_and_saplings": 75000,
        "fertilizer_expenses": 120000,
        "pesticide_costs": 85000,
        "irrigation_costs": 65000,
        "equipment_maintenance": 90000,
        "packaging_materials": 55000,
        "transportation_costs": 70000,
        "total_operational_costs": 1015000
    }
}
'''

# Revenue Data
revenue_data = '''
{
    "revenue_breakdown": {
        "chillies_revenue": 4025000,
        "capsicum_revenue": 2576000,
        "tomatoes_revenue": 3146000,
        "total_revenue": 9747000,
        "net_profit": 8732000
    }
}
'''

# Employee Information
employee_data = '''
{
    "workforce": {
        "total_employees": 12,
        "permanent_staff": 5,
        "seasonal_workers": 7,
        "average_daily_wage": 2500,
        "employee_performance": {
            "productivity_score": 0.82,
            "average_work_hours": 8,
            "overtime_hours_per_month": 45
        }
    }
}
'''

# Weather and Agricultural Conditions
weather_data = '''
{
    "agricultural_conditions": {
        "average_temperature": 28.5,
        "rainfall_mm": 275,
        "humidity_percentage": 80,
        "sunshine_hours_per_day": 6.2,
        "soil_quality_index": 0.75,
        "irrigation_water_quality": "Good"
    }
}
'''

# Market and Input Costs
market_data = '''
{
    "market_data": {
        "input_costs": {
            "fertilizer_price_per_kg": 45,
            "pesticide_price_per_liter": 850,
            "seeds_price_per_kg": 550
        },
        "market_prices": {
            "chillies_wholesale_price": 380,
            "capsicum_wholesale_price": 300,
            "tomatoes_wholesale_price": 240
        },
        "market_demand": {
            "chillies": "High",
            "capsicum": "Moderate",
            "tomatoes": "Stable"
        }
    }
}
'''

# Farm Infrastructure
infrastructure_data = '''
{
    "farm_infrastructure": {
        "greenhouses": 2,
        "irrigation_system": "Drip Irrigation",
        "storage_capacity": 10000,
        "storage_unit_type": "Refrigerated Warehouse",
        "equipment_list": [
            "Tractor",
            "Irrigation Pump",
            "Harvesting Tools",
            "Sorting Machine"
        ]
    }
}
'''

def parse_agricultural_data():
    """
    Parse all agricultural business data and return structured variables
    """
    # Parse Crop Yield Data
    crop_yield = json.loads(crop_yield_data)
    farm_name = crop_yield['farm_details']['name']
    farm_location = crop_yield['farm_details']['location']
    total_farm_area = crop_yield['farm_details']['total_farm_area']
    crop_yields = crop_yield['crop_yields']

    # Parse Operational Costs
    operational_costs = json.loads(operational_costs_data)['operational_costs']

    # Parse Revenue Data
    revenue = json.loads(revenue_data)['revenue_breakdown']

    # Parse Employee Data
    employee_info = json.loads(employee_data)['workforce']

    # Parse Weather Data
    weather_conditions = json.loads(weather_data)['agricultural_conditions']

    # Parse Market Data
    market_info = json.loads(market_data)['market_data']

    # Parse Infrastructure Data
    infrastructure = json.loads(infrastructure_data)['farm_infrastructure']

    return {
        'farm_name': farm_name,
        'farm_location': farm_location,
        'total_farm_area': total_farm_area,
        'crop_yields': crop_yields,
        'operational_costs': operational_costs,
        'revenue': revenue,
        'employee_info': employee_info,
        'weather_conditions': weather_conditions,
        'market_info': market_info,
        'infrastructure': infrastructure
    }

# print(result)