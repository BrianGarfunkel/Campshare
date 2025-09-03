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
            # Step 1: Search for parks that match the query
            parks = await self._search_parks(query, min(limit, 5))  # Limit parks to avoid too many API calls
            
            # Step 2: Get campgrounds for each park
            all_campgrounds = []
            for park in parks:
                park_campgrounds = await self._get_campgrounds_for_park(park['park_id'], limit // len(parks) if len(parks) > 0 else limit)
                all_campgrounds.extend(park_campgrounds)
                if len(all_campgrounds) >= limit:
                    break
            
            return all_campgrounds[:limit]
            
        except Exception as e:
            print(f"API Error: {e}")
            return self._get_mock_campgrounds(query, limit)

    async def _search_parks(self, query: str, limit: int = 5) -> List[Dict]:
        """Search for parks using the searchForParks endpoint."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/searchForParks",
                    headers=self.headers,
                    params={
                        "keyword": query,  # Use 'keyword' parameter for search
                        "start": 0,
                        "limit": limit
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data.get('results', [])  # Use 'results' based on the API response
        except Exception as e:
            print(f"Park search error: {e}")
            return []

    async def _get_campgrounds_for_park(self, park_id: str, limit: int = 10) -> List[Dict]:
        """Get campgrounds for a specific park using getCampgroundsByParkId endpoint."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/parks/{park_id}/campgrounds",
                    headers=self.headers,
                    params={
                        "start": 0,
                        "limit": limit
                    }
                )
                response.raise_for_status()
                data = response.json()
                return self._parse_campground_data(data.get('results', []))  # Use 'results' based on the API response
        except Exception as e:
            print(f"Campground search error for park {park_id}: {e}")
            return []

    def _parse_campground_data(self, api_data: List[Dict]) -> List[Dict]:
        """Parse API response into our campground format."""
        campgrounds = []
        for item in api_data:
            # Build location string carefully to avoid quote issues
            park = item.get('park', 'Unknown Park')
            city = item.get('city', '')
            state = item.get('state', '')
            location_parts = [park]
            if city:
                location_parts.append(city)
            if state:
                location_parts.append(state)
            location = ', '.join(location_parts)
            
            campground = {
                'name': item.get('name', 'Unknown Campground'),
                'location': location,
                'description': item.get('description', ''),
                'latitude': item.get('latitude'),
                'longitude': item.get('longitude'),
                'amenities': json.dumps(item.get('equipments', [])),  # Use 'equipments' from API
                'external_id': item.get('campground_id'),  # Use 'campground_id' from API
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
