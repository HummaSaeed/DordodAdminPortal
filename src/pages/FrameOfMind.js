import React, { useState, useEffect } from 'react';
import { Container, Card, Row, Col, Form, Button, Spinner } from 'react-bootstrap';
import axios from 'axios';
import { theme } from '../../theme';
import { Toast } from '../../components/Toast';
import { handleApiError } from '../../utils/apiErrorHandler';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const FrameOfMind = () => {
  const [mood, setMood] = useState({
    current_mood: '',
    energy_level: 5,
    stress_level: 5,
    notes: '',
    date: new Date().toISOString().split('T')[0]
  });

  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(false);
  const [moodHistory, setMoodHistory] = useState([]);
  const [toast, setToast] = useState({ show: false, message: '', variant: 'success' });

  const moodOptions = [
    'Happy', 'Excited', 'Calm', 'Focused',
    'Tired', 'Stressed', 'Anxious', 'Frustrated'
  ];

  // Fetch today's mood entry
  const fetchTodayMood = async () => {
    try {
      setFetching(true);
      const response = await axios.get('http://dordod.com/api/mood-tracking/today/', {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('accessToken')}` }
      });
      
      if (response.data) {
        setMood({
          current_mood: response.data.current_mood,
          energy_level: response.data.energy_level,
          stress_level: response.data.stress_level,
          notes: response.data.notes || '',
          date: response.data.date
        });
      }
    } catch (error) {
      if (error.response?.status !== 404) {
        setToast({
          show: true,
          message: handleApiError(error),
          variant: 'danger'
        });
      }
    } finally {
      setFetching(false);
    }
  };

  // Fetch mood history
  const fetchMoodHistory = async () => {
    try {
      const response = await axios.get('http://dordod.com/api/mood-tracking/history/', {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('accessToken')}` }
      });
      setMoodHistory(response.data);
    } catch (error) {
      setToast({
        show: true,
        message: handleApiError(error),
        variant: 'danger'
      });
    }
  };

  useEffect(() => {
    fetchTodayMood();
    fetchMoodHistory();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post('http://dordod.com/api/mood-tracking/', mood, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('accessToken')}` }
      });

      setToast({
        show: true,
        message: 'Mood updated successfully!',
        variant: 'success'
      });

      // Refresh mood history after successful update
      fetchMoodHistory();
    } catch (error) {
      setToast({
        show: true,
        message: handleApiError(error),
        variant: 'danger'
      });
    } finally {
      setLoading(false);
    }
  };

  // Prepare chart data
  const chartData = {
    labels: moodHistory.slice(0, 7).map(entry => new Date(entry.date).toLocaleDateString()),
    datasets: [
      {
        label: 'Energy Level',
        data: moodHistory.slice(0, 7).map(entry => entry.energy_level),
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      },
      {
        label: 'Stress Level',
        data: moodHistory.slice(0, 7).map(entry => entry.stress_level),
        borderColor: 'rgb(255, 99, 132)',
        tension: 0.1
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Mood Trends (Last 7 Days)'
      }
    },
    scales: {
      y: {
        min: 1,
        max: 10
      }
    }
  };

  return (
    <Container style={{ fontFamily: 'Poppins', paddingTop: '30px' }}>
      <Toast {...toast} onClose={() => setToast({ ...toast, show: false })} />
      
      <h2 style={{ color: theme.colors.primary, marginBottom: '30px' }}>
        Frame of Mind
      </h2>

      {fetching ? (
        <div className="text-center">
          <Spinner animation="border" role="status">
            <span className="visually-hidden">Loading...</span>
          </Spinner>
        </div>
      ) : (
        <>
          <Card style={{ boxShadow: theme.shadows.sm, marginBottom: '30px' }}>
            <Card.Header
              style={{
                backgroundImage: 'linear-gradient(45deg, #2C3E50, #28a745)',
                color: 'white',
                padding: '15px'
              }}
            >
              <h5 className="mb-0">Daily Mood Tracker</h5>
            </Card.Header>
            <Card.Body>
              <Form onSubmit={handleSubmit}>
                <Row>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>How are you feeling today?</Form.Label>
                      <div className="d-flex flex-wrap gap-2">
                        {moodOptions.map((option) => (
                          <Button
                            key={option}
                            variant={mood.current_mood === option ? 'success' : 'outline-success'}
                            onClick={() => setMood({ ...mood, current_mood: option })}
                            className="me-2 mb-2"
                          >
                            {option}
                          </Button>
                        ))}
                      </div>
                    </Form.Group>
                  </Col>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>Date</Form.Label>
                      <Form.Control
                        type="date"
                        value={mood.date}
                        onChange={(e) => setMood({ ...mood, date: e.target.value })}
                      />
                    </Form.Group>
                  </Col>
                </Row>

                <Row>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>Energy Level (1-10)</Form.Label>
                      <Form.Range
                        min="1"
                        max="10"
                        value={mood.energy_level}
                        onChange={(e) => setMood({ ...mood, energy_level: parseInt(e.target.value) })}
                      />
                      <div className="d-flex justify-content-between">
                        <span>Low</span>
                        <span>High</span>
                      </div>
                    </Form.Group>
                  </Col>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>Stress Level (1-10)</Form.Label>
                      <Form.Range
                        min="1"
                        max="10"
                        value={mood.stress_level}
                        onChange={(e) => setMood({ ...mood, stress_level: parseInt(e.target.value) })}
                      />
                      <div className="d-flex justify-content-between">
                        <span>Low</span>
                        <span>High</span>
                      </div>
                    </Form.Group>
                  </Col>
                </Row>

                <Form.Group className="mb-3">
                  <Form.Label>Notes</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={3}
                    value={mood.notes}
                    onChange={(e) => setMood({ ...mood, notes: e.target.value })}
                    placeholder="Add any additional notes about your mood..."
                  />
                </Form.Group>

                <div className="d-flex justify-content-end">
                  <Button
                    type="submit"
                    disabled={loading || !mood.current_mood}
                    style={{
                      backgroundImage: 'linear-gradient(45deg, #2C3E50, #28a745)',
                      border: 'none'
                    }}
                  >
                    {loading ? (
                      <>
                        <Spinner
                          as="span"
                          animation="border"
                          size="sm"
                          role="status"
                          aria-hidden="true"
                          className="me-2"
                        />
                        Saving...
                      </>
                    ) : (
                      'Save Mood'
                    )}
                  </Button>
                </div>
              </Form>
            </Card.Body>
          </Card>

          {/* Mood History Chart */}
          <Card style={{ boxShadow: theme.shadows.sm }}>
            <Card.Header
              style={{
                backgroundImage: 'linear-gradient(45deg, #2C3E50, #28a745)',
                color: 'white',
                padding: '15px'
              }}
            >
              <h5 className="mb-0">Mood History</h5>
            </Card.Header>
            <Card.Body>
              {moodHistory.length > 0 ? (
                <Line data={chartData} options={chartOptions} />
              ) : (
                <p className="text-center">No mood history available yet.</p>
              )}
            </Card.Body>
          </Card>
        </>
      )}
    </Container>
  );
};

export default FrameOfMind; 