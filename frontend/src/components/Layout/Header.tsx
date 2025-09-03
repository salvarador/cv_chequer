import React from 'react';
import { Menu, X, FileText, Activity } from 'lucide-react';

interface HeaderProps {
  isSidebarOpen: boolean;
  toggleSidebar: () => void;
}

const Header: React.FC<HeaderProps> = ({ isSidebarOpen, toggleSidebar }) => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <button
              type="button"
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500 lg:hidden"
              onClick={toggleSidebar}
            >
              <span className="sr-only">Toggle sidebar</span>
              {isSidebarOpen ? (
                <X className="block h-6 w-6" aria-hidden="true" />
              ) : (
                <Menu className="block h-6 w-6" aria-hidden="true" />
              )}
            </button>
            
            <div className="flex-shrink-0 flex items-center ml-4 lg:ml-0">
              <div className="flex items-center space-x-2">
                <div className="flex items-center justify-center w-8 h-8 bg-primary-600 rounded-lg">
                  <FileText className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-gray-900">CV Chequer</h1>
                  <p className="text-xs text-gray-500">AI-Powered CV Analysis</p>
                </div>
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            {/* Health Status Indicator */}
            <div className="flex items-center space-x-2">
              <Activity className="w-4 h-4 text-green-500" />
              <span className="text-sm text-gray-600 hidden sm:inline">API Connected</span>
            </div>

            {/* Version */}
            <div className="hidden md:flex items-center">
              <span className="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-800 rounded-full">
                v{import.meta.env.VITE_APP_VERSION || '1.0.0'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
