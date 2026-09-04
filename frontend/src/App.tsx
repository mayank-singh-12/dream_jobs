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
import AdminCompanyDetail from "./views/admin/CompanyDetail";
import AdminJobDetail from "./views/admin/JobDetail";

import CompanyNavbar from "./components/CompanyNavbar";
import CompanyDashboard from "./views/company/Dashboard";
import CompanyNewJob from "./views/company/NewJob";

import { ToastContainer, Bounce } from "react-toastify";

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
            path: "companies/:companyId",
            Component: AdminCompanyDetail,
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
            path: "jobs/:jobId",
            Component: AdminJobDetail,
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
    element: <ProtectedRoute allowedRole={"company"} />,
    children: [
      {
        path: "company",
        Component: CompanyNavbar,
        children: [
          {
            path: "dashboard",
            Component: CompanyDashboard,
          },
          {
            path: "jobs",
            Component: AdminDashboard,
          },
          {
            path: "jobs/new",
            Component: CompanyNewJob,
          },
          {
            path: "applications",
            Component: AdminDashboard,
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
            index: true,
            loader: () => redirect("/student/dashboard"),
          },
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
      <ToastContainer
        position="top-right"
        autoClose={2000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick={false}
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="dark"
        transition={Bounce}
      />
      <RouterProvider router={router} />
    </>
  );
}

export default App;
