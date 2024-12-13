import axios from "axios";
import { getAuth } from "firebase/auth";

const authConfig = async () => {
  const auth = getAuth();
  const token = await auth.currentUser?.getIdToken();
  if (!token) {
    throw new Error("No token available. User might not be authenticated.");
  }
  return {
    headers: {
      Authorization: `Bearer ${token}`, // Set the token in the header
    },
  };
};

const api = axios.create({
  baseURL: "http://localhost:8000/api/", // API endpoint
  // withCredentials: true, // Only if cookies are needed for authentication
});

export const getAccountUsers = async (accountId: string) => {
  const response = await api.get(
    `accounts/${accountId}/users/`,
    await authConfig()
  );
  return response.data;
};

export const getAccountInputs = async (accountId: string) => {
  const response = await api.get(
    `accounts/${accountId}/inputs/`,
    await authConfig()
  );
  return response.data;
};

// Exemple de requête GET pour récupérer les utilisateurs
export const getUsers = async () => {
  const response = await api.get("/users/", await authConfig());
  return response.data;
};

// Exemple de requête POST pour envoyer des données
export const createUser = async (data: any) => {
  const response = await api.post("/users/", data, await authConfig());
  return response.data;
};
