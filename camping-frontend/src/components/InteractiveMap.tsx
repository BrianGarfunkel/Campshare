import React, { useState, useEffect, forwardRef, useImperativeHandle } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { CampingTripWithDetails } from '../types/api';
import { campingTripAPI } from '../services/api';

// Fix for default markers in react-leaflet
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

// Custom icons for different trip types
const createCustomIcon = (isOwnTrip: boolean) => {
  return L.divIcon({
    className: 'custom-marker',
    html: `
      <div style="
        position: relative;
        width: 24px;
        height: 24px;
        background-color: ${isOwnTrip ? '#3b82f6' : '#EA4335'};
        border: 2px solid white;
        border-radius: 50% 50% 50% 0;
        transform: rotate(-45deg);
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
      ">
        <div style="
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%) rotate(45deg);
          width: 10px;
          height: 10px;
          background-color: white;
          border-radius: 50%;
        "></div>
      </div>
    `,
    iconSize: [24, 24],
    iconAnchor: [12, 24],
    popupAnchor: [0, -24],
  });
};

// Map controls component
const MapControls: React.FC<{
  includeOwn: boolean;
  includeFriends: boolean;
  onToggleOwn: () => void;
  onToggleFriends: () => void;
}> = ({ includeOwn, includeFriends, onToggleOwn, onToggleFriends }) => {
  return (
    <div style={{
      position: 'absolute',
      top: '1rem',
      right: '1rem',
      zIndex: 1000,
      backgroundColor: 'white',
      borderRadius: '8px',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
      padding: '1rem',
      minWidth: '200px'
    }}>
      <h3 style={{ fontWeight: '600', color: '#1f2937', marginBottom: '0.75rem' }}>Map Filters</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
          <input
            type="checkbox"
            checked={includeOwn}
            onChange={onToggleOwn}
            style={{ width: '1rem', height: '1rem' }}
          />
          <span style={{ fontSize: '0.875rem', color: '#374151' }}>My Trips</span>
        </label>
        <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
          <input
            type="checkbox"
            checked={includeFriends}
            onChange={onToggleFriends}
            style={{ width: '1rem', height: '1rem' }}
          />
          <span style={{ fontSize: '0.875rem', color: '#374151' }}>Friends' Trips</span>
        </label>
      </div>
      <div style={{ marginTop: '0.75rem', paddingTop: '0.75rem', borderTop: '1px solid #e5e7eb' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.75rem', color: '#6b7280' }}>
          <div style={{ width: '0.75rem', height: '0.75rem', backgroundColor: '#3b82f6', borderRadius: '50%' }}></div>
          <span>My Trips</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.75rem', color: '#6b7280' }}>
          <div style={{ width: '0.75rem', height: '0.75rem', backgroundColor: '#EA4335', borderRadius: '50%' }}></div>
          <span>Friends' Trips</span>
        </div>
      </div>
    </div>
  );
};

// Map bounds updater component
const MapBoundsUpdater: React.FC<{ trips: CampingTripWithDetails[] }> = ({ trips }) => {
  const map = useMap();

  useEffect(() => {
    if (trips.length > 0) {
      const bounds = L.latLngBounds(
        trips.map(trip => [trip.campground.latitude, trip.campground.longitude])
      );
      map.fitBounds(bounds, { padding: [20, 20] });
    }
  }, [trips, map]);

  return null;
};

interface InteractiveMapProps {
  onRefresh?: () => void;
}

export interface InteractiveMapRef {
  refreshTrips: () => void;
}

const InteractiveMap = forwardRef<InteractiveMapRef, InteractiveMapProps>(({ onRefresh }, ref) => {
  const [trips, setTrips] = useState<CampingTripWithDetails[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [includeOwn, setIncludeOwn] = useState(true);
  const [includeFriends, setIncludeFriends] = useState(true);
  const [mapReady, setMapReady] = useState(false);

  const fetchTrips = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await campingTripAPI.getForMap(includeOwn, includeFriends);
      setTrips(data);
    } catch (err) {
      setError('Failed to load camping trips');
      console.error('Error fetching trips:', err);
    } finally {
      setLoading(false);
    }
  };

  // Expose fetchTrips function to parent component
  useImperativeHandle(ref, () => ({
    refreshTrips: fetchTrips
  }));

  useEffect(() => {
    // Small delay to ensure DOM is ready
    const timer = setTimeout(() => {
      setMapReady(true);
      console.log('Map ready, fetching trips...');
    }, 500); // Increased delay
    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    if (mapReady) {
      console.log('Fetching trips with filters:', { includeOwn, includeFriends });
      fetchTrips();
    }
  }, [includeOwn, includeFriends, mapReady]);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const formatAmenities = (amenities: string) => {
    try {
      const parsed = JSON.parse(amenities);
      return Array.isArray(parsed) ? parsed.join(', ') : amenities;
    } catch {
      return amenities;
    }
  };

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{
            animation: 'spin 1s linear infinite',
            width: '3rem',
            height: '3rem',
            border: '2px solid #e5e7eb',
            borderTop: '2px solid #3b82f6',
            borderRadius: '50%',
            margin: '0 auto'
          }}></div>
          <p style={{ marginTop: '1rem', color: '#6b7280' }}>Loading camping trips...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh'
      }}>
        <div style={{ textAlign: 'center' }}>
          <p style={{ color: '#dc2626', marginBottom: '1rem' }}>{error}</p>
          <button
            onClick={fetchTrips}
            style={{
              padding: '0.5rem 1rem',
              backgroundColor: '#3b82f6',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer'
            }}
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={{ position: 'relative', height: 'calc(100vh - 4rem)', width: '100%', overflow: 'hidden' }}>
      <MapContainer
        center={[37.7749, -122.4194]} // Default to San Francisco
        zoom={6}
        style={{ height: '100%', width: '100%' }}
        zoomControl={true}
        scrollWheelZoom={true}
        doubleClickZoom={true}
        boxZoom={true}
        dragging={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.esri.com/">Esri</a> &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012'
          url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}"
          maxZoom={19}
        />

        <MapBoundsUpdater trips={trips} />

        {trips.map((trip) => (
          <Marker
            key={trip.id}
            position={[trip.campground.latitude, trip.campground.longitude]}
            icon={createCustomIcon(trip.is_own_trip)}
          >
            <Popup>
              <div style={{ minWidth: '250px' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                  <h3 style={{ fontWeight: 'bold', fontSize: '1.125rem', color: '#1f2937', margin: 0 }}>{trip.title}</h3>
                  <span style={{
                    padding: '0.25rem 0.5rem',
                    borderRadius: '9999px',
                    fontSize: '0.75rem',
                    fontWeight: '500',
                    backgroundColor: trip.is_own_trip ? '#dbeafe' : '#d1fae5',
                    color: trip.is_own_trip ? '#1e40af' : '#065f46'
                  }}>
                    {trip.is_own_trip ? 'My Trip' : 'Friend\'s Trip'}
                  </span>
                </div>

                <div style={{ marginBottom: '0.75rem' }}>
                  <p style={{ fontSize: '0.875rem', color: '#6b7280', margin: '0.25rem 0' }}>
                    <strong>By:</strong> {trip.user.full_name} (@{trip.user.username})
                  </p>
                  <p style={{ fontSize: '0.875rem', color: '#6b7280', margin: '0.25rem 0' }}>
                    <strong>Campground:</strong> {trip.campground.name}
                  </p>
                  <p style={{ fontSize: '0.875rem', color: '#6b7280', margin: '0.25rem 0' }}>
                    <strong>Location:</strong> {trip.campground.location}
                  </p>
                </div>

                <div style={{ marginBottom: '0.75rem' }}>
                  <p style={{ fontSize: '0.875rem', color: '#374151', margin: '0.25rem 0' }}>{trip.description}</p>
                  <p style={{ fontSize: '0.75rem', color: '#6b7280', margin: '0.25rem 0' }}>
                    <strong>Dates:</strong> {formatDate(trip.start_date)} - {formatDate(trip.end_date)}
                  </p>
                  <p style={{ fontSize: '0.75rem', color: '#6b7280', margin: '0.25rem 0' }}>
                    <strong>Group Size:</strong> {trip.group_size} people
                  </p>
                  {trip.weather_conditions && (
                    <p style={{ fontSize: '0.75rem', color: '#6b7280', margin: '0.25rem 0' }}>
                      <strong>Weather:</strong> {trip.weather_conditions}
                    </p>
                  )}
                </div>

                {trip.trip_notes && (
                  <div style={{ marginBottom: '0.75rem' }}>
                    <p style={{ fontSize: '0.75rem', color: '#6b7280', margin: '0.25rem 0' }}>
                      <strong>Notes:</strong> {trip.trip_notes}
                    </p>
                  </div>
                )}

                <div style={{ fontSize: '0.75rem', color: '#6b7280' }}>
                  <strong>Amenities:</strong> {formatAmenities(trip.campground.amenities)}
                </div>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>

      <MapControls
        includeOwn={includeOwn}
        includeFriends={includeFriends}
        onToggleOwn={() => setIncludeOwn(!includeOwn)}
        onToggleFriends={() => setIncludeFriends(!includeFriends)}
      />

      {trips.length === 0 && (
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          backgroundColor: 'white',
          borderRadius: '8px',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
          padding: '1.5rem',
          textAlign: 'center'
        }}>
          <p style={{ color: '#6b7280', marginBottom: '0.5rem' }}>No camping trips found</p>
          <p style={{ fontSize: '0.875rem', color: '#9ca3af' }}>
            Try adjusting the filters or add some camping trips!
          </p>
        </div>
      )}
    </div>
  );
});

InteractiveMap.displayName = 'InteractiveMap';

export default InteractiveMap;
