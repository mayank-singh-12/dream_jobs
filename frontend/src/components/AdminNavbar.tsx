import { useState } from "react";
import { Outlet } from "react-router";

function AdminNavbar() {
  return (
    <>
      <header className="bg-blue-400">
        <div className="p-4">
          <p className="font-bold text-2xl">Placement Portal [Admin]</p>
        </div>
      </header>
      <main className="bg-blue-200 ">
        <div className="p-2">
          <Outlet />
        </div>
      </main>
    </>
  );
}

export default AdminNavbar;
