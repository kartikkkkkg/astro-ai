import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { useMotionValue, useTransform } from "framer-motion";

interface AspectLineProps {
  planet1: keyof typeof PLANETARY_DATA;
  planet2: keyof typeof PLANETARY_DATA;
  aspect: AspectType;
  orb: number; // degrees of separation from exact aspect
  exact: boolean;
  className?: string;
}

// Planetary data would normally come from chart calculations
// For now, we'll define a basic structure
const PLANETARY_DATA = {
  Sun: { longitude: 0 },
  Moon: { longitude: 0 },
  Mars: { longitude: 0 },
  Mercury: { longitude: 0 },
  Jupiter: { longitude: 0 },
  Venus: { longitude: 0 },
  Saturn: { longitude: 0 },
  Rahu: { longitude: 0 },
  Ketu: { longitude: 0 },
};

export enum AspectType {
  Conjunction = 0,
  Sextile = 60,
  Square = 90,
  Trine = 120,
  Opposition = 180,
}

const ASPECT_COLORS: Record<AspectType, string> = {
  [AspectType.Conjunction]: "hsl(var(--observatory-primary))",
  [AspectType.Sextile]: "hsl(var(--observatory-accent))",
  [AspectType.Square]: "hsl(var(--observatory-destructive))",
  [AspectType.Trine]: "hsl(var(--observatory-cyan))",
  [AspectType.Opposition]: "hsl(var(--observatory-primary))",
};

const ASPECT_STYLES: Record<AspectType, string> = {
  [AspectType.Conjunction]: "solid",
  [AspectType.Sextile]: "dashed",
  [AspectType.Square]: "dotted",
  [AspectType.Trine]: "solid",
  [AspectType.Opposition]: "dashed",
};

export function AspectLine({
  planet1,
  planet2,
  aspect,
  orb,
  exact,
  className,
}: AspectLineProps) {
  // In a real implementation, we'd get actual longitudes from planetary data
  // For now, we'll use placeholder values
  const lon1 = PLANETARY_DATA[planet1].longitude || 0;
  const lon2 = PLANETARY_DATA[planet2].longitude || 0;

  // Calculate the actual angle between planets (simplified)
  const angle1 = (lon1 * Math.PI) / 180;
  const angle2 = (lon2 * Math.PI) / 180;

  const radius = 150; // Chart radius
  const cx = radius;
  const cy = radius;

  const x1 = radius * Math.cos(angle1) + radius;
  const y1 = radius * Math.sin(angle1) + radius;
  const x2 = radius * Math.cos(angle2) + radius;
  const y2 = radius * Math.sin(angle2) + radius;

  // Motion value for pulsing effect on exact aspects
  const pulse = useMotionValue(1);

  // Pulse exact aspects slightly
  if (exact) {
    // In a real implementation, we'd use useSpring or similar for animation
    // For now, we'll just note that exact aspects should pulse
  }

  return (
    <path
      d={`M ${x1},${y1} L ${x2},${y2}`}
      className={twMerge(
        "transition-opacity duration-300 hover:opacity-100",
        className
      )}
      stroke={ASPECT_COLORS[aspect]}
      strokeWidth={exact ? "2" : "1.5"}
      strokeDasharray={ASPECT_STYLES[aspect] === "dashed" ? "4,2" :
                      ASPECT_STYLES[aspect] === "dotted" ? "2,2" :
                      "none"}
      opacity={exact ? 0.8 : 0.6}
      style={{
        // In a full implementation, we'd animate the pulse here
      }}
    />
  );
}