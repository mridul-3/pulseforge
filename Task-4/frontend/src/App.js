// File: Task-4/frontend/src/App.jsx
import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import './App.css';

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Title, Tooltip, Legend);

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export default function App() {
  const [startDate, setStartDate] = useState(new Date('2024-01-01'));
  const [endDate, setEndDate] = useState(new Date('2024-01-03'));
  const [userId, setUserId] = useState('synthetic_001');
  const [metric, setMetric] = useState('heart_rate');
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const res = await axios.get(`${API_BASE}/data`, {
        params: {
          start_date: startDate.toISOString().split('T')[0],
          end_date: endDate.toISOString().split('T')[0],
          user_id: userId,
          metric
        }
      });
      setData(res.data);
    } catch (err) {
      setError(err.response?.data?.error || err.message);
    } finally {
      setLoading(false);
    }
  }, [startDate, endDate, userId, metric]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const chartData = {
    labels: data.map(d => new Date(d.timestamp).toLocaleString()),
    datasets: [
      {
        label: `${metric.toUpperCase()} over time`,
        data: data.map(d => Number(d.value)),
        borderColor: 'rgba(54, 162, 235, 1)',
        backgroundColor: 'rgba(54, 162, 235, 0.1)',
        fill: true,
        tension: 0.3,
        pointRadius: 0,
        pointHoverRadius: 3,
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: true, position: 'top' },
      title: {
        display: true,
        text: `${metric.toUpperCase()} Trend`,
        font: { size: 22 }
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        callbacks: {
          title: (items) => {
            return items[0].label;
          }
        }
      }
    },
    scales: {
      x: {
        ticks: {
          maxRotation: 45,
          minRotation: 0,
          autoSkip: true,
          maxTicksLimit: 30
        },
        title: {
          display: true,
          text: 'Timestamp',
          font: { size: 14 }
        }
      },
      y: {
        title: {
          display: true,
          text: 'Value',
          font: { size: 14 }
        }
      }
    }
  };

  return (
    <div className="app-container" style={{ fontFamily: 'Inter, sans-serif', padding: '2rem', width: '100%', maxWidth: '1400px', margin: 'auto' }}>
      <h1 style={{ textAlign: 'center', fontSize: '2.5rem', marginBottom: '1.5rem' }}>🩺 Wearipedia Dashboard</h1>

      <div className="controls" style={{
        display: 'flex',
        flexWrap: 'wrap',
        gap: '1.2rem',
        marginBottom: '2rem',
        justifyContent: 'center'
      }}>
        <div>
          <label>User</label>
          <input value={userId} onChange={(e) => setUserId(e.target.value)} />
        </div>

        <div>
          <label>Metric</label>
          <select value={metric} onChange={(e) => setMetric(e.target.value)}>
            <option value="heart_rate">Heart Rate</option>
            <option value="spo2">SpO2</option>
            <option value="activity">Activity</option>
            <option value="hrv">HRV</option>
            <option value="active_zone_minute">Active Zone Minute</option>
            <option value="breath_rate">Breath Rate</option>
          </select>
        </div>

        <div>
          <label>From</label>
          <DatePicker selected={startDate} onChange={date => setStartDate(date)} />
        </div>

        <div>
          <label>To</label>
          <DatePicker selected={endDate} onChange={date => setEndDate(date)} />
        </div>

        <div style={{ display: 'flex', alignItems: 'flex-end' }}>
          <button onClick={fetchData} style={{ padding: '0.6rem 1.2rem', backgroundColor: '#3b82f6', color: 'white', border: 'none', borderRadius: '8px' }}>
            🔍 Fetch
          </button>
        </div>
      </div>

      {loading && <p style={{ textAlign: 'center' }}>Loading...</p>}
      {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}

      <p style={{ textAlign: 'center', marginBottom: '1rem' }}>Total Points: {data.length}</p>

      {data.length > 0 ? (
        <div style={{
          height: '600px',
          overflowX: 'auto',
          backgroundColor: '#f8fafc',
          padding: '1.5rem',
          borderRadius: '16px',
          boxShadow: '0 4px 15px rgba(0,0,0,0.1)'
        }}>
          <Line data={chartData} options={chartOptions} />
        </div>
      ) : (
        !loading && <p style={{ textAlign: 'center' }}>No data found for this selection.</p>
      )}
    </div>
  );
}