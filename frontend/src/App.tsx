import { RouterProvider } from "react-router/dom";
import { createBrowserRouter } from "react-router";

import Login from "./views/auth/Login";
import LandingPage from "./views/LandingPage";
import ProtectedRoute from "./components/ProtectedRoute";
import AdminDashboard from "./views/admin/Dashboard";
import AdminNavbar from "./components/AdminNavbar";
import AdminCompanyList from "./views/admin/CompanyList";

const router = createBrowserRouter([
  { path: "/", Component: LandingPage },
  {
    path: "/login",
    Component: Login,
  },
  {
    element: <ProtectedRoute allowedRole={"admin"} />,
    children: [
      {
        path: "admin",
        Component: AdminNavbar,
        children: [
          {
            path: "dashboard",
            Component: AdminDashboard,
          },
          {
            path: "companies",
            Component: AdminCompanyList,
          },
        ],
      },
    ],
  },
]);

function App() {
  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}

export default App;
