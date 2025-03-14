import { useState } from 'react';
import './App.css';
import UrlSubmitForm from './components/UrlSubmitForm';
import TaskStatusMonitor from './components/TaskStatusMonitor';
import ScrapingResultsDisplay from './components/ScrapingResultsDisplay';

function App() {
  const [currentTaskId, setCurrentTaskId] = useState<number | null>(null);
  const [showResults, setShowResults] = useState(false);

  const handleTaskCreated = (taskId: number) => {
    setCurrentTaskId(taskId);
    setShowResults(false);
  };

  const handleTaskCompleted = () => {
    setShowResults(true);
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Web Scraper Application</h1>
        <p>Submit a URL and get information about the webpage</p>
      </header>

      <main className="app-main">
        <section className="section">
          <UrlSubmitForm onTaskCreated={handleTaskCreated} />
        </section>

        {currentTaskId && (
          <section className="section">
            <TaskStatusMonitor 
              taskId={currentTaskId}
              onTaskCompleted={handleTaskCompleted}
            />
          </section>
        )}

        {showResults && currentTaskId && (
          <section className="section">
            <ScrapingResultsDisplay taskId={currentTaskId} />
          </section>
        )}
      </main>

      <footer className="app-footer">
        <p>© 2025 Web Scraper App - Built with React, FastAPI and Celery</p>
      </footer>
    </div>
  );
}

export default App;
