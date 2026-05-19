import { ChartWidget } from '@/components/widgets/ChartWidget';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { useHealthCheck } from '@/lib/hooks/useCharts';
import { Loader2 } from 'lucide-react';
import { framerMotion } from '@/lib/utils/framerMotion';

export default function Dashboard() {
  const { data: healthData, isLoading, error } = useHealthCheck();

  return (
    <div className="min-h-screen bg-background">
      <header className="bg-[var(--color-neutral-950)]/20 backdrop-blur-sm border-b border-[var(--color-neutral-100)]/10">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
            <div className="space-y-1">
              <h1 className="text-3xl font-display text-[var(--color-neutral-50)]">
                AstroAI Observatory
              </h1>
              <p className="text-sm text-[var(--color-neutral-300)]">
                Premium deterministic astrology platform
              </p>
            </div>

            <div className="flex items-center space-x-4 text-xs">
              {healthData ? (
                <span className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-[var(--color-primary-500)]/20 rounded-full">
                    <div className="w-full h-full bg-[var(--color-primary-500)] rounded-full animate-pulse-observatory" />
                  </div>
                  <span className="text-[var(--color-neutral-300)]">Backend: {healthData.status}</span>
                </span>
              ) : (
                <span className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-[var(--color-error)]/20 rounded-full">
                    <div className="w-full h-full bg-[var(--color-error)] rounded-full animate-pulse-observatory" />
                  </div>
                  <span className="text-[var(--color-neutral-300)]">Backend: Checking...</span>
                </span>
              )}
            </div>
          </div>
        </div>
      </header>

      <main className="py-8">
        <div className="max-w-7xl mx-auto px-6">
          {/* System Status */}
          {!isLoading && !healthData && error && (
            <div className="mb-6 rounded-lg bg-[hsl(var(--observatory-destructive))]/10 border border-[hsl(var(--observatory-destructive))]/20 p-4">
              <div className="flex items-center space-x-3">
                <div className="w-4 h-4 bg-[hsl(var(--observatory-destructive))] rounded-full"></div>
                <div>
                  <h3 className="font-semibold text-[hsl(var(--observatory-destructive))]">Connection Issue</h3>
                  <p className="text-sm text-[hsl(var(--observatory-foreground-muted))]">
                    Unable to connect to the astrology backend. Please ensure the server is running on localhost:8000
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Chart Grid */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {/* D1 Chart Widget */}
            <ChartWidget
              chartType="d1"
              defaultData={{
                birth_date: "1990-08-15",
                birth_time: "14:30",
                birth_latitude: 19.0760,
                birth_longitude: 72.8777,
                timezone: "+05:30"
              }}
              className="opacity-0 animate-materialize"
            />

            {/* D9 Chart Widget */}
            <ChartWidget
              chartType="d9"
              defaultData={{
                birth_date: "1990-08-15",
                birth_time: "14:30",
                birth_latitude: 19.0760,
                birth_longitude: 72.8777,
                timezone: "+05:30"
              }}
              className="opacity-0 animate-materialize"
            />

            {/* Empty widget for future expansion - could be transit chart, etc. */}
            <Card className="glass h-[500px] flex flex-col items-center justify-center opacity-0 animate-materialize">
              <div className="text-center">
                <Loader2 className="h-10 w-10 text-[hsl(var(--observatory-accent))]/50 mb-4" />
                <h3 className="font-semibold text-[hsl(var(--observatory-foreground))]">
                  Transit Chart
                </h3>
                <p className="text-[hsl(var(--observatory-foreground-muted))] text-sm">
                  Coming soon: Real-time transit calculations
                </p>
              </div>
            </Card>
          </div>
        </div>
      </main>

      <footer className="bg-[hsl(var(--observatory-background))/20] backdrop-blur-sm border-t border-[hsl(var(--observatory-border))]/10">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
            <div className="text-[hsl(var(--observatory-foreground-muted))] text-sm">
              AstroAI • Deterministic Astrology Engine v1.0.0
            </div>
            <div className="flex items-center space-x-4 text-[hsl(var(--observatory-foreground-muted))] text-sm">
              <span>Chart Calculation: Swiss Ephemeris</span>
              <span>Ayanamsa: Lahiri</span>
              <span>House System: Placidus</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}