import { useEffect, useState } from "react";
import { listDevs, deleteDev } from "../services/dev";
import type { Dev } from "../types/dev";
import DevForm from "../forms/DevCreate";
import DevList from "../components/DevList";
import DevEdit from "../forms/DevEdit";

export default function DevPage() {
  const [devs, setDevs] = useState<Dev[]>([]);
  const [editing, setEditing] = useState<Dev | null>(null);

  useEffect(() => {
    listDevs().then(setDevs);
  }, []);

  const handleCreated = (dev: Dev) => setDevs([...devs, dev]);
  const handleDeleted = async (id: number) => {
    await deleteDev(id);
    setDevs(devs.filter((d) => d.id !== id));
  };
  const handleUpdated = (dev: Dev) => {
    setDevs(devs.map((d) => (d.id === dev.id ? dev : d)));
    setEditing(null);
  };

  return (
    <div>
      <h1>Meet the Devs</h1>
      {editing ? (
        <DevEdit dev={editing} onUpdated={handleUpdated} onCancel={() => setEditing(null)} />
      ) : (
        <DevForm onCreated={handleCreated} />
      )}
      <DevList devs={devs} onDelete={handleDeleted} onEdit={setEditing} />
    </div>
  );
}
