import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { useMotionValue, useTransform, useSpring } from "framer-motion";

interface PlanetaryGlyphProps {
  planet: keyof typeof PLANETARY_SYMBOLS;
  longitude: number; // 0-360
  latitude?: number; // Not used in 2D chart, but kept for 3D possibility
  speed?: number;
  isRetrograde: boolean;
  size?: number;
  className?: string;
}

const PLANETARY_SYMBOLS: Record<string, string> = {
  Sun: "☉",
  Moon: "☽",
  Mars: "♂",
  Mercury: "☿",
  Jupiter: "♃",
  Venus: "♀",
  Saturn: "♄",
  Rahu: "☊", // North Node
  Ketu: "☋", // South Node
};

export function PlanetaryGlyph({
  planet,
  longitude,
  latitude = 0,
  speed = 0,
  isRetrograde = false,
  size = 24,
  className,
}: PlanetaryGlyphProps) {
  // Convert longitude (0-360) to radians for circular positioning
  const angle = (longitude * Math.PI) / 180;
  const radius = 150; // Fixed radius for the chart circle (adjustable via ChartBase size)
  const x = radius * Math.cos(angle) + radius; // Center at (radius, radius)
  const y = radius * Math.sin(angle) + radius;

  // Motion values for hover and animation
  const scale = useMotionValue(1);
  const scaleY = useMotionValue(1);
  const rotate = useMotionValue(0);

  // Retrograde planets have a slight oscillation
  useEffect(() => {
    if (isRetrograde) {
      const spring = useSpring({ scale: 1, damping: 20 });
      spring.start();
    }
  }, [isRetrograde]);

  return (
    <g
      transform={`translate(${x}, ${y})`}
      className={twMerge(
        "cursor-pointer transition-transform duration-300",
        className
      )}
      onMouseEnter={() => (scale.current = 1.2)}
      onMouseLeave={() => (scale.current = 1)}
    >
      {/* Retrograde indicator */}
      {isRetrograde && (
        <circle
          cx="0"
          cy="0"
          r={size * 0.4}
          className="opacity-20 hover:opacity-40 transition-opacity duration-300"
          fill="hsl(var(--observatory-cyan))"
        />
      )}

      {/* Glyph background (subtle circle) */}
      <circle
        cx="0"
        cy="0"
        r={size * 0.3}
        className="opacity-10 hover:opacity-20 transition-opacity duration-300"
        fill="hsl(var(--observatory-cyan))"
      />

      {/* The planetary symbol */}
      <text
        x="0"
        y="{size * 0.1}"
        textAnchor="middle"
        className={twMerge(
          "select-none pointer-events-none",
          size > 20 ? "text-xl" : "text-lg",
          "text-foreground"
        )}
        style={{
          transform: `scale(${scale})`,
          transformOrigin: "center",
        }}
      >
        {PLANETARY_SYMBOLS[planet]}
      </text>

      {/* Optional: Speed indicator (for advanced users) */}
      {speed !== 0 && (
        <text
          x="0"
          y="{size * 0.5}"
          textAnchor="middle"
          className="text-xs text-muted-foreground opacity-50"
        >
          {speed.toFixed(2)}°/d
        </text>
      )}
    </g>
  );
}