import type { Dev, DevCreate, DevUpdate } from "../types/dev.ts";

// Ensure consistent URL formatting with trailing slash
const API_URL = (import.meta.env.VITE_API_URL || "http://localhost:8000").replace(/\/$/, '') + '/';

console.log('API_URL configured as:', API_URL);

export async function listDevs(): Promise<Dev[]> {
  try {
    console.log('Fetching from:', `${API_URL}devs/`);
    const res = await fetch(`${API_URL}devs/`);
    
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    }
    
    return res.json();
  } catch (error) {
    console.error('Error in listDevs:', error);
    throw error;
  }
}

export async function createDev(data: DevCreate): Promise<Dev> {
  try {
    console.log('Creating dev at:', `${API_URL}devs/`, 'with data:', data);
    const res = await fetch(`${API_URL}devs/`, {  // Removed trailing slash
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    
    console.log('Response status:', res.status);
    
    if (!res.ok) {
      const errorText = await res.text();
      console.error('Error response:', errorText);
      throw new Error(`HTTP ${res.status}: ${errorText}`);
    }
    
    return res.json();
  } catch (error) {
    console.error('Error in createDev:', error);
    throw error;
  }
}

export async function updateDev(id: number, data: DevUpdate): Promise<Dev> {
  try {
    const res = await fetch(`${API_URL}devs/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    }
    
    return res.json();
  } catch (error) {
    console.error('Error in updateDev:', error);
    throw error;
  }
}

export async function deleteDev(id: number): Promise<void> {
  try {
    const res = await fetch(`${API_URL}devs/${id}`, { method: "DELETE" });
    
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    }
  } catch (error) {
    console.error('Error in deleteDev:', error);
    throw error;
  }
}
