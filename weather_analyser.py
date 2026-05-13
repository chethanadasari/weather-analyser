import requests
import matplotlib.pyplot as plt
import numpy as np

# ── Fetch real live weather data for Dublin ──
# Using Open-Meteo API (100% free, no account needed!)

def get_dublin_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 53.3498,
        "longitude": -6.2603,
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "forecast_days": 7
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

# ── Get the data ──
print("Fetching live weather data for Dublin...")
data = get_dublin_weather()

hours = data["hourly"]["time"]
temperature = data["hourly"]["temperature_2m"]
humidity = data["hourly"]["relative_humidity_2m"]
wind_speed = data["hourly"]["wind_speed_10m"]

# Use only first 72 hours (3 days)
hours = hours[:72]
temperature = temperature[:72]
humidity = humidity[:72]
wind_speed = wind_speed[:72]

# ── Create day labels ──
day_labels = [h[5:10] + " " + h[11:16] for h in hours]
x = np.arange(len(hours))

# ── Plot ──
fig, axes = plt.subplots(3, 1, figsize=(12, 10))
fig.suptitle("Dublin Weather Forecast — Next 3 Days\n(Live Data from Open-Meteo API)",
             fontsize=14, fontweight="bold")

# Temperature
axes[0].plot(x, temperature, color="#FF5722", linewidth=2)
axes[0].fill_between(x, temperature, alpha=0.2, color="#FF5722")
axes[0].set_ylabel("Temperature (°C)", fontsize=11)
axes[0].set_title("Temperature", fontsize=12)
axes[0].grid(True, alpha=0.3)
axes[0].axhline(y=np.mean(temperature), color="red",
                linestyle="--", label=f"Average: {np.mean(temperature):.1f}°C")
axes[0].legend()

# Humidity
axes[1].plot(x, humidity, color="#2196F3", linewidth=2)
axes[1].fill_between(x, humidity, alpha=0.2, color="#2196F3")
axes[1].set_ylabel("Humidity (%)", fontsize=11)
axes[1].set_title("Relative Humidity", fontsize=12)
axes[1].grid(True, alpha=0.3)
axes[1].axhline(y=np.mean(humidity), color="blue",
                linestyle="--", label=f"Average: {np.mean(humidity):.1f}%")
axes[1].legend()

# Wind Speed
axes[2].plot(x, wind_speed, color="#4CAF50", linewidth=2)
axes[2].fill_between(x, wind_speed, alpha=0.2, color="#4CAF50")
axes[2].set_ylabel("Wind Speed (km/h)", fontsize=11)
axes[2].set_title("Wind Speed", fontsize=12)
axes[2].grid(True, alpha=0.3)
axes[2].axhline(y=np.mean(wind_speed), color="green",
                linestyle="--", label=f"Average: {np.mean(wind_speed):.1f} km/h")
axes[2].legend()

# X axis labels every 12 hours
tick_positions = x[::12]
tick_labels = [day_labels[i] for i in tick_positions]
for ax in axes:
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=45, fontsize=8)

plt.tight_layout()
plt.savefig("dublin_weather.png", dpi=150)
plt.show()

# ── Print summary ──
print("\n📊 Dublin Weather Summary (Next 3 Days):")
print(f"  🌡️  Temperature: min {min(temperature):.1f}°C  /  max {max(temperature):.1f}°C  /  avg {np.mean(temperature):.1f}°C")
print(f"  💧 Humidity:    min {min(humidity)}%  /  max {max(humidity)}%  /  avg {np.mean(humidity):.1f}%")
print(f"  💨 Wind Speed:  min {min(wind_speed):.1f}  /  max {max(wind_speed):.1f}  /  avg {np.mean(wind_speed):.1f} km/h")
print("\n✅ Chart saved as dublin_weather.png")