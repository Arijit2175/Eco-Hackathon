import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { motion, AnimatePresence } from 'framer-motion';

const getClimateData = async ({ city, lat, lon }) => {

  const OPENWEATHER_API_KEY = process.env.OPENWEATHER_API_KEY;

  let latitude = lat, longitude = lon, cityName = city;

  try {

    if (city && !lat) {

      const geoResponse = await fetch(`https://api.openweathermap.org/geo/1.0/direct?q=${city}&limit=1&appid=${OPENWEATHER_API_KEY}`);

      if (!geoResponse.ok) throw new Error(`Could not find location: ${city}`);

      const geoData = await geoResponse.json();

      if (geoData.length === 0) throw new Error(`Could not find location: ${city}. Please check spelling.`);

      latitude = geoData[0].lat; longitude = geoData[0].lon;

    } else if (lat && lon && !city) {

      const reverseGeoResponse = await fetch(`https://api.openweathermap.org/geo/1.0/reverse?lat=${lat}&lon=${lon}&limit=1&appid=${OPENWEATHER_API_KEY}`);

      const reverseGeoData = await reverseGeoResponse.json();

      if (reverseGeoData.length > 0) cityName = reverseGeoData[0].name;

    }

    const weatherResponse = await fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${OPENWEATHER_API_KEY}&units=metric`);

    const weatherData = await weatherResponse.json();

    const aqiResponse = await fetch(`https://api.openweathermap.org/data/2.5/air_pollution?lat=${latitude}&lon=${longitude}&appid=${OPENWEATHER_API_KEY}`);

    const aqiData = await aqiResponse.json();

    const forecastResponse = await fetch(`https://api.openweathermap.org/data/2.5/forecast?lat=${latitude}&lon=${longitude}&appid=${OPENWEATHER_API_KEY}&units=metric`);

    const forecastData = await forecastResponse.json();

    const formattedForecast = forecastData.list.map(item => ({ time: new Date(item.dt * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), temp: item.main.temp, humidity: item.main.humidity })).slice(0, 8);

    return { ...weatherData, name: cityName || weatherData.name, aqi: aqiData.list[0].main.aqi, forecast: formattedForecast };

  } catch (error) { console.error("API Fetch Error:", error.message); throw error; }

};

export { getClimateData };