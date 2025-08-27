import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { motion, AnimatePresence } from 'framer-motion';

const RiskCard = ({ icon, title, risk, details }) => {

  const riskClass = { Low: 'risk-low', Medium: 'risk-medium', High: 'risk-high' };

  return <motion.div initial={{ opacity: 0, y: 50 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }} className={`risk-card ${riskClass[risk]}`}><div className="risk-card-header"><h3>{title}</h3>{icon}</div><div className="risk-card-body"><p>{risk}</p><p>{details}</p></div></motion.div>;
};