import { RouterProvider } from "react-router/dom";
import { createBrowserRouter } from "react-router";
import AdminDashboard from "./views/admin/Dashboard";
import AdminNavbar from "./components/AdminNavbar";

const router = createBrowserRouter([
  {
    path: "/",
    Component: AdminNavbar,
    children: [{ index: true, Component: AdminDashboard }],
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
