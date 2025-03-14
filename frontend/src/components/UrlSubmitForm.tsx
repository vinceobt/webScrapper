import { useState } from 'react';
import { apiService } from '../services/api';

interface UrlSubmitFormProps {
  onTaskCreated: (taskId: number) => void;
}

const UrlSubmitForm: React.FC<UrlSubmitFormProps> = ({ onTaskCreated }) => {
  const [url, setUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Validate URL format
  const isValidUrl = (urlString: string) => {
    try {
      new URL(urlString);
      return true;
    } catch (error) {
      return false;
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Reset error state
    setError(null);
    
    // Validate URL
    if (!url) {
      setError('Please enter a URL');
      return;
    }
    
    if (!isValidUrl(url)) {
      setError('Please enter a valid URL (e.g., https://example.com)');
      return;
    }
    
    // Submit URL to backend
    try {
      setIsLoading(true);
      const task = await apiService.submitUrl(url);
      onTaskCreated(task.id);
      setUrl(''); // Clear input after successful submission
    } catch (err) {
      setError('Failed to submit URL for scraping. Please try again.');
      console.error('Error submitting URL:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="url-submit-form">
      <h2>Submit URL for Scraping</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter URL (e.g., https://example.com)"
            disabled={isLoading}
            className="url-input"
          />
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        <button 
          type="submit" 
          disabled={isLoading}
          className="submit-button"
        >
          {isLoading ? 'Submitting...' : 'Scrape URL'}
        </button>
      </form>
    </div>
  );
};

export default UrlSubmitForm;