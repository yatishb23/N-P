import random
import time

class DoctorRecommendationEngine:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def search_nearby_doctors(self, location_text):
        """Simulates fetching dermatologists near the user's location."""
        time.sleep(1.0) # Faster UI load
        
        mock_names = ["Dr. Sarah Sharma", "Dr. Amit Patil", "SkinCare Specialists Clinic", "Dr. Ravi Gupta", "DermaGlow Hospital"]
        mock_addresses = [
            f"12 Main St, {location_text}",
            f"Crossroad Medical Center, {location_text}",
            f"Suite 404, City Plaza, {location_text}",
            f"78 Health Ave, {location_text}",
            f"North wing, Metro Hospital, {location_text}"
        ]

        results = []
        num_results = random.randint(2, 4)
        
        for i in range(num_results):
            results.append({
                "name": mock_names[i],
                "address": mock_addresses[i],
                "rating": round(random.uniform(3.8, 4.9), 1),
                "distance_km": round(random.uniform(0.5, 8.0), 1)
            })
            
        results.sort(key=lambda x: x['distance_km'])
        return results
