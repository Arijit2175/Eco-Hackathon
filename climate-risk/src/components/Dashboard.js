import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { motion, AnimatePresence } from 'framer-motion';

const Dashboard = () => {

  const [city, setCity] = useState('Hyderabad');

  const [currentCity, setCurrentCity] = useState('Hyderabad');

  const [climateData, setClimateData] = useState(null);

  const [riskLevels, setRiskLevels] = useState(null);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState(null);

  const [showActionPlan, setShowActionPlan] = useState(false);

  const [actionPlan, setActionPlan] = useState("");

  const [isPlanLoading, setIsPlanLoading] = useState(false);

  const fetchData = async (targetCity) => {

    setLoading(true); setError(null);

    try {

      const data = await getClimateData({city: targetCity});

      setClimateData(data);

      setRiskLevels(predictRisk(data));

      setCurrentCity(data.name);

    } catch (err) {

      setError(err.message);

      setClimateData(null);

      setRiskLevels(null);

    } finally {

      setLoading(false);

    }

  };

  useEffect(() => { fetchData(city); }, []);

  const handleSearch = (e) => { e.preventDefault(); if (city.trim()) fetchData(city); };

  const handleGeneratePlan = async () => {

    if (!riskLevels) return;

    setShowActionPlan(true); setIsPlanLoading(true);

    const planText = await generateActionPlanWithGemini(currentCity, riskLevels);

    setActionPlan(planText); setIsPlanLoading(false);

  };

  return (

    <div className="dashboard">

      <form onSubmit={handleSearch} className="search-form">

        <input type="text" value={city} onChange={(e) => setCity(e.target.value)} placeholder="Search for a city..." className="search-input" />

        <button type="submit" className="search-button" disabled={loading}>{loading ? 'Searching...' : 'Search'}</button>

      </form>

      <AnimatePresence>

        {loading && <motion.div key="loader" exit={{ opacity: 0 }}><p>Loading climate data...</p></motion.div>}

        {error && <motion.div key="error" initial={{opacity: 0}} animate={{opacity: 1}} exit={{ opacity: 0 }} className="error-message"><strong>Error: </strong><span>{error}</span></motion.div>}

        {climateData && riskLevels && !loading && (

          <motion.div key="data" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>

            <div className="header-with-button">

              <h2>Climate Risk for {currentCity}</h2>

              <button onClick={handleGeneratePlan} className="ai-plan-button"><SparklesIcon /> AI Action Plan</button>

            </div>

            <div className="risk-grid">

              <RiskCard icon={<FloodIcon />} title="Flood" risk={riskLevels.flood.level} details={riskLevels.flood.details} />

              <RiskCard icon={<HeatwaveIcon />} title="Heatwave" risk={riskLevels.heatwave.level} details={riskLevels.heatwave.details} />

              <RiskCard icon={<PollutionIcon />} title="Pollution" risk={riskLevels.pollution.level} details={riskLevels.pollution.details} />

              <RiskCard icon={<DroughtIcon />} title="Drought" risk={riskLevels.drought.level} details={riskLevels.drought.details} />

            </div>

            <div className="charts-grid">

              <DataChart data={climateData.forecast} dataKey="temp" color="#ff7300" title="Temperature Forecast (°C)" />

              <DataChart data={climateData.forecast} dataKey="humidity" color="#387908" title="Humidity Forecast (%)" />

            </div>

            <DisasterTips />

          </motion.div>

        )}

      </AnimatePresence>

      <AnimatePresence>

        {showActionPlan && <ActionPlanModal plan={actionPlan} city={currentCity} onClose={() => setShowActionPlan(false)} isLoading={isPlanLoading} />}

      </AnimatePresence>

    </div>

  );

};

export default Dashboard;