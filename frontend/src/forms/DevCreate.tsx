import { useState } from "react";
import { createDev } from "../services/dev";
import type { Dev, DevCreate } from "../types/dev";
import "../styles/dev.css";

interface Props {
  onCreated: (dev: Dev) => void;
}

export default function DevForm({ onCreated }: Props) {
  const [form, setForm] = useState<DevCreate>({ name: "", major: "", grad_year: 2025, fun_fact: "" });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      const newDev = await createDev(form);
      onCreated(newDev);
      setForm({ name: "", major: "", grad_year: 2025, fun_fact: "" });
    } catch (error) {
      console.error("Error creating dev:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="dev-form-container fade-in">
      <h2 className="dev-form-title">Add New Developer</h2>
      <form onSubmit={handleSubmit} className="dev-form">
        <div className="form-group">
          <label htmlFor="dev-name" className="form-label">
            Full Name
          </label>
          <input
            id="dev-name"
            name="name"
            type="text"
            className="form-input"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            placeholder="Enter full name"
            required
            autoComplete="name"
            disabled={isSubmitting}
          />
        </div>

        <div className="form-group">
          <label htmlFor="dev-major" className="form-label">
            Major
          </label>
          <input
            id="dev-major"
            name="major"
            type="text"
            className="form-input"
            value={form.major}
            onChange={(e) => setForm({ ...form, major: e.target.value })}
            placeholder="e.g., Computer Science"
            required
            disabled={isSubmitting}
          />
        </div>

        <div className="form-group">
          <label htmlFor="dev-grad-year" className="form-label">
            Graduation Year
          </label>
          <input
            id="dev-grad-year"
            name="grad_year"
            type="number"
            className="form-input"
            value={form.grad_year}
            onChange={(e) => setForm({ ...form, grad_year: parseInt(e.target.value) || 2025 })}
            placeholder="2025"
            min="2020"
            max="2030"
            required
            disabled={isSubmitting}
          />
        </div>

        <div className="form-group">
          <label htmlFor="dev-fun-fact" className="form-label">
            Fun Fact <span style={{ color: "#6c757d", fontWeight: "normal" }}>(Optional)</span>
          </label>
          <input
            id="dev-fun-fact"
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
            {isSubmitting ? "Adding..." : "Add Developer"}
          </button>
        </div>
      </form>
    </div>
  );
}
