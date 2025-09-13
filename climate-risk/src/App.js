import React, { useState } from "react";
import axios from "axios";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer
} from "recharts";
import "./App.css";

const BACKEND = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";

function App() {
  const [temperature_c, setTemperature] = useState("");
  const [humidity, setHumidity] = useState("");
  const [pressure_hpa, setPressure] = useState("");
  const [wind_speed_kph, setWind] = useState("");
  const [tempSeqText, setTempSeqText] = useState("30,30.5,31");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const parseSeq = (text) =>
    text.split(",").map(s => parseFloat(s.trim())).filter(n => !isNaN(n));

  const handlePredict = async () => {
    setLoading(true);
    setResult(null);
    try {
      const payload = {
        features: {
          temperature_c: parseFloat(temperature_c),
          humidity: parseFloat(humidity),
          pressure_hpa: parseFloat(pressure_hpa),
          wind_speed_kph: parseFloat(wind_speed_kph),
        },
        temperature_sequence: parseSeq(tempSeqText),
      };

      const res = await axios.post(`${BACKEND}/predict`, payload);
      setResult({ ...res.data, temperature_sequence: payload.temperature_sequence });
    } catch (err) {
      console.error(err);
      alert("Prediction failed. Check console.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>🌍 Climate Risk Dashboard</h1>

      <div className="card">
        <label>Temperature (°C)</label>
        <input value={temperature_c} onChange={e => setTemperature(e.target.value)} />

        <label>Humidity (%)</label>
        <input value={humidity} onChange={e => setHumidity(e.target.value)} />

        <label>Pressure (hPa)</label>
        <input value={pressure_hpa} onChange={e => setPressure(e.target.value)} />

        <label>Wind Speed (kph)</label>
        <input value={wind_speed_kph} onChange={e => setWind(e.target.value)} />

        <label>Temperature Sequence (comma-separated)</label>
        <textarea value={tempSeqText} onChange={e => setTempSeqText(e.target.value)} />

        <button onClick={handlePredict} disabled={loading}>
          {loading ? "Predicting..." : "Predict"}
        </button>
      </div>

      {result && (
        <div className="card">
          <h2>Results</h2>
          <div className="results">
            <div className="result-box">
              <h3>🌧 Rainfall</h3>
              <p>{(result.predicted_rainfall_mm ?? 0).toFixed(2)} mm</p>
            </div>
            <div className="result-box">
              <h3>🌡 Temperature</h3>
              <p>{(result.predicted_temperature_c ?? 0).toFixed(2)} °C</p>
            </div>
            <div className="result-box">
              <h3>⚠️ Risks</h3>
              <p>Flood: <b>{result.flood_risk}</b></p>
              <p>Heatwave: <b>{result.heatwave_risk}</b></p>
              <p>Drought: <b>{result.drought_risk}</b></p>
            </div>
          </div>

          <h3>Temperature Sequence</h3>
          <div style={{ width: "100%", height: 220 }}>
            <ResponsiveContainer>
              <LineChart data={(result.temperature_sequence || []).map((t,i)=>({i: i+1, t}))}>
                <XAxis dataKey="i" />
                <YAxis />
                <Tooltip />
                <Line dataKey="t" stroke="#ff0000" dot />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
