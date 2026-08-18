import { RouterProvider } from "react-router/dom";
import { createBrowserRouter } from "react-router";

import Login from "./views/auth/Login";

import AdminDashboard from "./views/admin/Dashboard";
import AdminNavbar from "./components/AdminNavbar";
import AdminCompanyList from "./views/admin/CompanyList";

const router = createBrowserRouter([
  {
    path: "/login",
    Component: Login,
  },
  {
    path: "/admin",
    Component: AdminNavbar,
    children: [
      {
        index: true,
        loader: async () => {
          const res = await fetch(`${import.meta.env.VITE_ADMIN_API}/count`, {
            method: "GET",
            headers: {
              Authorization: `Bearer ${import.meta.env.VITE_ADMIN_JWT}`,
            },
          });
          console.log("Logger running");
          const data = await res.json();
          return data;
        },
        Component: AdminDashboard,
      },
      {
        path: "companies",

        Component: AdminCompanyList,
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
