import type { ChartResponse } from '@/types/chart';

// In a real app, this would come from environment variables
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export interface ChartRequest {
  chart_type: 'd1' | 'd9';
  birth_date: string; // YYYY-MM-DD
  birth_time: string; // HH:MM
  birth_latitude: number;
  birth_longitude: number;
  timezone: string; // +/-HH:MM
}

export class ChartService {
  /**
   * Generate a chart using the backend API
   */
  static async generateChart(request: ChartRequest): Promise<ChartResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/charts/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate chart');
      }

      return await response.json();
    } catch (error) {
      console.error('Chart service error:', error);
      throw error;
    }
  }

  /**
   * Generate a D1 (natal) chart
   */
  static async generateD1Chart(request: Omit<ChartRequest, 'chart_type'>): Promise<ChartResponse> {
    return this.generateChart({ ...request, chart_type: 'd1' });
  }

  /**
   * Generate a D9 (navamsha) chart
   */
  static async generateD9Chart(request: Omit<ChartRequest, 'chart_type'>): Promise<ChartResponse> {
    return this.generateChart({ ...request, chart_type: 'd9' });
  }

  /**
   * Health check endpoint
   */
  static async healthCheck(): Promise<{ status: string }> {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      if (!response.ok) {
        throw new Error('Health check failed');
      }
      return await response.json();
    } catch (error) {
      console.error('Health check error:', error);
      throw error;
    }
  }
}