import { useState } from "react";
import { createDev } from "../services/dev";
import type { Dev, DevCreate } from "../types/dev";

interface Props {
  onCreated: (dev: Dev) => void;
}

export default function DevForm({ onCreated }: Props) {
  const [form, setForm] = useState<DevCreate>({ name: "", major: "", grad_year: 2025, fun_fact: "" });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const newDev = await createDev(form);
    onCreated(newDev);
    setForm({ name: "", major: "", grad_year: 2025, fun_fact: "" });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={form.name}
        onChange={(e) => setForm({ ...form, name: e.target.value })}
        placeholder="Name"
        required
      />
      <input
        value={form.major}
        onChange={(e) => setForm({ ...form, major: e.target.value })}
        placeholder="Major"
        required
      />
      <input
        value={form.grad_year}
        onChange={(e) => setForm({ ...form, major: e.target.value })}
        placeholder="Grad Year"
        required
      />
      <input
        value={form.fun_fact || ""}
        onChange={(e) => setForm({ ...form, fun_fact: e.target.value })}
        placeholder="Fun fact"
      />
      <button type="submit">Add Dev</button>
    </form>
  );
}
