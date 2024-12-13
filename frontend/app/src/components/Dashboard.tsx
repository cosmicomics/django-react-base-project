import { useEffect, useState } from "react";
import { getAccountInputs, getAccountUsers, getUsers } from "../api"; // Suppose que nous récupérons aussi des utilisateurs pour ce dashboard
import { useParams } from "react-router-dom";
import Chart from "./chart/Chart";

interface User {
  id: number;
  username: string;
}

const Dashboard = () => {
  const { accountId } = useParams();

  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const [userCount, setUserCount] = useState<number>(0);
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    if (!accountId) return;

    const fetchUsers = async () => {
      try {
        const data = await getAccountUsers(accountId);
        setUserCount(data.length); // Compter les utilisateurs
      } catch (err) {
        console.error("Error fetching users:", err);
        setError("Failed to load dashboard data.");
      } finally {
        setLoading(false);
      }
    };

    const fetchData = async () => {
      try {
        const data = await getAccountInputs(accountId);
        setData(data);
        console.log(data);
      } catch (err) {
        console.error("Error fetching users:", err);
        setError("Failed to load dashboard data.");
      } finally {
        setLoading(false);
      }
    };

    //fetchUsers();
    fetchData();
  }, [accountId]);

  if (loading) {
    return <p>Loading dashboard...</p>;
  }

  if (error) {
    return <p style={{ color: "red" }}>{error}</p>;
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Number of users: {userCount}</p>
      <Chart data={data} />
    </div>
  );
};

export default Dashboard;
