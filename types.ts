
export interface AudioFeatures {
  pauseEntropy: number;
  pitchJitter: number;
  shimmer: number;
  silenceNoiseVariance: number;
  prosodyDrift: number;
  language: string;
}

export enum Classification {
  AUTHENTIC = 'Authentic / Human',
  SYNTHETIC = 'Synthetic / Generated',
  ALTERED = 'Altered / Edited'
}

export interface ExplanationResult {
  text: string;
  loading: boolean;
  error?: string;
}
