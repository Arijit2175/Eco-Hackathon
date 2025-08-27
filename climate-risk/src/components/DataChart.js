import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { motion, AnimatePresence } from 'framer-motion';

const DataChart = ({ data, dataKey, color, title }) => (

  <div className="data-chart"><h3>{title}</h3><ResponsiveContainer width="100%" height={200}><LineChart data={data}><CartesianGrid strokeDasharray="3 3" stroke="#ccc" /><XAxis dataKey="time" stroke="#555" /><YAxis stroke="#555" /><Tooltip contentStyle={{ backgroundColor: 'rgba(255, 255, 255, 0.8)', border: 'none', borderRadius: '10px' }} /><Legend /><Line type="monotone" dataKey={dataKey} stroke={color} strokeWidth={3} dot={{ r: 5 }} activeDot={{ r: 8 }} /></LineChart></ResponsiveContainer></div>

);