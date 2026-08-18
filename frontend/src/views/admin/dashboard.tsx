import { Link, useLoaderData } from "react-router";

function AdminDashboard() {
  const count = useLoaderData();
  return (
    <>
      <div>
        <h1 className="text-2xl">Admin Dashboard</h1>
        <p>Students:{count.students}</p>
        <p>Companies:{count.companies}</p>
        <p>Jobs:{count.jobs}</p>
        <div>
          <Link to={"/admin/students"} className="p-5 bg-rose-500">
            Students
          </Link>
        </div>
        <div>
          <Link to={"/admin/companies"} className="p-5 bg-rose-500">
            Companies
          </Link>
        </div>
        <div>
          <Link to={"/admin/jobs"} className="p-5 bg-rose-500">
            Jobs
          </Link>
        </div>
      </div>
    </>
  );
}

export default AdminDashboard;
