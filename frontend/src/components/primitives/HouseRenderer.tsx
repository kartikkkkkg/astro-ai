import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

interface HouseRendererProps {
  houseNumber: number; // 1-12
  longitude: number; // 0-360, the cusp longitude
  size?: number;
  className?: string;
}

export function HouseRenderer({
  houseNumber,
  longitude,
  size = 12,
  className,
}: HouseRendererProps) {
  // Convert longitude (0-360) to radians for circular positioning
  const angle = (longitude * Math.PI) / 180;
  const radius = 150; // Fixed radius for the chart circle (adjustable via ChartBase size)
  const x = radius * Math.cos(angle) + radius; // Center at (radius, radius)
  const y = radius * Math.sin(angle) + radius;

  // Calculate the label position (slightly outside the circle)
  const labelRadius = radius + 20;
  const labelX = labelRadius * Math.cos(angle) + labelRadius;
  const labelY = labelRadius * Math.sin(angle) + labelRadius;

  return (
    <g className={twMerge("opacity-60 hover:opacity-100 transition-opacity duration-300", className)}>
      {/* House cusp line (from center to edge) */}
      <line
        x1={radius}
        y1={radius}
        x2={x}
        y2={y}
        className="stroke-[hsl(var(--observatory-border))] stroke-1"
      />

      {/* House cusp point (dot) */}
      <circle
        cx={x}
        cy={y}
        r={size * 0.15}
        className="fill-[hsl(var(--observatory-cyan))]"
      />

      {/* House number label */}
      <text
        x={labelX}
        y={labelY}
        textAnchor="middle"
        dominantBaseline="middle"
        className={twMerge(
          "text-xs text-muted-foreground",
          "pointer-events-none"
        )}
      >
        {houseNumber}
      </text>
    </g>
  );
}