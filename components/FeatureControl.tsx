
import React from 'react';

interface FeatureControlProps {
  label: string;
  value: number;
  min: number;
  max: number;
  step: number;
  unit?: string;
  onChange: (val: number) => void;
}

const FeatureControl: React.FC<FeatureControlProps> = ({ label, value, min, max, step, unit, onChange }) => {
  return (
    <div className="flex flex-col gap-2 p-3 bg-slate-900 rounded-lg border border-slate-800">
      <div className="flex justify-between items-center text-xs font-semibold uppercase tracking-wider text-slate-400">
        <span>{label}</span>
        <span className="text-emerald-400">{value}{unit}</span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        className="w-full h-1.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-emerald-500"
      />
    </div>
  );
};

export default FeatureControl;
