// Chart types matching the backend API

export interface PlanetaryPosition {
  planet: string;
  longitude: number; // 0-360 degrees
  latitude: number; // Usually 0 for 2D chart
  speed: number; // Daily motion in degrees
  sign: string; // Zodiac sign
  house: string; // House number as string
  is_retrograde: boolean;
}

export interface HouseCusp {
  house: string; // House number as string
  longitude: number; // 0-360 degrees
  sign: string; // Zodiac sign
}

export interface AspectInfo {
  planet1: string;
  planet2: string;
  aspect: string; // Conjunction, Sextile, Square, Trine, Opposition
  orb: number; // Degrees of separation from exact aspect
  exact: boolean; // Whether aspect is exact
}

export interface ChartBase {
  birth_date: string; // YYYY-MM-DD
  birth_time: string; // HH:MM
  birth_latitude: number;
  birth_longitude: number;
  timezone: string; // +/-HH:MM
  ayanamsa?: string;
  planetary_positions: PlanetaryPosition[];
  house_cusps: HouseCusp[];
  aspects: AspectInfo[];
  // Divisional charts and other advanced data would go here
  [key: string]: any; // Allow for extension
}

export interface ChartResponse extends ChartBase {
  id: number;
  user_id: number;
  chart_type: 'd1' | 'd9';
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
  // Additional computed or stored fields
  divisional_data?: Record<string, any>;
}