import httpx
import json
from typing import List, Dict, Optional
from app.core.config import settings


class OutdoorActivitiesAPI:
    """Service to interact with RapidAPI Outdoor Activities API."""
    
    def __init__(self):
        self.base_url = "https://outdoor-activities.p.rapidapi.com"
        # You'll need to get your own API key from RapidAPI
        self.api_key = getattr(settings, 'rapidapi_key', None)
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "outdoor-activities.p.rapidapi.com"
        }
    
    async def search_campgrounds(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for campgrounds using the API."""
        if not self.api_key:
            # Return mock data for development
            return self._get_mock_campgrounds(query, limit)
        
        try:
            print(f"DEBUG: Headers: {self.headers}")
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/search",
                    headers=self.headers,
                    params={
                        "query": query,
                        "limit": limit,
                        "type": "campground"  # Assuming the API supports this filter
                    }
                )
                response.raise_for_status()
                data = response.json()
                return self._parse_campground_data(data)
        except Exception as e:
            print(f"API Error: {e}")
            return self._get_mock_campgrounds(query, limit)
    
    def _parse_campground_data(self, api_data: Dict) -> List[Dict]:
        """Parse API response into our campground format."""
        campgrounds = []
        # This will need to be adjusted based on the actual API response structure
        for item in api_data.get('results', []):
            campground = {
                'name': item.get('name', 'Unknown Campground'),
                'location': item.get('location', 'Unknown Location'),
                'description': item.get('description', ''),
                'latitude': item.get('lat'),
                'longitude': item.get('lng'),
                'amenities': json.dumps(item.get('amenities', [])),
                'external_id': item.get('id'),
                'source_api': 'rapidapi_outdoor'
            }
            campgrounds.append(campground)
        return campgrounds
    
    def _get_mock_campgrounds(self, query: str, limit: int) -> List[Dict]:
        """Return mock campground data for development/testing."""
        mock_campgrounds = [
            {
                'name': 'Yosemite Valley Campground',
                'location': 'Yosemite National Park, CA',
                'description': 'Beautiful campground in the heart of Yosemite Valley',
                'latitude': 37.7489,
                'longitude': -119.5870,
                'amenities': json.dumps(['tent_sites', 'rv_sites', 'showers', 'water']),
                'external_id': 'mock_001',
                'source_api': 'rapidapi_outdoor'
            },
            {
                'name': 'Big Sur Campground',
                'location': 'Big Sur, CA',
                'description': 'Scenic coastal camping with ocean views',
                'latitude': 36.2704,
                'longitude': -121.8081,
                'amenities': json.dumps(['tent_sites', 'water', 'fire_pits']),
                'external_id': 'mock_002',
                'source_api': 'rapidapi_outdoor'
            },
            {
                'name': 'Lake Tahoe Campground',
                'location': 'Lake Tahoe, CA',
                'description': 'Lakeside camping with mountain views',
                'latitude': 39.0968,
                'longitude': -120.0324,
                'amenities': json.dumps(['tent_sites', 'rv_sites', 'showers', 'wifi']),
                'external_id': 'mock_003',
                'source_api': 'rapidapi_outdoor'
            }
        ]
        
        # Filter by query if provided
        if query:
            filtered = [cg for cg in mock_campgrounds 
                       if query.lower() in cg['name'].lower() 
                       or query.lower() in cg['location'].lower()]
            return filtered[:limit]
        
        return mock_campgrounds[:limit]


# Global instance
outdoor_api = OutdoorActivitiesAPI()
