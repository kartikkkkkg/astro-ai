import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { useGenerateD1Chart, useGenerateD9Chart } from '@/lib/hooks/useCharts';
import { D1Chart } from '@/components/charts/D1Chart';
import { D9Chart } from '@/components/charts/D9Chart';
import { Loader2, Sparkles, Moon, MapPin } from 'lucide-react';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { framerMotion } from '@/lib/utils/framerMotion';
import { PlanetaryPositionCard } from '@/components/ui/planetary-position-card';
import type { ChartResponse } from '@/types/chart';

interface ChartWidgetProps {
  chartType: 'd1' | 'd9';
  defaultData?: {
    birth_date: string;
    birth_time: string;
    birth_latitude: number;
    birth_longitude: number;
    timezone: string;
  };
}

export function ChartWidget({ chartType, defaultData }: ChartWidgetProps) {
  const [birthData, setBirthData] = useState<{
    birth_date: string;
    birth_time: string;
    birth_latitude: number;
    birth_longitude: number;
    timezone: string;
  }>({
    birth_date: '1990-08-15',
    birth_time: '14:30',
    birth_latitude: 19.0760,
    birth_longitude: 72.8777,
    timezone: '+05:30',
    ...(defaultData || {}),
  });

  const [chartResult, setChartResult] = useState<ChartResponse | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { mutate: generateD1Chart, isPending: isD1Pending } = useGenerateD1Chart();
  const { mutate: generateD9Chart, isPending: isD9Pending } = useGenerateD9Chart();

  const handleGenerateChart = () => {
    setIsGenerating(true);
    setError(null);
    setChartResult(null);

    const request = {
      chart_type: chartType,
      birth_date: birthData.birth_date,
      birth_time: birthData.birth_time,
      birth_latitude: birthData.birth_latitude,
      birth_longitude: birthData.birth_longitude,
      timezone: birthData.timezone,
    };

    if (chartType === 'd1') {
      generateD1Chart(request, {
        onSuccess: (data) => {
          setChartResult(data);
          setIsGenerating(false);
        },
        onError: (err) => {
          setError(err.message || 'Failed to generate chart');
          setIsGenerating(false);
        },
      });
    } else {
      generateD9Chart(request, {
        onSuccess: (data) => {
          setChartResult(data);
          setIsGenerating(false);
        },
        onError: (err) => {
          setError(err.message || 'Failed to generate chart');
          setIsGenerating(false);
        },
      });
    }
  };

  return (
    <TooltipProvider>
      <div className="space-y-6">
        <Card className="glass hover:glass-lg transition-all duration-300 border border-[hsl(var(--border))/0.2]">
          <CardHeader className="pb-4">
            <CardTitle className="text-2xl font-display text-[hsl(var(--foreground))]">
              {chartType === 'd1' ? 'D1 Natal Chart' : 'D9 Navamsha Chart'}
            </CardTitle>
            <CardDescription className="text-[hsl(var(--foreground-muted))]">
              Enter birth details to calculate your astrological chart
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <form className="space-y-6" onSubmit={(e) => {
              e.preventDefault();
              handleGenerateChart();
            }}>
              <div className="space-y-4">
                <label htmlFor="birthDate" className="flex items-center space-x-2 text-sm font-medium text-[hsl(var(--foreground-muted))]">
                  <MapPin className="h-4 w-4 text-[hsl(var(--accent))]" />
                  Birth Date
                </label>
                <input
                  id="birthDate"
                  type="date"
                  value={birthData.birth_date}
                  onChange={(e) => setBirthData(prev => ({ ...prev, birth_date: e.target.value }))}
                  className="w-full px-4 py-3 border border-[hsl(var(--border))/0.3] rounded-lg bg-[hsl(var(--background))/0.2] text-[hsl(var(--foreground))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--accent))] focus:border-[hsl(var(--accent))] transition-all duration-200"
                />
              </div>

              <div className="space-y-4">
                <label htmlFor="birthTime" className="flex items-center space-x-2 text-sm font-medium text-[hsl(var(--foreground-muted))]">
                  <Moon className="h-4 w-4 text-[hsl(var(--accent))]" />
                  Birth Time
                </label>
                <input
                  id="birthTime"
                  type="time"
                  value={birthData.birth_time}
                  onChange={(e) => setBirthData(prev => ({ ...prev, birth_time: e.target.value }))}
                  className="w-full px-4 py-3 border border-[hsl(var(--border))/0.3] rounded-lg bg-[hsl(var(--background))/0.2] text-[hsl(var(--foreground))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--accent))] focus:border-[hsl(var(--accent))] transition-all duration-200"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-4">
                  <label htmlFor="latitude" className="flex items-center space-x-2 text-sm font-medium text-[hsl(var(--foreground-muted))]">
                    <MapPin className="h-4 w-4 text-[hsl(var(--accent))]" />
                    Latitude
                  </label>
                  <input
                    id="latitude"
                    type="number"
                    step="0.0001"
                    value={birthData.birth_latitude.toString()}
                    onChange={(e) => setBirthData(prev => ({ ...prev, birth_latitude: parseFloat(e.target.value) }))}
                    className="w-full px-4 py-3 border border-[hsl(var(--border))/0.3] rounded-lg bg-[hsl(var(--background))/0.2] text-[hsl(var(--foreground))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--accent))] focus:border-[hsl(var(--accent))] transition-all duration-200"
                  />
                </div>
                <div className="space-y-4">
                  <label htmlFor="longitude" className="flex items-center space-x-2 text-sm font-medium text-[hsl(var(--foreground-muted))]">
                    <MapPin className="h-4 w-4 text-[hsl(var(--accent))]" />
                    Longitude
                  </label>
                  <input
                    id="longitude"
                    type="number"
                    step="0.0001"
                    value={birthData.birth_longitude.toString()}
                    onChange={(e) => setBirthData(prev => ({ ...prev, birth_longitude: parseFloat(e.target.value) }))}
                    className="w-full px-4 py-3 border border-[hsl(var(--border))/0.3] rounded-lg bg-[hsl(var(--background))/0.2] text-[hsl(var(--foreground))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--accent))] focus:border-[hsl(var(--accent))] transition-all duration-200"
                  />
                </div>
              </div>

              <div className="space-y-4">
                <label htmlFor="timezone" className="flex items-center space-x-2 text-sm font-medium text-[hsl(var(--foreground-muted))]">
                  <MapPin className="h-4 w-4 text-[hsl(var(--accent))]" />
                  Timezone
                </label>
                <input
                  id="timezone"
                  type="text"
                  value={birthData.timezone}
                  onChange={(e) => setBirthData(prev => ({ ...prev, timezone: e.target.value }))}
                  className="w-full px-4 py-3 border border-[hsl(var(--border))/0.3] rounded-lg bg-[hsl(var(--background))/0.2] text-[hsl(var(--foreground))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--accent))] focus:border-[hsl(var(--accent))] transition-all duration-200"
                  placeholder="+05:30"
                />
              </div>
            </form>
          </CardContent>
          <CardFooter className="flex justify-end space-x-4 pt-4">
            <Button
              variant="outline"
              size="icon"
              onClick={handleGenerateChart}
              disabled={isGenerating}
              className="hover:bg-[hsl(var(--foreground))/0.05] transition-all duration-200"
            >
              {isGenerating ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Sparkles className="h-4 w-4" />
              )}
            </Button>
            <Button
              variant={isGenerating ? 'outline' : 'default'}
              disabled={isGenerating || isD1Pending || isD9Pending}
              onClick={handleGenerateChart}
              className="
                transition-all duration-300
                hover:scale-[1.02]
                active:scale-[0.98]
                {isGenerating ? 'opacity-80' : ''}
              "
            >
              {isGenerating ? 'Generating...' : 'Generate Chart'}
            </Button>
          </CardFooter>
        </Card>

        {error && (
          <div className="rounded-lg bg-[hsl(var(--destructive))]/10 border border-[hsl(var(--destructive))]/20 px-4 py-3 text-[hsl(var(--destructive))] text-sm">
            {error}
          </div>
        )}

        {isGenerating && !chartResult && (
          <div className="flex items-center justify-center py-8">
            <Loader2 className="h-8 w-8 text-[hsl(var(--accent))] animate-spin" />
          </div>
        )}

        {chartResult && (
          <div className="relative">
            <div className="mb-6">
              <ChartBase className="h-[500px] w-full">
                {chartType === 'd1' ? (
                  <D1Chart chartData={chartResult} className="opacity-0 animate-materialize" />
                ) : (
                  <D9Chart chartData={chartResult} className="opacity-0 animate-materialize" />
                )}
              </ChartBase>
            </div>

            <div className="space-y-4 text-center text-[hsl(var(--foreground-muted))] text-sm">
              <p>
                <strong>Born:</strong>
                {chartResult.birth_date} at {chartResult.birth_time}
                ({chartResult.timezone})
              </p>
              <p>
                <strong>Location:</strong>
                {chartResult.birth_latitude}° N, {chartResult.birth_longitude}° E
              </p>
              <p>
                <strong>Chart Type:</strong>
                {chartType.toUpperCase()}
              </p>
            </div>

            {/* Planetary Positions Section */}
            <div className="mt-8">
              <h3 className="text-xl font-display text-[hsl(var(--foreground))] mb-4">
                Planetary Positions
              </h3>
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                {chartResult.planetary_positions.map((planet) => (
                  <PlanetaryPositionCard
                    key={planet.planet}
                    planet={planet}
                  />
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </TooltipProvider>
  );
}