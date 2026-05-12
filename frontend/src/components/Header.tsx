// Header Component - Industrial styled header

import './Header.css';

interface HeaderProps {
  workOrderNumber?: string;
}

export function Header({ workOrderNumber }: HeaderProps) {
  return (
    <header className="header">
      <div className="header-content">
        <div className="header-title">
          <span className="header-icon">◆</span>
          <span className="header-text">COC INSPECTOR</span>
        </div>
        <div className="header-status">
          {workOrderNumber && (
            <span className="header-wo">WO: {workOrderNumber}</span>
          )}
          <span className="header-badge">QA SYSTEM v1.0</span>
        </div>
      </div>
    </header>
  );
}