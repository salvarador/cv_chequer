import React from 'react';
import { getScoreColor } from '../../utils/helpers';

interface Technology {
  name: string;
  probability: number;
}

interface CloudServices {
  aws?: Technology[];
  azure?: Technology[];
  gcp?: Technology[];
  others?: Technology[];
}

interface TechnologiesData {
  programming_languages: Technology[];
  cloud_services: CloudServices;
  databases: Technology[];
  devops_tools: Technology[];
  other_technologies: Technology[];
}

interface TechnologyDisplayProps {
  technologies: TechnologiesData;
}

interface BadgeProps {
  children: React.ReactNode;
  className?: string;
}

const TechBadge: React.FC<BadgeProps> = ({ children, className = '' }) => {
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${className}`}>
      {children}
    </span>
  );
};

const TechnologyDisplay: React.FC<TechnologyDisplayProps> = ({ technologies }) => {
  const renderTechnologyList = (items: Technology[], title: string) => {
    if (!items || items.length === 0) return null;

    return (
      <div className="mb-6">
        <h4 className="text-lg font-semibold text-gray-900 mb-3">{title}</h4>
        <div className="flex flex-wrap gap-2">
          {items.map((item, index) => (
            <TechBadge
              key={index}
              className={`${getScoreColor(item.probability)} bg-gray-100 border border-gray-200`}
            >
              <span className="font-medium">{item.name}</span>
              <span className="ml-1 text-xs">({item.probability}%)</span>
            </TechBadge>
          ))}
        </div>
      </div>
    );
  };

  const renderCloudServices = (cloudServices: CloudServices) => {
    const hasCloudServices = Object.values(cloudServices).some(services => services && services.length > 0);
    
    if (!hasCloudServices) return null;

    return (
      <div className="mb-6">
        <h4 className="text-lg font-semibold text-gray-900 mb-3">Cloud Services</h4>
        <div className="space-y-4">
          {Object.entries(cloudServices).map(([provider, services]) => {
            if (!services || services.length === 0) return null;
            
            const providerName = provider.toUpperCase();
            
            return (
              <div key={provider}>
                <h5 className="text-md font-medium text-gray-700 mb-2">{providerName}</h5>
                <div className="flex flex-wrap gap-2">
                  {services.map((service: Technology, index: number) => (
                    <TechBadge
                      key={index}
                      className={`${getScoreColor(service.probability)} bg-gray-100 border border-gray-200`}
                    >
                      <span className="font-medium">{service.name}</span>
                      <span className="ml-1 text-xs">({service.probability}%)</span>
                    </TechBadge>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  return (
    <div className="card p-6">
      <h3 className="text-xl font-bold text-gray-900 mb-6 border-b border-gray-200 pb-3">
        Technologies & Skills
      </h3>
      
      <div className="space-y-6">
        {renderTechnologyList(technologies.programming_languages, 'Programming Languages')}
        {renderCloudServices(technologies.cloud_services)}
        {renderTechnologyList(technologies.databases, 'Databases')}
        {renderTechnologyList(technologies.devops_tools, 'DevOps Tools')}
        {renderTechnologyList(technologies.other_technologies, 'Other Technologies')}
      </div>
    </div>
  );
};

export default TechnologyDisplay;
