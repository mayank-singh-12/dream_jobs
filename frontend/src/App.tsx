import { RouterProvider } from "react-router/dom";
import { createBrowserRouter } from "react-router";
import AdminDashboard from "./views/admin/dashboard";

const router = createBrowserRouter([
  {
    path: "/",
    element: <AdminDashboard />,
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
