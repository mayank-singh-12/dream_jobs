import { useEffect } from "react";
import { useAppDispatch, useAppSelector } from "../../lib/hooks";
import {
  selectCount,
  selectCountStatus,
  selectCountError,
  fetchAdminCounts,
} from "../../lib/features/counter/counterSlice";

function AdminDashboard() {
  const count = useAppSelector(selectCount);
  const countStatus = useAppSelector(selectCountStatus);
  const countError = useAppSelector(selectCountError);
  const dispatch = useAppDispatch();

  useEffect(() => {
    if (countStatus === "idle") {
      dispatch(fetchAdminCounts());
    }
  }, []);

  console.log(countStatus);

  if (countStatus === "pending")
    return (
      <>
        <p>Loading...</p>
      </>
    );

  if (countError !== null) {
    return (
      <>
        <p>{countError}</p>
      </>
    );
  }

  return (
    <>
      <div>
        <h1 className="text-2xl">Admin Dashboard</h1>
        <p>Students:{count.students}</p>
        <p>Companies:{count.companies}</p>
        <p>Jobs:{count.jobs}</p>
      </div>
    </>
  );
}

export default AdminDashboard;
