import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  FileText, 
  Search, 
  BarChart3, 
  Users, 
  Home,
  Upload,
  FileSearch
} from 'lucide-react';
import { type NavigationItem } from '../../types';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const navigation: NavigationItem[] = [
  { name: 'Dashboard', href: '/', icon: Home, current: false },
  { name: 'CV Analysis', href: '/cv-analysis', icon: FileText, current: false },
  { name: 'Job Matching', href: '/job-matching', icon: FileSearch, current: false },
  { name: 'Batch Analysis', href: '/batch-analysis', icon: Upload, current: false },
  { name: 'Batch Matching', href: '/batch-matching', icon: Users, current: false },
  { name: 'Job Analysis', href: '/job-analysis', icon: Search, current: false },
  { name: 'Reports', href: '/reports', icon: BarChart3, current: false },
];

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const location = useLocation();

  const navigationWithCurrent = navigation.map(item => ({
    ...item,
    current: location.pathname === item.href
  }));

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div className="fixed inset-0 flex z-40 lg:hidden">
          <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={onClose} />
          <div className="relative flex-1 flex flex-col max-w-xs w-full bg-white">
            <div className="absolute top-0 right-0 -mr-12 pt-2">
              <button
                type="button"
                className="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
                onClick={onClose}
              >
                <span className="sr-only">Close sidebar</span>
                <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <SidebarContent navigation={navigationWithCurrent} />
          </div>
        </div>
      )}

      {/* Desktop sidebar */}
      <div className="hidden lg:flex lg:flex-shrink-0">
        <div className="flex flex-col w-64">
          <div className="flex flex-col h-0 flex-1 bg-white border-r border-gray-200">
            <SidebarContent navigation={navigationWithCurrent} />
          </div>
        </div>
      </div>
    </>
  );
};

interface SidebarContentProps {
  navigation: NavigationItem[];
}

const SidebarContent: React.FC<SidebarContentProps> = ({ navigation }) => {
  return (
    <div className="flex flex-col flex-1 pt-5 pb-4 overflow-y-auto">
      <nav className="mt-5 flex-1 px-2 space-y-1">
        {navigation.map((item) => {
          const Icon = item.icon;
          return (
            <Link
              key={item.name}
              to={item.href}
              className={`${
                item.current
                  ? 'bg-primary-50 border-primary-500 text-primary-700'
                  : 'border-transparent text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              } group flex items-center px-3 py-2 text-sm font-medium border-l-4 transition-colors duration-150`}
            >
              {Icon && (
                <Icon
                  className={`${
                    item.current ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500'
                  } mr-3 h-5 w-5`}
                  aria-hidden="true"
                />
              )}
              {item.name}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="flex-shrink-0 flex border-t border-gray-200 p-4">
        <div className="flex-shrink-0 w-full group block">
          <div className="flex items-center">
            <div className="ml-3">
              <p className="text-xs font-medium text-gray-700 group-hover:text-gray-900">
                Powered by AWS
              </p>
              <p className="text-xs font-medium text-gray-500 group-hover:text-gray-700">
                Textract & Bedrock
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
