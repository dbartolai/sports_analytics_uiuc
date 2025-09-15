import type { Dev, DevCreate, DevUpdate } from "../types/dev.ts";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function listDevs(): Promise<Dev[]> {
  const res = await fetch(`${API_URL}/devs`);
  return res.json();
}

export async function createDev(data: DevCreate): Promise<Dev> {
  const res = await fetch(`${API_URL}devs/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

export async function updateDev(id: number, data: DevUpdate): Promise<Dev> {
  const res = await fetch(`${API_URL}devs/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

export async function deleteDev(id: number): Promise<void> {
  await fetch(`${API_URL}/devs/${id}`, { method: "DELETE" });
}
