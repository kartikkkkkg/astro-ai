import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { ChartService } from '@/lib/api/chartService';
import type { ChartResponse, ChartRequest } from '@/types/chart';

// Query keys
export const chartKeys = {
  all: ['charts'] as const,
  lists: () => [...chartKeys.all, 'list'] as const,
  list: (filters: string[]) => [...chartKeys.lists(), ...filters] as const,
  details: () => [...chartKeys.all, 'detail'] as const,
  detail: (id: number) => [...chartKeys.details(), id] as const,
  generating: ['generating'] as const,
};

/**
 * Hook to generate a chart (mutation)
 */
export function useGenerateChart() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (request: ChartRequest) =>
      ChartService.generateChart(request),
    onSuccess: (data, variables) => {
      // Invalidate and refetch queries if needed
      queryClient.invalidateQueries({ queryKey: chartKeys.all });
    },
    onError: (error) => {
      console.error('Failed to generate chart:', error);
      // Error handling can be customized by the consuming component
    },
  });
}

/**
 * Hook to generate a D1 chart
 */
export function useGenerateD1Chart() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (request: Omit<ChartRequest, 'chart_type'>) =>
      ChartService.generateD1Chart(request),
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: chartKeys.all });
    },
    onError: (error) => {
      console.error('Failed to generate D1 chart:', error);
    },
  });
}

/**
 * Hook to generate a D9 chart
 */
export function useGenerateD9Chart() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (request: Omit<ChartRequest, 'chart_type'>) =>
      ChartService.generateD9Chart(request),
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: chartKeys.all });
    },
    onError: (error) => {
      console.error('Failed to generate D9 chart:', error);
    },
  });
}

/**
 * Hook to check API health
 */
export function useHealthCheck() {
  return useQuery({
    queryKey: ['health'],
    queryFn: () => ChartService.healthCheck(),
    refetchInterval: 30000, // Check every 30 seconds
    retry: false,
  });
}