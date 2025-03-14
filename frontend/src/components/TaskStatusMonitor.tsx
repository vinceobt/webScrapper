import { useState, useEffect } from 'react';
import { apiService } from '../services/api';

interface TaskStatusMonitorProps {
  taskId: number | null;
  onTaskCompleted: () => void;
}

const TaskStatusMonitor: React.FC<TaskStatusMonitorProps> = ({ taskId, onTaskCompleted }) => {
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pollingInterval, setPollingInterval] = useState<number | null>(null);

  useEffect(() => {
    // Clear any existing polling interval when component unmounts or taskId changes
    return () => {
      if (pollingInterval) {
        clearInterval(pollingInterval);
      }
    };
  }, []);

  useEffect(() => {
    // If no task ID, don't do anything
    if (!taskId) {
      setStatus(null);
      return;
    }

    // Start with an immediate status check
    checkTaskStatus();

    // Set up polling every 2 seconds
    const intervalId = window.setInterval(checkTaskStatus, 2000);
    setPollingInterval(intervalId);

    // Cleanup function to clear interval when component unmounts or taskId changes
    return () => {
      clearInterval(intervalId);
      setPollingInterval(null);
    };
  }, [taskId]);

  const checkTaskStatus = async () => {
    if (!taskId) return;

    try {
      const taskStatus = await apiService.getTaskStatus(taskId);
      setStatus(taskStatus.status);
      
      // If task is completed or failed, stop polling
      if (taskStatus.status === 'completed' || taskStatus.status === 'failed') {
        if (pollingInterval) {
          clearInterval(pollingInterval);
          setPollingInterval(null);
        }
        
        if (taskStatus.status === 'completed') {
          onTaskCompleted();
        }
        
        if (taskStatus.status === 'failed' && taskStatus.error_message) {
          setError(`Scraping failed: ${taskStatus.error_message}`);
        }
      }
    } catch (err) {
      console.error('Error checking task status:', err);
      setError('Failed to check task status');
      
      // Stop polling on error
      if (pollingInterval) {
        clearInterval(pollingInterval);
        setPollingInterval(null);
      }
    }
  };

  if (!taskId || !status) {
    return null;
  }

  return (
    <div className="task-status-monitor">
      <h3>Task Status</h3>
      <div className="status-container">
        <div className="status-label">Status:</div>
        <div className={`status-value status-${status}`}>
          {status === 'pending' && 'Pending'}
          {status === 'in_progress' && 'Scraping in progress...'}
          {status === 'completed' && 'Scraping completed successfully'}
          {status === 'failed' && 'Scraping failed'}
        </div>
        {error && <div className="error-message">{error}</div>}
        
        {(status === 'pending' || status === 'in_progress') && (
          <div className="progress-indicator">
            <div className="spinner"></div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TaskStatusMonitor;