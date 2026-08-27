import { RouterProvider } from "react-router/dom";
import { createBrowserRouter, redirect } from "react-router";

import Login from "./views/auth/Login";
import Register from "./views/auth/Register";
import LandingPage from "./views/LandingPage";
import ProtectedRoute from "./components/ProtectedRoute";
import AdminDashboard from "./views/admin/Dashboard";
import AdminNavbar from "./components/AdminNavbar";
import AdminCompanyList from "./views/admin/CompanyList";
import AdminStudentList from "./views/admin/StudentList";
import AdminJobList from "./views/admin/JobList";
import AdminApplicationList from "./views/admin/ApplicationList";

const router = createBrowserRouter([
  { path: "/", Component: LandingPage },
  {
    path: "/login",
    Component: Login,
  },
  {
    path: "/register",
    Component: Register,
  },
  {
    element: <ProtectedRoute allowedRole={"admin"} />,
    children: [
      {
        path: "admin",
        Component: AdminNavbar,
        children: [
          {
            index: true,
            loader: () => redirect("/admin/dashboard"),
          },
          {
            path: "dashboard",
            Component: AdminDashboard,
          },
          {
            path: "companies",
            Component: AdminCompanyList,
          },
          {
            path: "students",
            Component: AdminStudentList,
          },
          {
            path: "jobs",
            Component: AdminJobList,
          },
          {
            path: "applications",
            Component: AdminApplicationList,
          },
        ],
      },
    ],
  },
  {
    element: <ProtectedRoute allowedRole={"student"} />,
    children: [
      {
        path: "student",
        Component: AdminNavbar,
        children: [
          {
            path: "dashboard",
            Component: AdminDashboard,
          },
        ],
      },
    ],
  },
  {
    element: <ProtectedRoute allowedRole={"company"} />,
    children: [
      {
        path: "company",
        Component: AdminNavbar,
        children: [
          {
            path: "dashboard",
            Component: AdminDashboard,
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
