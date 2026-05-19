import { Loader2, Moon, Sparkles, Star } from 'lucide-react';
import { useMotionValue, useTransform } from 'framer-motion';
import { useEffect } from 'react';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  title?: string;
  className?: string;
}

export function LoadingSpinner({
  size = 'md',
  title = 'Generating your cosmic chart...',
  className = ''
}: LoadingSpinnerProps) {
  const sizeMap: Record<string, number> = {
    sm: 20,
    md: 32,
    lg: 48,
    xl: 64
  };

  const spinnerSize = sizeMap[size] || 32;
  const rotateValue = useMotionValue(0);

  useEffect(() => {
    rotateValue.set(spinnerSize * 0.1); // Start spinning immediately
  }, []);

  return (
    <div className={`flex flex-col items-center space-y-4 ${className}`}>
      <div className="relative w-[{$spinnerSize}px] h-[{$spinnerSize}px]">
        <Loader2
          className={`absolute inset-0 h-full w-full text-[hsl(var(--accent))]
          animate-[spin_${spinnerSize}s_linear_infinite]
          opacity-70`}
        />

        {/* Cosmic orbit effect */}
        <div className="absolute inset-0">
          <div className="absolute inset-0 rounded-full
            border-[hsl(var(--accent))]/20
            border-2
            animate-[orbit-slow_20s_linear_infinite]">
          </div>

          {/* Orbiting particles */}
          <div className="absolute inset-0 flex items-center justify-center">
            {[1, 2, 3].map((i) => (
              <div key={i} className="absolute w-2 h-2 bg-[hsl(var(--accent))]/50 rounded-full
                animate-[orbit-slow_${20 + i * 5}s_linear_infinite]
                transform-[translate(${Math.cos(i * 2) * 8}px,${Math.sin(i * 2) * 8}px)]"
              />
            ))}
          </div>
        </div>
      </div>

      {title && (
        <p className="text-[hsl(var(--foreground-muted))] text-center max-w-xs">
          {title}
        </p>
      )}
    </div>
  );
}

// Skeleton loader for chart elements
export function ChartSkeleton() {
  return (
    <div className="space-y-6">
      {/* Chart placeholder */}
      <div className="h-[400px] w-full rounded-xl bg-[hsl(var(--background))/0.1]
        animate-[pulse-slow_3s_ease-in-out_infinite]">
        <div className="absolute inset-0 pointer-events-none
          bg-[radial-gradient(circle_at_center,transparent_0%,hsl(var(--accent))/0.1_70%)]
          animate-[orbit-slow_15s_linear_infinite]">
        </div>
      </div>

      {/* Info skeleton */}
      <div className="space-y-3">
        <div className="h-4 w-32 rounded bg-[hsl(var(--background))/0.1]
          animate-[pulse-slow_3s_ease-in-out_infinite]"></div>
        <div className="h-4 w-24 rounded bg-[hsl(var(--background))/0.1]
          animate-[pulse-slow_3s_ease-in-out_infinite] delay-[100ms]"></div>
        <div className="h-4 w-20 rounded bg-[hsl(var(--background))/0.1]
          animate-[pulse-slow_3s_ease-in-out_infinite] delay-[200ms]"></div>
      </div>
    </div>
  );
}