import axios from 'axios';
import {
  User,
  Campground,
  CampingTrip,
  CampingTripWithDetails,
  Friend,
  FriendRequest,
  UserSearchResult,
  AuthResponse,
  LoginRequest,
  RegisterRequest,
  FriendRequestData,
  FriendResponseData
} from '../types/api';

const API_BASE_URL = 'http://localhost:8000/api/v1';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: async (credentials: LoginRequest): Promise<AuthResponse> => {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await axios.post(`${API_BASE_URL}/auth/login`, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },

  register: async (userData: RegisterRequest): Promise<User> => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/users/me');
    return response.data;
  },
};

// Campground API
export const campgroundAPI = {
  search: async (query: string, limit: number = 10): Promise<Campground[]> => {
    const response = await api.get(`/campgrounds/search?q=${encodeURIComponent(query)}&limit=${limit}`);
    return response.data;
  },

  getById: async (id: number): Promise<Campground> => {
    const response = await api.get(`/campgrounds/${id}`);
    return response.data;
  },
};

// Camping Trip API
export const campingTripAPI = {
  create: async (tripData: Omit<CampingTrip, 'id' | 'user_id' | 'created_at' | 'updated_at'>): Promise<CampingTrip> => {
    const response = await api.post('/camping-trips/', tripData);
    return response.data;
  },

  getMyTrips: async (skip: number = 0, limit: number = 100): Promise<CampingTrip[]> => {
    const response = await api.get(`/camping-trips/my-trips?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  getFeed: async (skip: number = 0, limit: number = 100): Promise<CampingTrip[]> => {
    const response = await api.get(`/camping-trips/feed?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  getForMap: async (includeOwn: boolean = true, includeFriends: boolean = true): Promise<CampingTripWithDetails[]> => {
    const response = await api.get(`/camping-trips/map?include_own=${includeOwn}&include_friends=${includeFriends}`);
    return response.data;
  },

  getById: async (id: number): Promise<CampingTrip> => {
    const response = await api.get(`/camping-trips/${id}`);
    return response.data;
  },

  update: async (id: number, tripData: Partial<CampingTrip>): Promise<CampingTrip> => {
    const response = await api.put(`/camping-trips/${id}`, tripData);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/camping-trips/${id}`);
  },
};

// Friend API
export const friendAPI = {
  searchUsers: async (query: string): Promise<UserSearchResult[]> => {
    const response = await api.get(`/friends/search?q=${encodeURIComponent(query)}`);
    return response.data;
  },

  sendRequest: async (username: string): Promise<{ message: string; friend_request_id: number }> => {
    const response = await api.post('/friends/send-request', { username });
    return response.data;
  },

  getPendingRequests: async (): Promise<FriendRequest[]> => {
    const response = await api.get('/friends/pending-requests');
    return response.data;
  },

  respondToRequest: async (requestId: number, accept: boolean): Promise<{ message: string }> => {
    const response = await api.post('/friends/respond', { friend_request_id: requestId, accept });
    return response.data;
  },

  getMyFriends: async (): Promise<Friend[]> => {
    const response = await api.get('/friends/my-friends');
    return response.data;
  },

  removeFriend: async (friendId: number): Promise<{ message: string }> => {
    const response = await api.delete(`/friends/remove/${friendId}`);
    return response.data;
  },
};

export default api;
