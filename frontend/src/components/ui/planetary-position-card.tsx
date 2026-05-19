import { className } from 'klass';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Loader2, Moon, Sparkles } from 'lucide-react';

// Zodiac signs symbols
const ZODIAC_SYMBOLS: Record<string, string> = {
  Aries: '♈',
  Taurus: '♉',
  Gemini: '♊',
  Cancer: '♋',
  Leo: '♌',
  Virgo: '♍',
  Libra: '♎',
  Scorpio: '♏',
  Sagittarius: '♐',
  Capricorn: '♑',
  Aquarius: '♒',
  Pisces: '♓',
};

// Planet symbols
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

// Format degree to DMS (Degree-Minute-Second) or just decimal degrees
function formatDegree(degree: number): string {
  const degrees = Math.floor(degree);
  const minutesFloat = (degree - degrees) * 60;
  const minutes = Math.floor(minutesFloat);
  const seconds = Math.floor((minutesFloat - minutes) * 60);

  // Return as DMS: °'"
  return `${degrees}°${minutes}'${seconds}"`;
}

interface PlanetaryPositionCardProps {
  planet: {
    planet: string;
    longitude: number;
    latitude: number;
    speed: number;
    sign: string;
    house: string;
    is_retrograde: boolean;
  };
}

export function PlanetaryPositionCard({ planet }: PlanetaryPositionCardProps) {
  const planetSymbol = PLANET_SYMBOLS[planet.planet] || '?';
  const zodiacSymbol = ZODIAC_SYMBOLS[planet.sign] || '?';

  // Determine if retrograde
  const isRetrograde = planet.is_retrograde;
  const speedText = isRetrograde
    ? `-${Math.abs(planet.speed).toFixed(3)}`
    : `+${planet.speed.toFixed(3)}`;

  return (
    <Card className="glass hover:glass-lg transition-all duration-300 border border-[hsl(var(--border))/0.2]">
      <CardHeader className="pb-3">
        <div className="flex flex-col items-center text-center">
          <div className="text-2xl mb-2">
            {planetSymbol}
          </div>
          <CardTitle className="text-[hsl(var(--foreground))] font-semibold">
            {planet.planet}
          </CardTitle>
        </div>
      </CardHeader>
      <CardContent className="space-y-2">
        <div className="flex justify-between text-[hsl(var(--foreground-muted))] text-sm">
          <span>Sign</span>
          <span>{zodiacSymbol} {planet.sign}</span>
        </div>

        <div className="flex justify-between text-[hsl(var(--foreground-muted))] text-sm">
          <span>Position</span>
          <span>{formatDegree(planet.longitude)}</span>
        </div>

        <div className="flex justify-between text-[hsl(var(--foreground-muted))] text-sm">
          <span>House</span>
          <span>{planet.house}</span>
        </div>

        <div className="flex justify-between text-[hsl(var(--foreground-muted))] text-sm">
          <span>Speed</span>
          <span className={isRetrograde ? 'text-[hsl(var(--destructive))]' : 'text-[hsl(var(--accent))]'}>
            {speedText}
          </span>
        </div>

        {isRetrograde && (
          <div className="flex items-center space-x-2 text-[hsl(var(--destructive))] text-xs">
            <Moon className="h-3 w-3" />
            <span>Retrograde</span>
          </div>
        )}
      </CardContent>
    </Card>
  );
}