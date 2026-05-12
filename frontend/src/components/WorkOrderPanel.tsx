// WorkOrderPanel Component - Display work order info

import type { WorkOrder } from '../types';
import './WorkOrderPanel.css';

interface WorkOrderPanelProps {
  workOrder: WorkOrder;
}

export function WorkOrderPanel({ workOrder }: WorkOrderPanelProps) {
  return (
    <div className="work-order-panel">
      <div className="panel-header">
        <span className="panel-title">WORK ORDER</span>
        <span className="panel-status">ACTIVE</span>
      </div>
      <div className="panel-grid">
        <div className="panel-item">
          <span className="panel-label">Work Order #</span>
          <span className="panel-value">{workOrder.work_order_number}</span>
        </div>
        <div className="panel-item">
          <span className="panel-label">Part Number</span>
          <span className="panel-value">{workOrder.part_number}</span>
        </div>
        <div className="panel-item">
          <span className="panel-label">Lot Number</span>
          <span className="panel-value">{workOrder.lot_number}</span>
        </div>
        <div className="panel-item">
          <span className="panel-label">Customer</span>
          <span className="panel-value">{workOrder.customer}</span>
        </div>
      </div>
    </div>
  );
}