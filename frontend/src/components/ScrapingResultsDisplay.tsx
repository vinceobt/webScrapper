import { useEffect, useState } from 'react';
import { apiService, TaskWithResults, ScrapingResult } from '../services/api';

interface ScrapingResultsDisplayProps {
  taskId: number | null;
}

const ScrapingResultsDisplay: React.FC<ScrapingResultsDisplayProps> = ({ taskId }) => {
  const [results, setResults] = useState<ScrapingResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState('summary');

  useEffect(() => {
    const fetchResults = async () => {
      if (!taskId) return;
      
      try {
        setLoading(true);
        setError(null);
        
        const task = await apiService.getTaskWithResults(taskId);
        if (task.results && task.results.length > 0) {
          setResults(task.results[0]);
        } else {
          setError("No results found for this task");
        }
      } catch (err) {
        console.error('Error fetching results:', err);
        setError('Failed to load results');
      } finally {
        setLoading(false);
      }
    };

    fetchResults();
  }, [taskId]);

  if (!taskId) {
    return null;
  }

  if (loading) {
    return <div className="loading">Loading results...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  if (!results) {
    return <div>No results available yet.</div>;
  }

  const { content } = results;

  return (
    <div className="scraping-results">
      <h2>Scraping Results</h2>
      
      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'summary' ? 'active' : ''}`}
          onClick={() => setActiveTab('summary')}
        >
          Summary
        </button>
        <button 
          className={`tab ${activeTab === 'links' ? 'active' : ''}`}
          onClick={() => setActiveTab('links')}
        >
          Links ({content.links_count})
        </button>
        <button 
          className={`tab ${activeTab === 'images' ? 'active' : ''}`}
          onClick={() => setActiveTab('images')}
        >
          Images ({content.images_count})
        </button>
      </div>
      
      <div className="tab-content">
        {activeTab === 'summary' && (
          <div className="summary">
            <h3>Page Information</h3>
            <table className="info-table">
              <tbody>
                <tr>
                  <td><strong>Page Title:</strong></td>
                  <td>{content.title}</td>
                </tr>
                <tr>
                  <td><strong>URL:</strong></td>
                  <td>
                    <a href={content.url} target="_blank" rel="noopener noreferrer">
                      {content.url}
                    </a>
                  </td>
                </tr>
                <tr>
                  <td><strong>Meta Description:</strong></td>
                  <td>{content.meta_description || 'Not available'}</td>
                </tr>
                <tr>
                  <td><strong>Total Links:</strong></td>
                  <td>{content.links_count}</td>
                </tr>
                <tr>
                  <td><strong>Total Images:</strong></td>
                  <td>{content.images_count}</td>
                </tr>
              </tbody>
            </table>
          </div>
        )}
        
        {activeTab === 'links' && (
          <div className="links-list">
            <h3>Links Found ({content.links_count})</h3>
            {content.links && content.links.length > 0 ? (
              <ul>
                {content.links.map((link, index) => (
                  <li key={index}>
                    <a href={link} target="_blank" rel="noopener noreferrer">
                      {link}
                    </a>
                  </li>
                ))}
              </ul>
            ) : (
              <p>No links found</p>
            )}
          </div>
        )}
        
        {activeTab === 'images' && (
          <div className="images-list">
            <h3>Images Found ({content.images_count})</h3>
            {content.images && content.images.length > 0 ? (
              <div className="image-grid">
                {content.images.map((img, index) => (
                  <div className="image-item" key={index}>
                    <img 
                      src={img.startsWith('http') ? img : `${content.url.replace(/\/$/, '')}${img}`} 
                      alt={`Image ${index + 1}`}
                      onError={(e) => {
                        const target = e.target as HTMLImageElement;
                        target.onerror = null; 
                        target.style.display = 'none';
                      }}
                    />
                    <div className="image-url">{img}</div>
                  </div>
                ))}
              </div>
            ) : (
              <p>No images found</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ScrapingResultsDisplay;