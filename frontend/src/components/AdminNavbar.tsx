import { Outlet } from "react-router";
import Logout from "./Logout";
import { NavLink } from "react-router";

function AdminNavbar() {
  return (
    <>
      <header className="bg-blue-800">
        <div className="p-4 flex items-center gap-[1rem]">
          <p className="font-bold pe-4 text-2xl">Placement Portal [Admin]</p>
          <NavLink to="/admin/dashboard">
            <p className="text-blue-300 hover:text-white">Home</p>
          </NavLink>
          <NavLink to="/admin/companies">
            <p className="text-blue-300 hover:text-white">Companies</p>
          </NavLink>
          <NavLink to="/admin/students">
            <p className="text-blue-300 hover:text-white">Students</p>
          </NavLink>
          <NavLink to="/admin/jobs">
            <p className="text-blue-300 hover:text-white">Jobs</p>
          </NavLink>
          <NavLink to="/admin/applications">
            <p className="text-blue-300 hover:text-white">Applications</p>
          </NavLink>
          <div className="ms-auto">
            <Logout />
          </div>
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
