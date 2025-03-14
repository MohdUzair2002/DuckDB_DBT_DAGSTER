from weather_project.assets import cleaned_weather_data

def test_cleaned_weather_data():
    data = {"temperature": [15, 16], "time": ["12:00", "13:00"]}
    df = cleaned_weather_data(data)
    
    assert not df.empty
    assert "temperature" in df.columns
    assert "time" in df.columns

