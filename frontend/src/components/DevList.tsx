import type { Dev } from "../types/dev";

interface Props {
  devs: Dev[];
  onDelete: (id: number) => void;
  onEdit: (dev: Dev) => void;
}

export default function DevList({ devs, onDelete, onEdit }: Props) {
  return (
    <ul>
      {devs.map((d) => (
        <li key={d.id}>
          <strong>{d.name}</strong> – {d.major} d.grad_year
          {d.fun_fact && <em> ({d.fun_fact})</em>}
          <button onClick={() => onEdit(d)}>Edit</button>
          <button onClick={() => onDelete(d.id)}>Delete</button>
        </li>
      ))}
    </ul>
  );
}
