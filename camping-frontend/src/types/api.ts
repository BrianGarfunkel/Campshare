export interface User {
  id: number;
  username: string;
  full_name: string;
  email: string;
  is_active: boolean;
  created_at: string;
  updated_at: string | null;
}

export interface Campground {
  id: number;
  name: string;
  location: string;
  description: string;
  latitude: number;
  longitude: number;
  amenities: string;
  max_capacity: number | null;
  has_electricity: boolean | null;
  has_water: boolean | null;
  has_showers: boolean | null;
  has_wifi: boolean | null;
  pet_friendly: boolean | null;
  rv_friendly: boolean | null;
  tent_friendly: boolean | null;
  external_id: string;
  source_api: string;
  created_at: string;
}

export interface CampingTrip {
  id: number;
  title: string;
  description: string;
  start_date: string;
  end_date: string;
  notes: string | null;
  weather_conditions: string | null;
  group_size: number;
  user_id: number;
  campground_id: number;
  created_at: string;
  updated_at: string | null;
}

export interface CampingTripWithDetails {
  id: number;
  title: string;
  description: string;
  start_date: string;
  end_date: string;
  notes: string | null;
  weather_conditions: string | null;
  group_size: number;
  created_at: string;
  updated_at: string | null;
  is_own_trip: boolean;
  user: {
    id: number;
    username: string;
    full_name: string;
  };
  campground: {
    id: number;
    name: string;
    location: string;
    description: string;
    latitude: number;
    longitude: number;
    amenities: string;
  };
}

export interface Friend {
  id: number;
  user_id: number;
  friend_id: number;
  is_accepted: boolean;
  created_at: string;
  friend_username: string;
  friend_full_name: string;
}

export interface FriendRequest {
  id: number;
  user_id: number;
  friend_id: number;
  is_accepted: boolean;
  created_at: string;
  sender_username: string;
  sender_full_name: string;
}

export interface UserSearchResult {
  id: number;
  username: string;
  full_name: string;
  relationship_status: 'none' | 'friends' | 'request_sent' | 'request_received';
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
  full_name: string;
}

export interface FriendRequestData {
  username: string;
}

export interface FriendResponseData {
  friend_request_id: number;
  accept: boolean;
}
