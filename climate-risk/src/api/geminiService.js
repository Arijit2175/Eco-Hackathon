import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { motion, AnimatePresence } from 'framer-motion';

const generateActionPlanWithGemini = async (city, riskLevels) => {

  const prompt = `Create a simple, personalized daily action plan for a citizen in ${city} based on these climate risks: Flood is ${riskLevels.flood.level}, Heatwave is ${riskLevels.heatwave.level}, Pollution is ${riskLevels.pollution.level}, and Drought is ${riskLevels.drought.level}. Provide 3-5 clear, actionable bullet points using markdown. Keep it brief and easy to understand.`;

  const apiKey = "";

  const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=${apiKey}`;

  const payload = { contents: [{ parts: [{ text: prompt }] }] };

  try {

    const response = await fetch(apiUrl, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });

    if (!response.ok) throw new Error(`Gemini API request failed with status ${response.status}`);

    const result = await response.json();

    if (result.candidates?.[0]?.content?.parts?.[0]) return result.candidates[0].content.parts[0].text;

    else throw new Error("Invalid response structure from Gemini API.");

  } catch (error) { console.error("Gemini API Error:", error); return "Could not generate an action plan at this time."; }

};