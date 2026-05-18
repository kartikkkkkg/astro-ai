import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { type TooltipProps } from "@/components/ui/tooltip";

interface ChartTooltipProps {
  type: 'planet' | 'house' | 'aspect';
  title: string;
  content: string;
  className?: string;
}

export function ChartTooltip({
  type,
  title,
  content,
  className,
}: ChartTooltipProps) {
  // Determine icon and color based on type
  const getTypeInfo = () => {
    switch (type) {
      case 'planet':
        return {
          icon: '🪐',
          bg: 'bg-[hsl(var(--observatory-primary))]/10',
          border: 'border-[hsl(var(--observatory-primary))]/20',
          text: 'text-[hsl(var(--observatory-primary))]',
        };
      case 'house':
        return {
          icon: '🏠',
          bg: 'bg-[hsl(var(--observatory-accent))]/10',
          border: 'border-[hsl(var(--observatory-accent))]/20',
          text: 'text-[hsl(var(--observatory-accent))]',
        };
      case 'aspect':
        return {
          icon: '🔗',
          bg: 'bg-[hsl(var(--observatory-cyan))]/10',
          border: 'border-[hsl(var(--observatory-cyan))]/20',
          text: 'text-[hsl(var(--observatory-cyan))]',
        };
      default:
        return {
          icon: '❓',
          bg: 'bg-[hsl(var(--observatory-muted))]/10',
          border: 'border-[hsl(var(--observatory-muted))]/20',
          text: 'text-[hsl(var(--observatory-foreground))]',
        };
    }
  };

  const { icon, bg, border, text } = getTypeInfo();

  return (
    <div className={twMerge(
      "max-w-xs px-4 py-3",
      bg,
      border,
      "rounded-lg",
      "shadow-observatory-lg",
      "text-sm",
      "z-50",
      className
    )}>
      <div className="flex items-center space-x-2 mb-2">
        <span className="text-2xl">{icon}</span>
        <h3 className={twMerge("font-semibold", text)}>{title}</h3>
      </div>
      <p className="text-[hsl(var(--observatory-foreground-muted))] leading-relaxed">
        {content}
      </p>
    </div>
  );
}