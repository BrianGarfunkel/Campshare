import json
from typing import List, Dict, Optional


class OutdoorActivitiesAPI:
    """Service to provide mock campground data."""
    
    def __init__(self):
        pass
    
    async def search_campgrounds(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for campgrounds using mock data only."""
        return self._get_mock_campgrounds(query, limit)

    def _get_mock_campgrounds(self, query: str, limit: int) -> List[Dict]:
        """Return mock campground data for development/testing."""
        mock_campgrounds = [
            {
                "name": "Yosemite Valley Campground",
                "location": "Yosemite National Park, CA",
                "description": "Beautiful campground in the heart of Yosemite Valley with stunning granite cliffs",
                "latitude": 37.7489,
                "longitude": -119.5870,
                "amenities": json.dumps(["tent_sites", "rv_sites", "showers", "water", "fire_pits", "bathrooms"]),
                "external_id": "mock_001",
                "source_api": "mock_data"
            },
            {
                "name": "Big Sur Campground",
                "location": "Big Sur, CA",
                "description": "Scenic coastal camping with ocean views and redwood forests",
                "latitude": 36.2704,
                "longitude": -121.8081,
                "amenities": json.dumps(["tent_sites", "water", "fire_pits", "hiking_trails"]),
                "external_id": "mock_002",
                "source_api": "mock_data"
            },
            {
                "name": "Lake Tahoe Campground",
                "location": "Lake Tahoe, CA",
                "description": "Lakeside camping with mountain views and water activities",
                "latitude": 39.0968,
                "longitude": -120.0324,
                "amenities": json.dumps(["tent_sites", "rv_sites", "showers", "wifi", "boat_ramp"]),
                "external_id": "mock_003",
                "source_api": "mock_data"
            },
            {
                "name": "Yellowstone Valley Campground",
                "location": "Yellowstone National Park, WY",
                "description": "Historic campground near Old Faithful with geothermal features",
                "latitude": 44.4605,
                "longitude": -110.8281,
                "amenities": json.dumps(["tent_sites", "rv_sites", "showers", "water", "geyser_views"]),
                "external_id": "mock_004",
                "source_api": "mock_data"
            },
            {
                "name": "Grand Teton Campground",
                "location": "Grand Teton National Park, WY",
                "description": "Mountain camping with spectacular Teton Range views",
                "latitude": 43.7904,
                "longitude": -110.6818,
                "amenities": json.dumps(["tent_sites", "hiking_trails", "wildlife_viewing"]),
                "external_id": "mock_005",
                "source_api": "mock_data"
            }
        ]
        
        # Filter by query if provided
        if query:
            query_lower = query.lower()
            filtered = [cg for cg in mock_campgrounds 
                       if query_lower in cg["name"].lower() 
                       or query_lower in cg["location"].lower()
                       or query_lower in cg["description"].lower()
                       or any(state in cg["location"] for state in ["CA", "WY", "CO", "UT", "AZ", "MT", "OR"] if query_lower in state.lower())]
            return filtered[:limit]
        
        return mock_campgrounds[:limit]


# Global instance
outdoor_api = OutdoorActivitiesAPI()
