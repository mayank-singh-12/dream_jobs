import { Link } from "react-router";
import { useEffect, useState } from "react";
import { useAppSelector } from "@/lib/hooks";
import { selectUserData } from "@/lib/features/auth/authSlice";

interface Count {
  students: number;
  companies: number;
  jobs: number;
}

function AdminDashboard() {
  const [loadingCount, setLoadingCount] = useState<boolean>(false);
  const [countErrorMessage, setCountErrorMessage] = useState<string | null>("");
  const [count, setCount] = useState<Count>();
  const userData = useAppSelector(selectUserData);
  useEffect(() => {
    async function fetchCounts() {
      try {
        setLoadingCount(true);
        setCountErrorMessage(null);
        const response = await fetch(
          `${import.meta.env.VITE_ADMIN_API}/count`,
          {
            headers: {
              Authorization: `Bearer ${import.meta.env.VITE_ADMIN_JWT}`,
            },
          },
        );
        if (!response.ok) {
          const error = await response.json();
          throw error.msg;
        }
        const data = await response.json();
        console.log(data);
        setCount(data);
      } catch (e) {
        setCountErrorMessage(e);
      } finally {
        setLoadingCount(false);
      }
    }
    fetchCounts();
  }, []);

  console.log(userData);

  return (
    <>
      <div>
        <h1 className="text-2xl">Admin Dashboard</h1>
        {loadingCount && <p>Loading...</p>}
        {countErrorMessage && (
          <p className="text-red-500">{countErrorMessage}</p>
        )}
        {count && (
          <>
            <p>Students:{count.students}</p>
            <p>Companies:{count.companies}</p>
            <p>Jobs:{count.jobs}</p>
          </>
        )}
        <div className="flex justify-center gap-2">
          <Link to={"/admin/students"}>
            <div className="p-5 bg-rose-500">Students</div>
          </Link>
          <Link to={"/admin/companies"}>
            <div className="p-5 bg-rose-500">Companies</div>
          </Link>
          <Link to={"/admin/jobs"}>
            <div className="p-5 bg-rose-500">Jobs</div>
          </Link>
        </div>
      </div>
    </>
  );
}

export default AdminDashboard;
