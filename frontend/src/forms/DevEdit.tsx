import { useState } from "react";
import { updateDev } from "../services/dev";
import type { Dev, DevUpdate } from "../types/dev";
import "../styles/dev.css";

interface Props {
  dev: Dev;
  onUpdated: (dev: Dev) => void;
  onCancel: () => void;
}

export default function DevEditForm({ dev, onUpdated, onCancel }: Props) {
  const [form, setForm] = useState<DevUpdate>({
    name: dev.name,
    major: dev.major,
    grad_year: dev.grad_year,
    fun_fact: dev.fun_fact,
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      const updated = await updateDev(dev.id, form);
      onUpdated(updated);
    } catch (error) {
      console.error("Error updating dev:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="dev-form-container fade-in">
      <h2 className="dev-form-title">Edit Developer</h2>
      <form onSubmit={handleSubmit} className="dev-form">
        <div className="form-group">
          <label htmlFor="edit-dev-name" className="form-label">
            Full Name
          </label>
          <input
            id="edit-dev-name"
            name="name"
            type="text"
            className="form-input"
            value={form.name || ""}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            placeholder="Enter full name"
            required
            autoComplete="name"
            disabled={isSubmitting}
          />
        </div>

        <div className="form-group">
          <label htmlFor="edit-dev-major" className="form-label">
            Major
          </label>
          <input
            id="edit-dev-major"
            name="major"
            type="text"
            className="form-input"
            value={form.major || ""}
            onChange={(e) => setForm({ ...form, major: e.target.value })}
            placeholder="e.g., Computer Science"
            required
            disabled={isSubmitting}
          />
        </div>

        <div className="form-group">
          <label htmlFor="edit-dev-grad-year" className="form-label">
            Graduation Year
          </label>
          <input
            id="edit-dev-grad-year"
            name="grad_year"
            type="number"
            className="form-input"
            value={form.grad_year || 0}
            onChange={(e) => setForm({ ...form, grad_year: Number(e.target.value) })}
            placeholder="2025"
            min="2020"
            max="2030"
            required
            disabled={isSubmitting}
          />
        </div>

        <div className="form-group">
          <label htmlFor="edit-dev-fun-fact" className="form-label">
            Fun Fact <span style={{ color: "#6c757d", fontWeight: "normal" }}>(Optional)</span>
          </label>
          <input
            id="edit-dev-fun-fact"
            name="fun_fact"
            type="text"
            className="form-input"
            value={form.fun_fact || ""}
            onChange={(e) => setForm({ ...form, fun_fact: e.target.value })}
            placeholder="Share something interesting about yourself"
            disabled={isSubmitting}
          />
        </div>

        <div className="form-actions">
          <button 
            type="submit" 
            className="btn btn-primary"
            disabled={isSubmitting}
          >
            {isSubmitting ? "Saving..." : "Save Changes"}
          </button>
          <button 
            type="button" 
            onClick={onCancel}
            className="btn btn-secondary"
            disabled={isSubmitting}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
