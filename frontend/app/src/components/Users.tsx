import { useEffect, useState } from "react";
import { getAccountUsers } from "../api"; // Suppose qu'on a une fonction API pour récupérer les utilisateurs
import { useParams } from "react-router-dom";

interface User {
  id: number;
  username: string;
  email: string;
}

const Users = () => {
  const { accountId } = useParams();

  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!accountId) return;

    const fetchUsers = async () => {
      try {
        const data = await getAccountUsers(accountId);
        setUsers(data); // Compter les utilisateurs
      } catch (err) {
        console.error("Error fetching users:", err);
        setError("Failed to load dashboard data.");
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, [accountId]);

  if (loading) {
    return <p>Loading users...</p>;
  }

  if (error) {
    return <p style={{ color: "red" }}>{error}</p>;
  }

  return (
    <div>
      <h1>User List</h1>
      <ul>
        {users.map((user) => (
          <li key={user.id}>
            <strong>{user.username}</strong> - {user.email}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Users;
