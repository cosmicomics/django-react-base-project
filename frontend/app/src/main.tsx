import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import Login from "./components/Login.tsx";
import ProtectedRoute from "./components/ProtectedRoute.tsx";
import Dashboard from "./components/Dashboard.tsx";
import Users from "./components/Users.tsx";

const router = createBrowserRouter([
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/",
    element: <ProtectedRoute />,
    children: [
      {
        path: "/accounts/:accountId",
        element: <App />,
        children: [
          {
            path: "",
            element: <Dashboard />,
          },
          {
            path: "dashboard",
            element: <Dashboard />,
          },
          {
            path: "users",
            element: <Users />,
          },
        ],
      },
    ],
  },
]);

createRoot(document.getElementById("root")!).render(
  <RouterProvider router={router} />
);
