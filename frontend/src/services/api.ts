import axios from 'axios';

// API configuration
const API_URL = 'http://localhost:8000/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types for API responses
export interface ScrapingTask {
  id: number;
  url: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  created_at: string;
  completed_at?: string;
  error_message?: string;
}

export interface ScrapingResult {
  id: number;
  task_id: number;
  content: {
    title: string;
    meta_description: string;
    url: string;
    links_count: number;
    images_count: number;
    links: string[];
    images: string[];
  };
  html_content?: string;
  created_at: string;
}

export interface TaskWithResults extends ScrapingTask {
  results: ScrapingResult[];
}

// API service functions
export const apiService = {
  // Submit URL for scraping
  submitUrl: async (url: string): Promise<ScrapingTask> => {
    const response = await apiClient.post('/scrape', { url });
    return response.data;
  },

  // Get task status
  getTaskStatus: async (taskId: number): Promise<{ id: number; status: string; error_message?: string }> => {
    const response = await apiClient.get(`/task-status/${taskId}`);
    return response.data;
  },

  // Get task with results
  getTaskWithResults: async (taskId: number): Promise<TaskWithResults> => {
    const response = await apiClient.get(`/tasks/${taskId}`);
    return response.data;
  },

  // Get all tasks
  getAllTasks: async (): Promise<ScrapingTask[]> => {
    const response = await apiClient.get('/tasks');
    return response.data;
  },
};

export default apiService;