import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout/Layout';
import Dashboard from './pages/Dashboard';
import CVAnalysis from './pages/CVAnalysis';

// Placeholder components for other pages
const JobMatching = () => (
  <div className="text-center py-12">
    <h1 className="text-2xl font-bold text-gray-900 mb-4">Job Matching</h1>
    <p className="text-gray-600">This feature will be implemented soon.</p>
  </div>
);

const BatchAnalysis = () => (
  <div className="text-center py-12">
    <h1 className="text-2xl font-bold text-gray-900 mb-4">Batch Analysis</h1>
    <p className="text-gray-600">This feature will be implemented soon.</p>
  </div>
);

const BatchMatching = () => (
  <div className="text-center py-12">
    <h1 className="text-2xl font-bold text-gray-900 mb-4">Batch Matching</h1>
    <p className="text-gray-600">This feature will be implemented soon.</p>
  </div>
);

const JobAnalysis = () => (
  <div className="text-center py-12">
    <h1 className="text-2xl font-bold text-gray-900 mb-4">Job Analysis</h1>
    <p className="text-gray-600">This feature will be implemented soon.</p>
  </div>
);

const Reports = () => (
  <div className="text-center py-12">
    <h1 className="text-2xl font-bold text-gray-900 mb-4">Reports</h1>
    <p className="text-gray-600">This feature will be implemented soon.</p>
  </div>
);

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="cv-analysis" element={<CVAnalysis />} />
          <Route path="job-matching" element={<JobMatching />} />
          <Route path="batch-analysis" element={<BatchAnalysis />} />
          <Route path="batch-matching" element={<BatchMatching />} />
          <Route path="job-analysis" element={<JobAnalysis />} />
          <Route path="reports" element={<Reports />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;