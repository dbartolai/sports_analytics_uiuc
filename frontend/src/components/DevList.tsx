import type { Dev } from "../types/dev";
import "../styles/dev.css";

interface Props {
  devs: Dev[];
  onDelete: (id: number) => void;
  onEdit: (dev: Dev) => void;
}

export default function DevList({ devs, onDelete, onEdit }: Props) {
  if (devs.length === 0) {
    return (
      <div className="dev-list-container">
        <div className="empty-state">
          <div className="empty-state-icon">👥</div>
          <div className="empty-state-text">No developers yet</div>
          <div className="empty-state-subtext">Add your first developer to get started!</div>
        </div>
      </div>
    );
  }

  return (
    <div className="dev-list-container slide-in">
      <h2 className="dev-list-title">Developer Team</h2>
      <ul className="dev-list">
        {devs.map((dev) => (
          <li key={dev.id} className="dev-item">
            <div className="dev-info">
              <div className="dev-name">{dev.name}</div>
              <div className="dev-details">
                {dev.major} • Class of {dev.grad_year}
              </div>
              {dev.fun_fact && (
                <div className="dev-fun-fact">
                  💡 {dev.fun_fact}
                </div>
              )}
            </div>
            <div className="dev-actions">
              <button 
                onClick={() => onEdit(dev)}
                className="btn btn-secondary btn-small"
                aria-label={`Edit ${dev.name}`}
              >
                Edit
              </button>
              <button 
                onClick={() => onDelete(dev.id)}
                className="btn btn-danger btn-small"
                aria-label={`Delete ${dev.name}`}
              >
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
