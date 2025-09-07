import React, { useState, useEffect } from 'react';
import { campgroundAPI, campingTripAPI } from '../services/api';
import { Campground, CampingTrip } from '../types/api';

interface CampingTripFormProps {
  onTripCreated?: () => void;
  onCancel?: () => void;
}

const CampingTripForm: React.FC<CampingTripFormProps> = ({ onTripCreated, onCancel }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    start_date: '',
    end_date: '',
    trip_notes: '',
    weather_conditions: '',
    group_size: 1,
    campground_search: '',
    selected_campground: null as Campground | null
  });

  const [searchResults, setSearchResults] = useState<Campground[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Search for campgrounds
  const handleCampgroundSearch = async (query: string) => {
    if (query.length < 2) {
      setSearchResults([]);
      return;
    }

    setIsSearching(true);
    try {
      const results = await campgroundAPI.search(query, 10);
      setSearchResults(results);
    } catch (err) {
      console.error('Error searching campgrounds:', err);
      setError('Failed to search campgrounds');
    } finally {
      setIsSearching(false);
    }
  };

  // Select a campground from search results
  const selectCampground = (campground: Campground) => {
    setFormData(prev => ({
      ...prev,
      selected_campground: campground,
      campground_search: campground.name
    }));
    setSearchResults([]);
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.selected_campground) {
      setError('Please select a campground');
      return;
    }
    
    if (!formData.title.trim()) {
      setError('Please enter a trip title');
      return;
    }
    
    if (!formData.start_date || !formData.end_date) {
      setError('Please select both start and end dates');
      return;
    }
    
    if (new Date(formData.start_date) >= new Date(formData.end_date)) {
      setError('End date must be after start date');
      return;
    }

    setIsSubmitting(true);
    setError('');
    setSuccess('');

    try {
      const tripData = {
        title: formData.title,
        description: formData.description,
        start_date: formData.start_date,
        end_date: formData.end_date,
        trip_notes: formData.trip_notes || null,
        weather_conditions: formData.weather_conditions || null,
        group_size: formData.group_size,
        campground_id: formData.selected_campground.id
      };

      await campingTripAPI.create(tripData);
      
      // Show success message
      setSuccess('Camping trip created successfully! 🎉');
      
      // Reset form and close modal after a short delay
      setTimeout(() => {
        setFormData({
          title: '',
          description: '',
          start_date: '',
          end_date: '',
          trip_notes: '',
          weather_conditions: '',
          group_size: 1,
          campground_search: '',
          selected_campground: null
        });
        setSuccess('');
        onTripCreated?.();
      }, 2000);
    } catch (err) {
      console.error('Error creating camping trip:', err);
      setError('Failed to create camping trip');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Set default dates (today and tomorrow)
  useEffect(() => {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    setFormData(prev => ({
      ...prev,
      start_date: today.toISOString().split('T')[0],
      end_date: tomorrow.toISOString().split('T')[0]
    }));
  }, []);

  return (
    <div style={{
      maxWidth: '600px',
      margin: '2rem auto',
      padding: '2rem',
      backgroundColor: 'white',
      borderRadius: '8px',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
      position: 'relative'
    }}>
      {/* Close Button */}
      {onCancel && (
        <button
          onClick={onCancel}
          style={{
            position: 'absolute',
            top: '1rem',
            right: '1rem',
            background: 'none',
            border: 'none',
            fontSize: '1.5rem',
            cursor: 'pointer',
            color: '#6b7280',
            padding: '0.25rem',
            borderRadius: '4px',
            transition: 'color 0.2s'
          }}
          onMouseOver={(e) => e.currentTarget.style.color = '#374151'}
          onMouseOut={(e) => e.currentTarget.style.color = '#6b7280'}
        >
          ×
        </button>
      )}
      
      <h2 style={{
        fontSize: '1.5rem',
        fontWeight: '600',
        marginBottom: '1.5rem',
        textAlign: 'center',
        color: '#111827'
      }}>
        🏕️ Log a Camping Trip
      </h2>

      {error && (
        <div style={{
          padding: '0.75rem',
          marginBottom: '1rem',
          backgroundColor: '#fef2f2',
          border: '1px solid #fecaca',
          borderRadius: '6px',
          color: '#dc2626'
        }}>
          {error}
        </div>
      )}

      {success && (
        <div style={{
          padding: '0.75rem',
          marginBottom: '1rem',
          backgroundColor: '#f0fdf4',
          border: '1px solid #bbf7d0',
          borderRadius: '6px',
          color: '#166534'
        }}>
          {success}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        {/* Campground Search */}
        <div style={{ marginBottom: '1.5rem' }}>
          <label style={{
            display: 'block',
            marginBottom: '0.5rem',
            fontWeight: '500',
            color: '#374151'
          }}>
            Campground *
          </label>
          <input
            type="text"
            value={formData.campground_search}
            onChange={(e) => {
              setFormData(prev => ({ ...prev, campground_search: e.target.value }));
              handleCampgroundSearch(e.target.value);
            }}
            placeholder="Search for a campground (e.g., 'Yosemite', 'CA')"
            style={{
              width: '100%',
              padding: '0.75rem',
              border: '1px solid #d1d5db',
              borderRadius: '6px',
              fontSize: '1rem'
            }}
          />
          
          {/* Search Results */}
          {searchResults.length > 0 && (
            <div style={{
              marginTop: '0.5rem',
              border: '1px solid #e5e7eb',
              borderRadius: '6px',
              maxHeight: '200px',
              overflowY: 'auto'
            }}>
              {searchResults.map((campground) => (
                <div
                  key={campground.id}
                  onClick={() => selectCampground(campground)}
                  style={{
                    padding: '0.75rem',
                    cursor: 'pointer',
                    borderBottom: '1px solid #f3f4f6',
                    transition: 'background-color 0.2s'
                  }}
                  onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#f9fafb'}
                  onMouseOut={(e) => e.currentTarget.style.backgroundColor = 'white'}
                >
                  <div style={{ fontWeight: '500' }}>{campground.name}</div>
                  <div style={{ fontSize: '0.875rem', color: '#6b7280' }}>
                    {campground.location}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Selected Campground */}
          {formData.selected_campground && (
            <div style={{
              marginTop: '0.5rem',
              padding: '0.75rem',
              backgroundColor: '#f0f9ff',
              border: '1px solid #0ea5e9',
              borderRadius: '6px'
            }}>
              <div style={{ fontWeight: '500', color: '#0c4a6e' }}>
                Selected: {formData.selected_campground.name}
              </div>
              <div style={{ fontSize: '0.875rem', color: '#0369a1' }}>
                {formData.selected_campground.location}
              </div>
            </div>
          )}
        </div>

        {/* Trip Title */}
        <div style={{ marginBottom: '1.5rem' }}>
          <label style={{
            display: 'block',
            marginBottom: '0.5rem',
            fontWeight: '500',
            color: '#374151'
          }}>
            Trip Title *
          </label>
          <input
            type="text"
            value={formData.title}
            onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
            placeholder="e.g., 'Weekend at Yosemite'"
            required
            style={{
              width: '100%',
              padding: '0.75rem',
              border: '1px solid #d1d5db',
              borderRadius: '6px',
              fontSize: '1rem'
            }}
          />
        </div>

        {/* Description */}
        <div style={{ marginBottom: '1.5rem' }}>
          <label style={{
            display: 'block',
            marginBottom: '0.5rem',
            fontWeight: '500',
            color: '#374151'
          }}>
            Description
          </label>
          <textarea
            value={formData.description}
            onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
            placeholder="Tell us about your camping trip..."
            rows={3}
            style={{
              width: '100%',
              padding: '0.75rem',
              border: '1px solid #d1d5db',
              borderRadius: '6px',
              fontSize: '1rem',
              resize: 'vertical'
            }}
          />
        </div>

        {/* Dates and Group Size */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem', marginBottom: '1.5rem' }}>
          <div>
            <label style={{
              display: 'block',
              marginBottom: '0.5rem',
              fontWeight: '500',
              color: '#374151'
            }}>
              Start Date *
            </label>
            <input
              type="date"
              value={formData.start_date}
              onChange={(e) => setFormData(prev => ({ ...prev, start_date: e.target.value }))}
              required
              style={{
                width: '100%',
                padding: '0.75rem',
                border: '1px solid #d1d5db',
                borderRadius: '6px',
                fontSize: '1rem'
              }}
            />
          </div>

          <div>
            <label style={{
              display: 'block',
              marginBottom: '0.5rem',
              fontWeight: '500',
              color: '#374151'
            }}>
              End Date *
            </label>
            <input
              type="date"
              value={formData.end_date}
              onChange={(e) => setFormData(prev => ({ ...prev, end_date: e.target.value }))}
              required
              style={{
                width: '100%',
                padding: '0.75rem',
                border: '1px solid #d1d5db',
                borderRadius: '6px',
                fontSize: '1rem'
              }}
            />
          </div>

          <div>
            <label style={{
              display: 'block',
              marginBottom: '0.5rem',
              fontWeight: '500',
              color: '#374151'
            }}>
              Group Size
            </label>
            <input
              type="number"
              min="1"
              value={formData.group_size}
              onChange={(e) => setFormData(prev => ({ ...prev, group_size: parseInt(e.target.value) || 1 }))}
              placeholder="Number of people"
              style={{
                width: '100%',
                padding: '0.75rem',
                border: '1px solid #d1d5db',
                borderRadius: '6px',
                fontSize: '1rem'
              }}
            />
          </div>
        </div>

        {/* Notes and Weather */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.5rem' }}>
          <div>
            <label style={{
              display: 'block',
              marginBottom: '0.5rem',
              fontWeight: '500',
              color: '#374151'
            }}>
              Notes
            </label>
            <textarea
              value={formData.trip_notes}
              onChange={(e) => setFormData(prev => ({ ...prev, trip_notes: e.target.value }))}
              placeholder="Any additional notes..."
              rows={2}
              style={{
                width: '100%',
                padding: '0.75rem',
                border: '1px solid #d1d5db',
                borderRadius: '6px',
                fontSize: '1rem',
                resize: 'vertical'
              }}
            />
          </div>

          <div>
            <label style={{
              display: 'block',
              marginBottom: '0.5rem',
              fontWeight: '500',
              color: '#374151'
            }}>
              Weather Conditions
            </label>
            <textarea
              value={formData.weather_conditions}
              onChange={(e) => setFormData(prev => ({ ...prev, weather_conditions: e.target.value }))}
              placeholder="Weather during your trip..."
              rows={2}
              style={{
                width: '100%',
                padding: '0.75rem',
                border: '1px solid #d1d5db',
                borderRadius: '6px',
                fontSize: '1rem',
                resize: 'vertical'
              }}
            />
          </div>
        </div>

        {/* Buttons */}
        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              disabled={isSubmitting}
              style={{
                padding: '0.75rem 1.5rem',
                backgroundColor: '#f3f4f6',
                color: '#374151',
                border: 'none',
                borderRadius: '6px',
                fontSize: '1rem',
                cursor: 'pointer',
                transition: 'background-color 0.2s'
              }}
              onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#e5e7eb'}
              onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#f3f4f6'}
            >
              Cancel
            </button>
          )}
          
          <button
            type="submit"
            disabled={isSubmitting || !formData.selected_campground}
            style={{
              padding: '0.75rem 1.5rem',
              backgroundColor: isSubmitting || !formData.selected_campground ? '#9ca3af' : '#3b82f6',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              fontSize: '1rem',
              cursor: isSubmitting || !formData.selected_campground ? 'not-allowed' : 'pointer',
              transition: 'background-color 0.2s'
            }}
            onMouseOver={(e) => {
              if (!isSubmitting && formData.selected_campground) {
                e.currentTarget.style.backgroundColor = '#2563eb';
              }
            }}
            onMouseOut={(e) => {
              if (!isSubmitting && formData.selected_campground) {
                e.currentTarget.style.backgroundColor = '#3b82f6';
              }
            }}
          >
            {isSubmitting ? 'Creating...' : 'Log Trip'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default CampingTripForm;
