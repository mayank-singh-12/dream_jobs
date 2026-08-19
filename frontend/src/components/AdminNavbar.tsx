import { Outlet } from "react-router";
import Logout from "./Logout";

function AdminNavbar() {
  return (
    <>
      <header className="bg-blue-800">
        <div className="p-4">
          <p className="font-bold text-2xl">Placement Portal [Admin]</p>
        </div>
        <div>
          <Logout />
        </div>
      </header>
      <main className="bg-gray-800">
        <div className="p-2">
          <Outlet />
        </div>
      </main>
    </>
  );
}

export default AdminNavbar;
