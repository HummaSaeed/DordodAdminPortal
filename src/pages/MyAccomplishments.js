import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Form, Modal, Badge, Alert, ProgressBar, Card } from 'react-bootstrap';
import { 
  FaTrophy, FaPlus, FaShare, FaEdit, FaTrash, FaMedal, 
  FaCertificate, FaBriefcase, FaGraduationCap, FaStar,
  FaDownload, FaEye, FaFilter, FaSort, FaChartBar
} from 'react-icons/fa';
import { DashboardCard, ActionButton } from '../components/SharedComponents';
import { useApp } from '../context/AppContext';
import { formatDate } from '../utils/helpers';

const API_URL = 'http://127.0.0.1:8000/api/accomplishments/';

const MyAccomplishments = () => {
  const { state, dispatch } = useApp();
  const [accomplishments, setAccomplishments] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [selectedAccomplishment, setSelectedAccomplishment] = useState(null);
  const [stats, setStats] = useState({});
  const [filter, setFilter] = useState('all');
  const [sortBy, setSortBy] = useState('date');
  const [searchTerm, setSearchTerm] = useState('');
  const [newAccomplishment, setNewAccomplishment] = useState({
    title: '',
    description: '',
    date: new Date().toISOString().split('T')[0],
    category: 'professional',
    impact: '',
    evidence: null,
    is_public: false,
    tags: [],
    skills_used: [],
    metrics: {},
    external_links: []
  });

  const categories = [
    { value: 'professional', label: 'Professional', icon: FaBriefcase, color: 'primary' },
    { value: 'academic', label: 'Academic', icon: FaGraduationCap, color: 'success' },
    { value: 'personal', label: 'Personal', icon: FaStar, color: 'warning' },
    { value: 'certification', label: 'Certification', icon: FaCertificate, color: 'info' },
    { value: 'award', label: 'Award', icon: FaMedal, color: 'danger' },
    { value: 'project', label: 'Project', icon: FaTrophy, color: 'secondary' },
    { value: 'publication', label: 'Publication', icon: FaEdit, color: 'dark' },
    { value: 'volunteer', label: 'Volunteer', icon: FaStar, color: 'success' }
  ];

  useEffect(() => {
    fetchAccomplishments();
    fetchStats();
  }, []);

  const fetchAccomplishments = async () => {
    setLoading(true);
    try {
      const response = await fetch(API_URL, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json'
        }
      });
      const data = await response.json();
      setAccomplishments(data);
      
      dispatch({
        type: 'UPDATE_PROGRESS',
        payload: {
          ...state.progress,
          accomplishments: data.length
        }
      });
    } catch (err) {
      console.error('Failed to fetch accomplishments:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await fetch(`${API_URL}stats/`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json'
        }
      });
      const data = await response.json();
      setStats(data);
    } catch (err) {
      console.error('Failed to fetch stats:', err);
    }
  };

  const handleSubmit = async () => {
    try {
      const formData = new FormData();
      Object.keys(newAccomplishment).forEach(key => {
        if (key === 'evidence' && newAccomplishment[key]) {
          formData.append(key, newAccomplishment[key]);
        } else if (key !== 'evidence') {
          formData.append(key, JSON.stringify(newAccomplishment[key]));
        }
      });

      const url = selectedAccomplishment 
        ? `${API_URL}${selectedAccomplishment.id}/`
        : API_URL;
      
      const method = selectedAccomplishment ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: formData
      });

      if (response.ok) {
        fetchAccomplishments();
        fetchStats();
        setShowModal(false);
        resetForm();
      }
    } catch (err) {
      console.error('Failed to save accomplishment:', err);
    }
  };

  const handleShare = async (accomplishment) => {
    try {
      const response = await fetch(`${API_URL}${accomplishment.id}/share/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          platform: 'connections',
          message: `Check out my accomplishment: ${accomplishment.title}`
        })
      });
      
      if (response.ok) {
        alert('Accomplishment shared successfully!');
      }
    } catch (err) {
      console.error('Failed to share accomplishment:', err);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this accomplishment?')) {
      try {
        const response = await fetch(`${API_URL}${id}/`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          }
        });
        
        if (response.ok) {
          fetchAccomplishments();
          fetchStats();
        }
      } catch (err) {
        console.error('Failed to delete accomplishment:', err);
      }
    }
  };

  const resetForm = () => {
    setNewAccomplishment({
      title: '',
      description: '',
      date: new Date().toISOString().split('T')[0],
      category: 'professional',
      impact: '',
      evidence: null,
      is_public: false,
      tags: [],
      skills_used: [],
      metrics: {},
      external_links: []
    });
    setSelectedAccomplishment(null);
  };

  const filteredAccomplishments = accomplishments
    .filter(acc => filter === 'all' || acc.category === filter)
    .filter(acc => 
      acc.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      acc.description.toLowerCase().includes(searchTerm.toLowerCase())
    )
    .sort((a, b) => {
      if (sortBy === 'date') return new Date(b.date) - new Date(a.date);
      if (sortBy === 'title') return a.title.localeCompare(b.title);
      if (sortBy === 'category') return a.category.localeCompare(b.category);
      return 0;
    });

  const AccomplishmentCard = ({ accomplishment }) => {
    const category = categories.find(c => c.value === accomplishment.category);
    const CategoryIcon = category?.icon || FaTrophy;
    
    return (
      <DashboardCard
        title={
          <div className="d-flex align-items-center">
            <CategoryIcon className={`me-2 text-${category?.color}`} />
            {accomplishment.title}
          </div>
        }
        headerAction={
          <div className="d-flex align-items-center gap-2">
            {accomplishment.is_public ? 
              <Badge bg="success">Public</Badge> : 
              <Badge bg="secondary">Private</Badge>
            }
            {accomplishment.evidence_url && (
              <ActionButton
                icon={FaDownload}
                label="Download"
                variant="outline-info"
                size="sm"
                onClick={() => window.open(accomplishment.evidence_url)}
              />
            )}
          </div>
        }
      >
        <div>
          <p className="text-muted">{accomplishment.description}</p>
          {accomplishment.impact && (
            <Alert variant="success" className="py-2">
              <strong>Impact:</strong> {accomplishment.impact}
            </Alert>
          )}
          
          {accomplishment.tags && accomplishment.tags.length > 0 && (
            <div className="mb-2">
              {accomplishment.tags.map((tag, index) => (
                <Badge key={index} bg="light" text="dark" className="me-1">
                  {tag}
                </Badge>
              ))}
            </div>
          )}

          {accomplishment.skills_used && accomplishment.skills_used.length > 0 && (
            <div className="mb-2">
              <small className="text-muted">Skills: </small>
              {accomplishment.skills_used.map((skill, index) => (
                <Badge key={index} bg="info" className="me-1">
                  {skill}
                </Badge>
              ))}
            </div>
          )}

          <div className="d-flex justify-content-between align-items-center">
            <small className="text-muted">
              {formatDate(accomplishment.date)}
            </small>
            <div>
              <ActionButton
                icon={FaEdit}
                label="Edit"
                variant="outline-primary"
                size="sm"
                className="me-2"
                onClick={() => {
                  setSelectedAccomplishment(accomplishment);
                  setNewAccomplishment(accomplishment);
                  setShowModal(true);
                }}
              />
              <ActionButton
                icon={FaShare}
                label="Share"
                variant="outline-success"
                size="sm"
                className="me-2"
                onClick={() => handleShare(accomplishment)}
              />
              <ActionButton
                icon={FaTrash}
                label="Delete"
                variant="outline-danger"
                size="sm"
                onClick={() => handleDelete(accomplishment.id)}
              />
            </div>
          </div>
        </div>
      </DashboardCard>
    );
  };

  return (
    <Container style={{ fontFamily: 'Poppins', paddingTop: '30px' }}>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>My Accomplishments</h2>
        <ActionButton
          icon={FaPlus}
          label="Add Accomplishment"
          onClick={() => {
            resetForm();
            setShowModal(true);
          }}
        />
      </div>

      {/* Filters and Search */}
      <Card className="mb-4">
        <Card.Body>
          <Row>
            <Col md={4}>
              <Form.Group>
                <Form.Label><FaFilter className="me-2" />Filter by Category</Form.Label>
                <Form.Select
                  value={filter}
                  onChange={(e) => setFilter(e.target.value)}
                >
                  <option value="all">All Categories</option>
                  {categories.map(category => (
                    <option key={category.value} value={category.value}>
                      {category.label}
                    </option>
                  ))}
                </Form.Select>
              </Form.Group>
            </Col>
            <Col md={4}>
              <Form.Group>
                <Form.Label><FaSort className="me-2" />Sort By</Form.Label>
                <Form.Select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                >
                  <option value="date">Date</option>
                  <option value="title">Title</option>
                  <option value="category">Category</option>
                </Form.Select>
              </Form.Group>
            </Col>
            <Col md={4}>
              <Form.Group>
                <Form.Label><FaEye className="me-2" />Search</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Search accomplishments..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </Form.Group>
            </Col>
          </Row>
        </Card.Body>
      </Card>

      <Row>
        <Col md={8}>
          {loading ? (
            <div className="text-center">
              <div className="spinner-border" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
            </div>
          ) : filteredAccomplishments.length === 0 ? (
            <Alert variant="info">
              No accomplishments found. Add your first accomplishment to get started!
            </Alert>
          ) : (
            filteredAccomplishments.map(accomplishment => (
              <AccomplishmentCard 
                key={accomplishment.id} 
                accomplishment={accomplishment} 
              />
            ))
          )}
        </Col>

        <Col md={4}>
          <DashboardCard title="Accomplishments Summary">
            <div className="text-center mb-4">
              <FaTrophy size={40} className="text-warning mb-3" />
              <h3>{stats.total || 0}</h3>
              <p>Total Accomplishments</p>
            </div>
            
            <div className="mb-3">
              <div className="d-flex justify-content-between mb-1">
                <span>Public</span>
                <span>{stats.public_count || 0}</span>
              </div>
              <ProgressBar 
                now={stats.total ? (stats.public_count / stats.total) * 100 : 0} 
                variant="success" 
              />
            </div>

            <div className="mb-3">
              <div className="d-flex justify-content-between mb-1">
                <span>Recent (30 days)</span>
                <span>{stats.recent || 0}</span>
              </div>
              <ProgressBar 
                now={stats.total ? (stats.recent / stats.total) * 100 : 0} 
                variant="info" 
              />
            </div>

            <div>
              <h6>By Category</h6>
              {categories.map(category => (
                <div key={category.value} className="d-flex align-items-center mb-2">
                  <category.icon className={`me-2 text-${category.color}`} />
                  <span>{category.label}</span>
                  <div className="ms-auto">
                    {stats.by_category?.[category.value] || 0}
                  </div>
                </div>
              ))}
            </div>
          </DashboardCard>
        </Col>
      </Row>

      {/* Add/Edit Modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>
            {selectedAccomplishment ? 'Edit Accomplishment' : 'Add New Accomplishment'}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Row>
              <Col md={8}>
                <Form.Group className="mb-3">
                  <Form.Label>Title</Form.Label>
                  <Form.Control
                    type="text"
                    value={newAccomplishment.title}
                    onChange={(e) => setNewAccomplishment({
                      ...newAccomplishment,
                      title: e.target.value
                    })}
                  />
                </Form.Group>
              </Col>
              <Col md={4}>
                <Form.Group className="mb-3">
                  <Form.Label>Category</Form.Label>
                  <Form.Select
                    value={newAccomplishment.category}
                    onChange={(e) => setNewAccomplishment({
                      ...newAccomplishment,
                      category: e.target.value
                    })}
                  >
                    {categories.map(category => (
                      <option key={category.value} value={category.value}>
                        {category.label}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
            </Row>

            <Form.Group className="mb-3">
              <Form.Label>Description</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                value={newAccomplishment.description}
                onChange={(e) => setNewAccomplishment({
                  ...newAccomplishment,
                  description: e.target.value
                })}
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Impact</Form.Label>
              <Form.Control
                as="textarea"
                rows={2}
                value={newAccomplishment.impact}
                onChange={(e) => setNewAccomplishment({
                  ...newAccomplishment,
                  impact: e.target.value
                })}
                placeholder="Describe the impact of this accomplishment..."
              />
            </Form.Group>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Date</Form.Label>
                  <Form.Control
                    type="date"
                    value={newAccomplishment.date}
                    onChange={(e) => setNewAccomplishment({
                      ...newAccomplishment,
                      date: e.target.value
                    })}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Evidence</Form.Label>
                  <Form.Control
                    type="file"
                    onChange={(e) => setNewAccomplishment({
                      ...newAccomplishment,
                      evidence: e.target.files[0]
                    })}
                  />
                </Form.Group>
              </Col>
            </Row>

            <Form.Group className="mb-3">
              <Form.Label>Tags (comma-separated)</Form.Label>
              <Form.Control
                type="text"
                value={newAccomplishment.tags.join(', ')}
                onChange={(e) => setNewAccomplishment({
                  ...newAccomplishment,
                  tags: e.target.value.split(',').map(tag => tag.trim()).filter(tag => tag)
                })}
                placeholder="Enter tags separated by commas"
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Skills Used (comma-separated)</Form.Label>
              <Form.Control
                type="text"
                value={newAccomplishment.skills_used.join(', ')}
                onChange={(e) => setNewAccomplishment({
                  ...newAccomplishment,
                  skills_used: e.target.value.split(',').map(skill => skill.trim()).filter(skill => skill)
                })}
                placeholder="Enter skills separated by commas"
              />
            </Form.Group>

            <Form.Check
              type="switch"
              id="public-switch"
              label="Make this accomplishment public"
              checked={newAccomplishment.is_public}
              onChange={(e) => setNewAccomplishment({
                ...newAccomplishment,
                is_public: e.target.checked
              })}
            />
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <ActionButton
            variant="secondary"
            label="Cancel"
            onClick={() => setShowModal(false)}
          />
          <ActionButton
            label={selectedAccomplishment ? 'Update' : 'Add'}
            onClick={handleSubmit}
            disabled={loading}
          />
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default MyAccomplishments; 