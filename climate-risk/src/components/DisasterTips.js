import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { motion, AnimatePresence } from 'framer-motion';

const DisasterTips = () => {

  const tips = { Floods: ["Keep an emergency kit ready.", "Avoid low-lying areas.", "Prepare sandbags."], Heatwaves: ["Stay hydrated.", "Avoid peak sun hours.", "Use cooling centers."], Pollution: ["Wear an N95 mask.", "Avoid outdoor activity.", "Use air purifiers."], Drought: ["Store water safely.", "Practice water conservation.", "Plan irrigation wisely."] };

  return <div className="disaster-tips"><h2>Disaster Management Tips</h2><div className="tips-grid">{Object.entries(tips).map(([category, tipList]) => <div key={category} className="tip-category"><h3>{category}</h3><div className="tip-list">{tipList.map((tip, index) => <p key={index} className="tip-item"><TipIcon /><span>{tip}</span></p>)}</div></div>)}</div></div>;

};

export default DisasterTips;