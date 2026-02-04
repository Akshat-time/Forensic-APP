
import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, ResponsiveContainer } from 'recharts';
import { AudioFeatures } from '../types';

interface ForensicChartProps {
  features: AudioFeatures;
}

const ForensicChart: React.FC<ForensicChartProps> = ({ features }) => {
  // Normalize values for visualization (0-100 scale)
  const data = [
    { subject: 'Pause Ent.', A: (features.pauseEntropy / 5) * 100, fullMark: 100 },
    { subject: 'Jitter', A: (features.pitchJitter / 5) * 100, fullMark: 100 },
    { subject: 'Shimmer', A: (features.shimmer / 5) * 100, fullMark: 100 },
    { subject: 'Silence Var', A: features.silenceNoiseVariance * 100, fullMark: 100 },
    { subject: 'Prosody Drift', A: (features.prosodyDrift / 10) * 100, fullMark: 100 },
  ];

  return (
    <div className="w-full h-64 md:h-80 bg-slate-900/50 rounded-xl border border-slate-800 p-4">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
          <PolarGrid stroke="#334155" />
          <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 10 }} />
          <Radar
            name="Forensic Profile"
            dataKey="A"
            stroke="#10b981"
            fill="#10b981"
            fillOpacity={0.4}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ForensicChart;
