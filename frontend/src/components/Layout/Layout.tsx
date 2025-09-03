import React, { useState, useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import Header from './Header';
import Sidebar from './Sidebar';
import { apiService } from '../../services/api';

const Layout: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isApiConnected, setIsApiConnected] = useState(false);

  useEffect(() => {
    // Check API connection on mount
    const checkApiConnection = async () => {
      try {
        await apiService.healthCheck();
        setIsApiConnected(true);
      } catch (error) {
        setIsApiConnected(false);
        console.error('API connection failed:', error);
      }
    };

    checkApiConnection();
    
    // Check API connection periodically
    const interval = setInterval(checkApiConnection, 30000); // Every 30 seconds
    
    return () => clearInterval(interval);
  }, []);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const closeSidebar = () => {
    setSidebarOpen(false);
  };

  return (
    <div className="h-screen flex overflow-hidden bg-gray-100">
      <Sidebar isOpen={sidebarOpen} onClose={closeSidebar} />
      
      <div className="flex flex-col w-0 flex-1 overflow-hidden">
        <Header isSidebarOpen={sidebarOpen} toggleSidebar={toggleSidebar} />
        
        <main className="flex-1 relative overflow-y-auto focus:outline-none">
          <div className="py-6">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              {!isApiConnected && (
                <div className="mb-4 bg-red-50 border border-red-200 rounded-md p-4">
                  <div className="flex">
                    <div className="flex-shrink-0">
                      <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <div className="ml-3">
                      <h3 className="text-sm font-medium text-red-800">
                        API Connection Failed
                      </h3>
                      <div className="mt-2 text-sm text-red-700">
                        <p>Unable to connect to the CV Chequer API. Please ensure the backend server is running.</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              
              <Outlet />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;
