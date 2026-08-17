import { RouterProvider } from "react-router/dom";
import { createBrowserRouter } from "react-router";
import AdminDashboard from "./views/admin/Dashboard";
import AdminNavbar from "./components/AdminNavbar";
import AdminCompanyList from "./views/admin/CompanyList";

const router = createBrowserRouter([
  {
    path: "/admin",
    Component: AdminNavbar,
    children: [
      { index: true, Component: AdminDashboard },
      { path: "companies", Component: AdminCompanyList },
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
