import React from 'react';
import { getScoreColor, camelToTitle } from '../../utils/helpers';
import { Users, MessageCircle, Lightbulb, Zap, Clock, Target, Heart } from 'lucide-react';

interface SoftSkill {
  skill: string;
  confidence: number;
  evidence: string;
}

interface SoftSkillsData {
  leadership_management?: SoftSkill[];
  communication_collaboration?: SoftSkill[];
  problem_solving_analytical?: SoftSkill[];
  adaptability_learning?: SoftSkill[];
  time_management_organization?: SoftSkill[];
  creativity_innovation?: SoftSkill[];
  interpersonal_skills?: SoftSkill[];
  others?: SoftSkill[];
}

interface SoftSkillsDisplayProps {
  softSkills: SoftSkillsData;
}

interface SkillBadgeProps {
  children: React.ReactNode;
  className?: string;
}

const SkillBadge: React.FC<SkillBadgeProps> = ({ children, className = '' }) => {
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${className}`}>
      {children}
    </span>
  );
};

const categoryIcons: Record<string, React.ComponentType<{ className?: string }>> = {
  leadership_management: Users,
  communication_collaboration: MessageCircle,
  problem_solving_analytical: Lightbulb,
  adaptability_learning: Zap,
  time_management_organization: Clock,
  creativity_innovation: Target,
  interpersonal_skills: Heart,
};

const SoftSkillsDisplay: React.FC<SoftSkillsDisplayProps> = ({ softSkills }) => {
  const renderSkillCategory = (skills: SoftSkill[], categoryKey: string) => {
    if (!skills || skills.length === 0) return null;

    const categoryTitle = camelToTitle(categoryKey);
    const IconComponent = categoryIcons[categoryKey];

    return (
      <div key={categoryKey} className="mb-6">
        <div className="flex items-center mb-3">
          {IconComponent && <IconComponent className="h-5 w-5 text-primary-600 mr-2" />}
          <h4 className="text-lg font-semibold text-gray-900">{categoryTitle}</h4>
        </div>
        
        <div className="space-y-3">
          {skills.map((skill, index) => (
            <div
              key={index}
              className="border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow"
            >
              <div className="flex items-start justify-between mb-2">
                <h5 className="font-medium text-gray-900">{skill.skill}</h5>
                <SkillBadge className={`${getScoreColor(skill.confidence)} bg-gray-100 border border-gray-200`}>
                  {skill.confidence}% confidence
                </SkillBadge>
              </div>
              
              <p className="text-sm text-gray-600 italic">
                "{skill.evidence}"
              </p>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const hasAnySkills = Object.values(softSkills).some(skills => skills && skills.length > 0);

  if (!hasAnySkills) {
    return (
      <div className="card p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-6 border-b border-gray-200 pb-3">
          Soft Skills Analysis
        </h3>
        <div className="text-center py-8">
          <p className="text-gray-500">No soft skills detected in this CV.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card p-6">
      <h3 className="text-xl font-bold text-gray-900 mb-6 border-b border-gray-200 pb-3">
        Soft Skills Analysis
      </h3>
      
      <div className="space-y-6">
        {Object.entries(softSkills).map(([categoryKey, skills]) => 
          renderSkillCategory(skills, categoryKey)
        )}
      </div>
    </div>
  );
};

export default SoftSkillsDisplay;
