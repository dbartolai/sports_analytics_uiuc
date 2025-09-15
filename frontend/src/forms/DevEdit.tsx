import { useState } from "react";
import { updateDev } from "../services/dev";
import type { Dev, DevUpdate } from "../types/dev";

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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const updated = await updateDev(dev.id, form);
    onUpdated(updated);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={form.name || ""}
        onChange={(e) => setForm({ ...form, name: e.target.value })}
      />
      <input
        value={form.major || ""}
        onChange={(e) => setForm({ ...form, major: e.target.value })}
      />
      <input
        value={form.grad_year || 0}
        onChange={(e) => setForm({ ...form, grad_year: Number(e.target.value) })}
      />
      <input
        value={form.fun_fact || ""}
        onChange={(e) => setForm({ ...form, fun_fact: e.target.value })}
      />
      <button type="submit">Save</button>
      <button type="button" onClick={onCancel}>Cancel</button>
    </form>
  );
}
