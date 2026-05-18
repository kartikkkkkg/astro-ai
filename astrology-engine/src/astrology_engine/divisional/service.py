"""
Divisional chart service for D2-D60 charts.
"""
from typing import Dict, Any, Optional, List
from ..charts.base import ChartCalculator
from ..core.models import BaseChart, DivisionalChartInfo

class DivisionalChartService:
    """
    Service for calculating divisional charts (D2 through D60).
    """

    def __init__(self, ayanamsa: str = None):
        """
        Initialize divisional chart service.

        Args:
            ayanamsa: Ayanamsa system to use
        """
        self.chart_calculator = ChartCalculator(ayanamsa)
        self.ayanamsa = ayanamsa

    def get_divisional_chart_info(self, division: int) -> DivisionalChartInfo:
        """
        Get information about a specific divisional chart.

        Args:
            division: Divisional number (2-60)

        Returns:
            DivisionalChartInfo object
        """
        if division < 2 or division > 60:
            raise ValueError("Divisional chart must be between D2 and D60")

        # Map common divisional charts to their descriptions
        divisional_descriptions = {
            2: "Hora - Wealth and possessions",
            3: "Drekkana - Siblings and courage",
            4: "Chaturthamsha - Property and fortune",
            5: "Panchamsha - Knowledge and intellect",
            6: "Shashthamsha - Enemies and diseases",
            7: "Saptamsha - Children and progeny",
            8: "Ashtamsha - Longevity and obstacles",
            9: "Navamsha - Spouse and partnerships",
            10: "Dashamsha - Career and profession",
            11: "Ekadashamsha - Gains and aspirations",
            12: "Dwadasamsha - Parents and grandparents",
            13: "Trayodashamsha - Purva punya and spiritual merit",
            14: "Chaturdashamsha - Strength and vitality",
            15: "Panchadashamsha - Auspicious and inauspicious effects",
            16: "Shodashamsha - Vehicles and comforts",
            17: "Saptadasamsha - Nature of death",
            18: "Ashtadasamsha - Difficulties and struggles",
            19: "Navadasamsha - Leprosy and skin diseases",
            20: "Vimshamsha - Spiritual advancement",
            21: "Chauvimshamsha - Nobel deeds and character",
            22: "Sauvimshamsha - Destruction and loss",
            23: "Traysovimshamsha - Education and learning",
            24: "Chaturvimshamsha - Knowledge and wisdom",
            25: "Panchavimshamsha - Strength and vitality",
            26: "Shadvimshamsha - Offspring and progeny",
            27: "Saptavimshamsha - Strength and courage",
            28: "Navavimshamsha - Prospects and opportunities",
            29: "Trimsamsha - Evils and troubles",
            30: "Chhatrashamsha - Obstacles and obstructions",
            40: "Khavedamsha - Auspicious and inauspicious effects",
            45: "Akshavedamsha - All areas of life",
            60: "Shashtiamsha - Past life karma"
        }

        description = divisional_descriptions.get(division, f"Divisional chart D{division}")

        return DivisionalChartInfo(
            division=division,
            multiplier=division,  # For simple multiplication method
            description=description
        )

    def calculate_divisional_chart(self, base_chart: BaseChart, division: int) -> BaseChart:
        """
        Calculate a specific divisional chart from a base chart.

        Args:
            base_chart: Base D1 chart
            division: Divisional number (2-60)

        Returns:
            BaseChart object for the divisional chart
        """
        return self.chart_calculator.calculate_divisional_chart(base_chart, division)

    def calculate_all_divisional_charts(self, base_chart: BaseChart,
                                      divisions: Optional[List[int]] = None) -> Dict[int, BaseChart]:
        """
        Calculate multiple divisional charts at once.

        Args:
            base_chart: Base D1 chart
            divisions: List of division numbers to calculate (defaults to common ones)

        Returns:
            Dictionary mapping division number to BaseChart
        """
        if divisions is None:
            # Common divisional charts for MVP
            divisions = [2, 3, 9, 10, 12, 16, 30, 40, 45, 60]

        charts = {}
        for division in divisions:
            try:
                charts[division] = self.calculate_divisional_chart(base_chart, division)
            except Exception as e:
                # In production, we might want to log this
                # For MVP, we'll skip failed calculations
                pass

        return charts