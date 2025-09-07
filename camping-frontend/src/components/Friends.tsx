import React, { useState, useEffect } from 'react';
import { friendAPI } from '../services/api';
import { UserSearchResult, Friend, FriendRequest } from '../types/api';

interface FriendsProps {
  onBack: () => void;
}

const Friends: React.FC<FriendsProps> = ({ onBack }) => {
  const [activeTab, setActiveTab] = useState<'search' | 'pending' | 'friends'>('search');
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<UserSearchResult[]>([]);
  const [pendingRequests, setPendingRequests] = useState<FriendRequest[]>([]);
  const [friends, setFriends] = useState<Friend[]>([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  // Load pending requests and friends on component mount
  useEffect(() => {
    loadPendingRequests();
    loadFriends();
  }, []);

  const loadPendingRequests = async () => {
    try {
      const requests = await friendAPI.getPendingRequests();
      setPendingRequests(requests);
    } catch (error) {
      console.error('Error loading pending requests:', error);
    }
  };

  const loadFriends = async () => {
    try {
      const friendsList = await friendAPI.getMyFriends();
      setFriends(friendsList);
    } catch (error) {
      console.error('Error loading friends:', error);
    }
  };

  const searchUsers = async (query: string) => {
    if (query.trim().length < 2) {
      setSearchResults([]);
      return;
    }

    setLoading(true);
    try {
      const results = await friendAPI.searchUsers(query);
      setSearchResults(results);
    } catch (error) {
      console.error('Error searching users:', error);
      setMessage('Error searching users');
    } finally {
      setLoading(false);
    }
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const query = e.target.value;
    setSearchQuery(query);
    searchUsers(query);
  };

  const sendFriendRequest = async (username: string) => {
    try {
      await friendAPI.sendRequest(username);
      setMessage(`Friend request sent to ${username}`);
      // Refresh search results to update status
      searchUsers(searchQuery);
    } catch (error: any) {
      setMessage(error.response?.data?.detail || 'Error sending friend request');
    }
  };

  const respondToRequest = async (requestId: number, accept: boolean) => {
    try {
      await friendAPI.respondToRequest(requestId, accept);
      setMessage(accept ? 'Friend request accepted' : 'Friend request rejected');
      loadPendingRequests();
      loadFriends();
    } catch (error: any) {
      setMessage(error.response?.data?.detail || 'Error responding to request');
    }
  };

  const removeFriend = async (friendId: number) => {
    if (window.confirm('Are you sure you want to remove this friend?')) {
      try {
        await friendAPI.removeFriend(friendId);
        setMessage('Friend removed');
        loadFriends();
      } catch (error: any) {
        setMessage(error.response?.data?.detail || 'Error removing friend');
      }
    }
  };

  const getStatusButton = (user: UserSearchResult) => {
    switch (user.relationship_status) {
      case 'friends':
        return <span style={{ color: '#10b981', fontSize: '0.875rem' }}>Friends</span>;
      case 'request_sent':
        return <span style={{ color: '#6b7280', fontSize: '0.875rem' }}>Request Sent</span>;
      case 'request_received':
        return <span style={{ color: '#f59e0b', fontSize: '0.875rem' }}>Request Received</span>;
      default:
        return (
          <button
            onClick={() => sendFriendRequest(user.username)}
            style={{
              padding: '0.25rem 0.75rem',
              backgroundColor: '#3b82f6',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              fontSize: '0.875rem',
              cursor: 'pointer'
            }}
          >
            Add Friend
          </button>
        );
    }
  };

  return (
    <div style={{ 
      height: 'calc(100vh - 4rem)', 
      display: 'flex', 
      flexDirection: 'column',
      backgroundColor: '#f9fafb'
    }}>
      {/* Header */}
      <div style={{
        padding: '1rem',
        backgroundColor: 'white',
        borderBottom: '1px solid #e5e7eb',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <button
            onClick={onBack}
            style={{
              background: 'none',
              border: 'none',
              fontSize: '1.5rem',
              cursor: 'pointer',
              color: '#6b7280'
            }}
          >
            ←
          </button>
          <h1 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 'bold' }}>Friends</h1>
        </div>
      </div>

      {/* Message */}
      {message && (
        <div style={{
          padding: '0.75rem 1rem',
          backgroundColor: message.includes('Error') ? '#fef2f2' : '#f0fdf4',
          border: `1px solid ${message.includes('Error') ? '#fecaca' : '#bbf7d0'}`,
          color: message.includes('Error') ? '#dc2626' : '#166534',
          fontSize: '0.875rem'
        }}>
          {message}
        </div>
      )}

      {/* Tabs */}
      <div style={{
        display: 'flex',
        backgroundColor: 'white',
        borderBottom: '1px solid #e5e7eb'
      }}>
        {[
          { key: 'search', label: 'Search Users' },
          { key: 'pending', label: `Pending (${pendingRequests.length})` },
          { key: 'friends', label: `Friends (${friends.length})` }
        ].map(tab => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key as any)}
            style={{
              padding: '1rem',
              border: 'none',
              backgroundColor: activeTab === tab.key ? '#3b82f6' : 'transparent',
              color: activeTab === tab.key ? 'white' : '#6b7280',
              cursor: 'pointer',
              fontSize: '0.875rem',
              fontWeight: '500',
              borderBottom: activeTab === tab.key ? '2px solid #3b82f6' : '2px solid transparent'
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Content */}
      <div style={{ flex: 1, padding: '1rem', overflow: 'auto' }}>
        {activeTab === 'search' && (
          <div>
            <div style={{ marginBottom: '1rem' }}>
              <input
                type="text"
                placeholder="Search for users by username..."
                value={searchQuery}
                onChange={handleSearchChange}
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  border: '1px solid #d1d5db',
                  borderRadius: '6px',
                  fontSize: '1rem'
                }}
              />
            </div>

            {loading && <div style={{ textAlign: 'center', padding: '2rem' }}>Searching...</div>}

            {searchResults.length > 0 && (
              <div>
                {searchResults.map(user => (
                  <div
                    key={user.id}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      padding: '1rem',
                      backgroundColor: 'white',
                      border: '1px solid #e5e7eb',
                      borderRadius: '6px',
                      marginBottom: '0.5rem'
                    }}
                  >
                    <div>
                      <div style={{ fontWeight: '500', fontSize: '1rem' }}>{user.full_name}</div>
                      <div style={{ color: '#6b7280', fontSize: '0.875rem' }}>@{user.username}</div>
                    </div>
                    {getStatusButton(user)}
                  </div>
                ))}
              </div>
            )}

            {searchQuery.length >= 2 && searchResults.length === 0 && !loading && (
              <div style={{ textAlign: 'center', padding: '2rem', color: '#6b7280' }}>
                No users found
              </div>
            )}
          </div>
        )}

        {activeTab === 'pending' && (
          <div>
            {pendingRequests.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '2rem', color: '#6b7280' }}>
                No pending friend requests
              </div>
            ) : (
              <div>
                {pendingRequests.map(request => (
                  <div
                    key={request.id}
                    style={{
                      padding: '1rem',
                      backgroundColor: 'white',
                      border: '1px solid #e5e7eb',
                      borderRadius: '6px',
                      marginBottom: '0.5rem'
                    }}
                  >
                    <div style={{ marginBottom: '0.5rem' }}>
                      <div style={{ fontWeight: '500', fontSize: '1rem' }}>{request.sender_full_name}</div>
                      <div style={{ color: '#6b7280', fontSize: '0.875rem' }}>@{request.sender_username}</div>
                    </div>
                    <div style={{ display: 'flex', gap: '0.5rem' }}>
                      <button
                        onClick={() => respondToRequest(request.id, true)}
                        style={{
                          padding: '0.5rem 1rem',
                          backgroundColor: '#10b981',
                          color: 'white',
                          border: 'none',
                          borderRadius: '4px',
                          cursor: 'pointer',
                          fontSize: '0.875rem'
                        }}
                      >
                        Accept
                      </button>
                      <button
                        onClick={() => respondToRequest(request.id, false)}
                        style={{
                          padding: '0.5rem 1rem',
                          backgroundColor: '#ef4444',
                          color: 'white',
                          border: 'none',
                          borderRadius: '4px',
                          cursor: 'pointer',
                          fontSize: '0.875rem'
                        }}
                      >
                        Reject
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'friends' && (
          <div>
            {friends.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '2rem', color: '#6b7280' }}>
                No friends yet. Search for users to add friends!
              </div>
            ) : (
              <div>
                {friends.map(friend => (
                  <div
                    key={friend.id}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      padding: '1rem',
                      backgroundColor: 'white',
                      border: '1px solid #e5e7eb',
                      borderRadius: '6px',
                      marginBottom: '0.5rem'
                    }}
                  >
                    <div>
                      <div style={{ fontWeight: '500', fontSize: '1rem' }}>{friend.friend_full_name}</div>
                      <div style={{ color: '#6b7280', fontSize: '0.875rem' }}>@{friend.friend_username}</div>
                    </div>
                    <button
                      onClick={() => removeFriend(friend.friend_id)}
                      style={{
                        padding: '0.5rem 1rem',
                        backgroundColor: '#ef4444',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontSize: '0.875rem'
                      }}
                    >
                      Remove
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Friends;
