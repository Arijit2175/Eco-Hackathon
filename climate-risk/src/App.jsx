import React, { useState } from "react";
import axios from "axios";

function App() {
  const [city, setCity] = useState("");
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://127.0.0.1:8000/predict", {
        features: {
          temperature_c: 30,
          humidity: 60,
          wind_speed_kph: 15,
          pressure_hpa: 1012,
        },
        temperature_sequence: [29, 30, 31, 32, 33],
      });
      setResult(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>🌍 Climate Risk Predictor</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter city name (not used yet)"
          value={city}
          onChange={(e) => setCity(e.target.value)}
        />
        <button type="submit">Predict</button>
      </form>

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h2>Results</h2>
          <p>Predicted Rainfall: {result.predicted_rainfall_mm} mm</p>
          <p>Predicted Temperature: {result.predicted_temperature_c} °C</p>
          <p>Flood Risk: {result.flood_risk}</p>
          <p>Heatwave Risk: {result.heatwave_risk}</p>
          <p>Drought Risk: {result.drought_risk}</p>
        </div>
      )}
    </div>
  );
}

export default App;
