import { ChartBase } from '@/components/primitives/ChartBase';
import { PlanetaryGlyph } from '@/components/primitives/PlanetaryGlyph';
import { HouseRenderer } from '@/components/primitives/HouseRenderer';
import { AspectLine } from '@/components/primitives/AspectLine';
import { ChartTooltip } from '@/components/primitives/ChartTooltip';
import { useEffect, useState } from 'react';

interface D9ChartProps {
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

export function D9Chart({ chartData, className }: D9ChartProps) {
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
    <ChartBase className={className}>
      {/* Chart background circle */}
      <circle
        cx="200"
        cy="200"
        r="180"
        className="fill-[hsl(var(--observatory-background))/20]"
      />

      {/* Zodiac band (outer ring) */}
      <path
        d="M 200,200 m -180,0 a 180,180 0 1,0 360,0 a 180,180 0 1,0 -360,0"
        className="fill-none stroke-[hsl(var(--observatory-border))]/20 stroke-1"
      />

      {/* Zodiac sign labels */}
      {Object.values(ZODIAC_SIGNS).map((sign) => {
        const angle = ((sign.start + sign.end) / 2 * Math.PI) / 180;
        const radius = 220;
        const x = radius * Math.cos(angle) + 200;
        const y = radius * Math.sin(angle) + 200;

        return (
          <text
            key={sign.name}
            x={x}
            y={y}
            textAnchor="middle"
            dominantBaseline="middle"
            className="text-xs text-[hsl(var(--observatory-foreground-muted))] opacity-60"
          >
            {sign.name.slice(0, 3)}
          </text>
        );
      })}

      {/* House cusps */}
      {chartData.house_cusps.map((house) => (
        <HouseRenderer
          key={house.house}
          houseNumber={parseInt(house.house)}
          longitude={house.longitude}
          size={12}
        />
      ))}

      {/* Aspect lines */}
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
              planet1={planet1Data.planet as keyof typeof PLANETARY_SYMBOLS}
              planet2={planet2Data.planet as keyof typeof PLANETARY_SYMBOLS}
              aspect={AspectType[aspect.aspect as keyof typeof AspectType] || AspectType.Conjunction}
              orb={aspect.orb}
              exact={aspect.exact}
            />
          );
        }
        return null;
      }).filter(Boolean)}

      {/* Planetary glyphs (D9 chart - different positioning) */}
      {chartData.planetary_positions.map((planet) => (
        <PlanetaryGlyph
          key={planet.planet}
          planet={planet.planet as keyof typeof PLANETARY_SYMBOLS}
          longitude={planet.longitude}
          latitude={planet.latitude}
          speed={planet.speed}
          isRetrograde={planet.is_retrograde}
          size={18}
          className="transition-transform duration-300"
        />
      ))}

      {/* Center point */}
      <circle
        cx="200"
        cy="200"
        r="3"
        className="fill-[hsl(var(--observatory-cyan))] opacity-60"
      />
    </ChartBase>
  );
}