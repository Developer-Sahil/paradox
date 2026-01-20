import React from 'react';

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
}

const GlassCard: React.FC<GlassCardProps> = ({ children, className }) => {
  return (
    <div
      className={`bg-white bg-opacity-5 backdrop-blur-md rounded-xl shadow-glass-dark border border-white border-opacity-10 overflow-hidden ${className || ''}`}
    >
      {children}
    </div>
  );
};

export default GlassCard;
