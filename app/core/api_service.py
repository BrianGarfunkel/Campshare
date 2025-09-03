import json
from typing import List, Dict, Optional


class MockCampgroundService:
    """Service to provide mock campground data."""
    
    def __init__(self):
        pass
    
    async def search_campgrounds(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for campgrounds using mock data only."""
        return self._get_mock_campgrounds(query, limit)

    def _get_mock_campgrounds(self, query: str, limit: int) -> List[Dict]:
        """Return mock campground data for development/testing."""
        mock_campgrounds = [
            # California
            {
                'name': 'Yosemite Valley Campground',
                'location': 'Yosemite National Park, CA',
                'state': 'CA',
                'description': 'Beautiful campground in the heart of Yosemite Valley with stunning granite cliffs',
                'latitude': 37.7489,
                'longitude': -119.5870,
                'amenities': json.dumps(['tent_sites', 'rv_sites', 'showers', 'water', 'fire_pits', 'bathrooms']),
                'external_id': 'mock_001',
                'source_api': 'mock_data'
            },
            {
                'name': 'Big Sur Campground',
                'location': 'Big Sur, CA',
                'state': 'CA',
                'description': 'Scenic coastal camping with ocean views and redwood forests',
                'latitude': 36.2704,
                'longitude': -121.8081,
                'amenities': json.dumps(['tent_sites', 'water', 'fire_pits', 'hiking_trails']),
                'external_id': 'mock_002',
                'source_api': 'mock_data'
            },
            {
                'name': 'Lake Tahoe Campground',
                'location': 'Lake Tahoe, CA',
                'state': 'CA',
                'description': 'Lakeside camping with mountain views and water activities',
                'latitude': 39.0968,
                'longitude': -120.0324,
                'amenities': json.dumps(['tent_sites', 'rv_sites', 'showers', 'wifi', 'boat_ramp']),
                'external_id': 'mock_003',
                'source_api': 'mock_data'
            },
            # Wyoming
            {
                'name': 'Yellowstone Valley Campground',
                'location': 'Yellowstone National Park, WY',
                'state': 'WY',
                'description': 'Historic campground near Old Faithful with geothermal features',
                'latitude': 44.4605,
                'longitude': -110.8281,
                'amenities': json.dumps(['tent_sites', 'rv_sites', 'showers', 'water', 'geyser_views']),
                'external_id': 'mock_004',
                'source_api': 'mock_data'
            },
            {
                'name': 'Grand Teton Campground',
                'location': 'Grand Teton National Park, WY',
                'state': 'WY',
                'description': 'Mountain camping with spectacular Teton Range views',
                'latitude': 43.7904,
                'longitude': -110.6818,
                'amenities': json.dumps(['tent_sites', 'hiking_trails', 'wildlife_viewing']),
                'external_id': 'mock_005',
                'source_api': 'mock_data'
            },
            # Colorado
            {
                'name': 'Rocky Mountain Campground',
                'location': 'Rocky Mountain National Park, CO',
                'state': 'CO',
                'description': 'Alpine camping with mountain lakes and wildlife',
                'latitude': 40.3556,
                'longitude': -105.6977,
                'amenities': json.dumps(['tent_sites', 'mountain_views', 'hiking_trails']),
                'external_id': 'mock_006',
                'source_api': 'mock_data'
            },
            # Utah
            {
                'name': 'Arches Campground',
                'location': 'Arches National Park, UT',
                'state': 'UT',
                'description': 'Desert camping among stunning red rock formations',
                'latitude': 38.7331,
                'longitude': -109.5925,
                'amenities': json.dumps(['tent_sites', 'desert_views', 'stargazing']),
                'external_id': 'mock_007',
                'source_api': 'mock_data'
            },
            # Arizona
            {
                'name': 'Grand Canyon Campground',
                'location': 'Grand Canyon National Park, AZ',
                'state': 'AZ',
                'description': 'Canyon rim camping with spectacular views',
                'latitude': 36.1069,
                'longitude': -112.1129,
                'amenities': json.dumps(['tent_sites', 'canyon_views', 'visitor_center']),
                'external_id': 'mock_008',
                'source_api': 'mock_data'
            },
            # Montana
            {
                'name': 'Glacier Peak Campground',
                'location': 'Glacier National Park, MT',
                'state': 'MT',
                'description': 'Alpine camping with glacier views and mountain goats',
                'latitude': 48.7596,
                'longitude': -113.7870,
                'amenities': json.dumps(['tent_sites', 'glacier_views', 'wildlife']),
                'external_id': 'mock_009',
                'source_api': 'mock_data'
            },
            # Oregon
            {
                'name': 'Crater Lake Campground',
                'location': 'Crater Lake National Park, OR',
                'state': 'OR',
                'description': 'Lakeside camping at the deepest lake in the US',
                'latitude': 42.9445,
                'longitude': -122.1090,
                'amenities': json.dumps(['tent_sites', 'lake_views', 'hiking_trails']),
                'external_id': 'mock_010',
                'source_api': 'mock_data'
            }
        ]
        
        # Filter by query if provided
        if query:
            query_lower = query.lower()
            
            # If query is exactly 2 characters, treat it as a state abbreviation
            if len(query) == 2:
                filtered = [cg for cg in mock_campgrounds 
                           if cg['state'].lower() == query_lower]
            else:
                # Regular text search on name, location, and description
                filtered = [cg for cg in mock_campgrounds 
                           if query_lower in cg['name'].lower() 
                           or query_lower in cg['location'].lower()
                           or query_lower in cg['description'].lower()]
            
            return filtered[:limit]
        
        return mock_campgrounds[:limit]


# Global instance
mock_campground_service = MockCampgroundService()
