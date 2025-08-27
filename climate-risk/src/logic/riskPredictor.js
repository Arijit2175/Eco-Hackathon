import React from "react";

const predictRisk = (weatherData) => {

  const { main, weather, rain, aqi } = weatherData;

  let floodRisk = 'Low', heatwaveRisk = 'Low', pollutionRisk = 'Low', droughtRisk = 'Low';

  if (rain && rain['1h'] > 10) floodRisk = 'Medium';

  if (rain && rain['1h'] > 25) floodRisk = 'High';

  if (weather[0].main === 'Thunderstorm') floodRisk = 'High';

  if (main.temp > 35) heatwaveRisk = 'Medium';

  if (main.temp > 42) heatwaveRisk = 'High';

  if (aqi >= 2) pollutionRisk = 'Medium';

  if (aqi >= 4) pollutionRisk = 'High';

  if (main.humidity < 20 && main.temp > 30 && (!rain || rain['1h'] === 0)) droughtRisk = 'Medium';

  if (main.humidity < 15 && main.temp > 35 && (!rain || rain['1h'] === 0)) droughtRisk = 'High';

  return { flood: { level: floodRisk, details: `Rainfall: ${rain ? rain['1h'] : 0} mm/h` }, heatwave: { level: heatwaveRisk, details: `Temp: ${main.temp}°C` }, pollution: { level: pollutionRisk, details: `AQI Level: ${aqi}` }, drought: { level: droughtRisk, details: `Humidity: ${main.humidity}%` } };

};