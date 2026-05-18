import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { useEffect, useRef, useState } from "react";

interface ChartBaseProps {
  width?: number;
  height?: number;
  viewBox?: string;
  className?: string;
  children: React.ReactNode;
}

export function ChartBase({
  width = 400,
  height = 400,
  viewBox = "0 0 400 400",
  className,
  children,
}: ChartBaseProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState({ width, height });

  useEffect(() => {
    const updateDimensions = () => {
      if (containerRef.current) {
        const rect = containerRef.current.getBoundingClientRect();
        const size = Math.min(rect.width, rect.height, 800); // Max 800px
        setDimensions({ width: size, height: size });
      }
    };

    updateDimensions();
    window.addEventListener("resize", updateDimensions);
    return () => window.removeEventListener("resize", updateDimensions);
  }, []);

  return (
    <div
      ref={containerRef}
      className={twMerge(
        "relative w-full h-[400px] md:h-[500px] lg:h-[600px]",
        className
      )}
      style={{
        width: dimensions.width,
        height: dimensions.height,
      }}
    >
      <svg
        width={dimensions.width}
        height={dimensions.height}
        viewBox={viewBox}
        className="block"
      >
        {children}
      </svg>
    </div>
  );
}