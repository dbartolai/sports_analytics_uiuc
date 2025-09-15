import { useEffect, useState } from "react";
import { listDevs, deleteDev } from "../services/dev";
import type { Dev } from "../types/dev";
import DevForm from "../forms/DevCreate";
import DevList from "../components/DevList";
import DevEdit from "../forms/DevEdit";
import "../styles/dev.css";

export default function DevPage() {
  const [devs, setDevs] = useState<Dev[]>([]);
  const [editing, setEditing] = useState<Dev | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDevs = async () => {
      try {
        const data = await listDevs();
        setDevs(data);
      } catch (error) {
        console.error("Error loading devs:", error);
      } finally {
        setLoading(false);
      }
    };

    loadDevs();
  }, []);

  const handleCreated = (dev: Dev) => setDevs([...devs, dev]);
  
  const handleDeleted = async (id: number) => {
    try {
      await deleteDev(id);
      setDevs(devs.filter((d) => d.id !== id));
    } catch (error) {
      console.error("Error deleting dev:", error);
    }
  };
  
  const handleUpdated = (dev: Dev) => {
    setDevs(devs.map((d) => (d.id === dev.id ? dev : d)));
    setEditing(null);
  };

  return (
    <div className="dev-page">
      <h1>Meet out Devs</h1>
      
      {editing ? (
        <DevEdit 
          dev={editing} 
          onUpdated={handleUpdated} 
          onCancel={() => setEditing(null)} 
        />
      ) : (
        <DevForm onCreated={handleCreated} />
      )}
      
      {loading ? (
        <div className="loading">
          <div className="loading-spinner"></div>
          Loading developers...
        </div>
      ) : (
        <DevList 
          devs={devs} 
          onDelete={handleDeleted} 
          onEdit={setEditing} 
        />
      )}
    </div>
  );
}
