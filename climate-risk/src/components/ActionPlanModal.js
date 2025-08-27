import React from "react";

const ActionPlanModal = ({ plan, city, onClose, isLoading }) => {

  const formatPlan = (text) => text.split('\n').map((line, i) => line.startsWith('* ') ? <li key={i}><span>•</span>{line.substring(2)}</li> : <p key={i}>{line}</p>);

  return <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="modal-overlay" onClick={onClose}><motion.div initial={{ scale: 0.9 }} animate={{ scale: 1 }} exit={{ scale: 0.9 }} className="modal-content" onClick={e => e.stopPropagation()}><h2>✨ AI Action Plan for {city}</h2>{isLoading ? <div><p>Generating your personalized plan...</p></div> : <div className="modal-body"><ul>{formatPlan(plan)}</ul></div>}<button onClick={onClose} className="modal-close-button">Close</button></motion.div></motion.div>;

};