import { ChartBase } from '@/components/primitives/ChartBase';
import { PlanetaryGlyph } from '@/components/primitives/PlanetaryGlyph';
import { HouseRenderer } from '@/components/primitives/HouseRenderer';
import { AspectLine } from '@/components/primitives/AspectLine';
import { ChartTooltip } from '@/components/primitives/ChartTooltip';
import { useMotionValue, useTransform } from 'framer-motion';
import { useEffect, useState } from 'react';

interface D1ChartProps {
  chartData: {
    planetary_positions: Array<{
      planet: string;
      longitude: number;
      latitude: number;
      speed: number;
      sign: string;
      house: string;
      is_retrograde: boolean;
    }>;
    house_cusps: Array<{
      house: string;
      longitude: number;
      sign: string;
    }>;
    aspects: Array<{
      planet1: string;
      planet2: string;
      aspect: string;
      orb: number;
      exact: boolean;
    }>;
  };
  className?: string;
}

export function D1Chart({ chartData, className }: D1ChartProps) {
  const [isAnimating, setIsAnimating] = useState(false);
  const chartProgress = useMotionValue(0);

  // Animate chart materialization
  useEffect(() => {
    setIsAnimating(true);
    // In a full implementation, we'd animate this over time
    chartProgress.set(1);
  }, [chartData, chartProgress]);

  // Zodiac sign positions (0-360 degrees)
  const ZODIAC_SIGNS: Record<string, { start: number; end: number; name: string }> = {
    Aries: { start: 0, end: 30, name: 'Aries' },
    Taurus: { start: 30, end: 60, name: 'Taurus' },
    Gemini: { start: 60, end: 90, name: 'Gemini' },
    Cancer: { start: 90, end: 120, name: 'Cancer' },
    Leo: { start: 120, end: 150, name: 'Leo' },
    Virgo: { start: 150, end: 180, name: 'Virgo' },
    Libra: { start: 180, end: 210, name: 'Libra' },
    Scorpio: { start: 210, end: 240, name: 'Scorpio' },
    Sagittarius: { start: 240, end: 270, name: 'Sagittarius' },
    Capricorn: { start: 270, end: 300, name: 'Capricorn' },
    Aquarius: { start: 300, end: 330, name: 'Aquarius' },
    Pisces: { start: 330, end: 360, name: 'Pisces' },
  };

  // Planet to symbol mapping
  const PLANET_SYMBOLS: Record<string, string> = {
    Sun: '☉',
    Moon: '☽',
    Mars: '♂',
    Mercury: '☿',
    Jupiter: '♃',
    Venus: '♀',
    Saturn: '♄',
    Rahu: '☊',
    Ketu: '☋',
  };

  return (
    <ChartBase className={`${className} hover:glass-lg transition-all duration-300`}>
      {/* Outer glow effect */}
      <circle
        cx="200"
        cy="200"
        r="190"
        className="fill-none stroke-[hsl(var(--accent))]/10 stroke-2"
      />

      {/* Chart background circle with glass effect */}
      <circle
        cx="200"
        cy="200"
        r="180"
        className="fill-[hsl(var(--background))/10] stroke-[hsl(var(--border))]/20 stroke-1"
      />

      {/* Nebula background effect */}
      <path
        d="M 200,200 m -180,0 a 180,180 0 1,0 360,0 a 180,180 0 1,0 -360,0"
        className="fill-[hsl(var(--accent))/0.02] stroke-none"
      />

      {/* Zodiac band (outer ring) with enhanced styling */}
      <path
        d="M 200,200 m -180,0 a 180,180 0 1,0 360,0 a 180,180 0 1,0 -360,0"
        className="fill-none stroke-[hsl(var(--border))]/30 stroke-2"
      />

      {/* Inner decorative ring */}
      <path
        d="M 200,200 m -150,0 a 150,150 0 1,0 300,0 a 150,150 0 1,0 -300,0"
        className="fill-none stroke-[hsl(var(--border))]/10 stroke-1"
      />

      {/* Zodiac sign labels with enhanced typography */}
      {Object.values(ZODIAC_SIGNS).map((sign) => {
        const angle = ((sign.start + sign.end) / 2 * Math.PI) / 180;
        const radius = 230;
        const x = radius * Math.cos(angle) + 200;
        const y = radius * Math.sin(angle) + 200;

        return (
          <text
            key={sign.name}
            x={x}
            y={y}
            textAnchor="middle"
            dominantBaseline="middle"
            className="text-sm font-medium text-[hsl(var(--foreground-muted))]/70"
          >
            {sign.name.slice(0, 3)}
          </text>
        );
      })}

      {/* Decorative zodiac dots */}
      {Object.values(ZODIAC_SIGNS).map((sign, index) => {
        const angle = (sign.start * Math.PI) / 180;
        const radius = 190;
        const x = radius * Math.cos(angle) + 200;
        const y = radius * Math.sin(angle) + 200;

        return (
          <circle
            key={`${sign.name}-dot`}
            cx={x}
            cy={y}
            r="2"
            className="fill-[hsl(var(--accent))]/50"
          />
        );
      })}

      {/* House cusps with enhanced styling */}
      {chartData.house_cusps.map((house) => (
        <HouseRenderer
          key={house.house}
          houseNumber={parseInt(house.house)}
          longitude={house.longitude}
          size={14}
          className="transition-transform duration-300"
        />
      ))}

      {/* Aspect lines with glow effect */}
      {chartData.aspects.map((aspect) => {
        // Find the planetary data for aspect lines
        const planet1Data = chartData.planetary_positions.find(
          p => p.planet === aspect.planet1
        );
        const planet2Data = chartData.planetary_positions.find(
          p => p.planet === aspect.planet2
        );

        if (planet1Data && planet2Data) {
          return (
            <AspectLine
              key={`${aspect.planet1}-${aspect.planet2}-${aspect.aspect}`}
              planet1={planet1Data.planet as keyof typeof PLANETARY_DATA}
              planet2={planet2Data.planet as keyof typeof PLANETARY_DATA}
              aspect={AspectType[aspect.aspect as keyof typeof AspectType] || AspectType.Conjunction}
              orb={aspect.orb}
              exact={aspect.exact}
              className="transition-all duration-300 hover:stroke-[hsl(var(--accent))]/50"
            />
          );
        }
        return null;
      }).filter(Boolean)}

      {/* Planetary glyphs with enhanced animations */}
      {chartData.planetary_positions.map((planet) => (
        <PlanetaryGlyph
          key={planet.planet}
          planet={planet.planet as keyof typeof PLANETARY_SYMBOLS}
          longitude={planet.longitude}
          latitude={planet.latitude}
          speed={planet.speed}
          isRetrograde={planet.is_retrograde}
          size={24}
          className="
            transition-all duration-400
            hover:scale-110
            hover:glow-lg
            [&:active]:scale-105
          "
        />
      ))}

      {/* Enhanced center point with cosmic effect */}
      <circle
        cx="200"
        cy="200"
        r="6"
        className="
          fill-[hsl(var(--accent))]
          animate-[pulse-slow_3s_ease-in-out_infinite]
        "
      />

      {/* Inner decorative circle */}
      <circle
        cx="200"
        cy="200"
        r="8"
        className="fill-none stroke-[hsl(var(--accent))]/20 stroke-1"
      />
    </ChartBase>
  );
}