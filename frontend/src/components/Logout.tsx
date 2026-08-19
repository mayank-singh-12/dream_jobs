import { useAppDispatch } from "@/lib/hooks";
import { logout } from "@/lib/features/auth/authSlice";
import { Navigate } from "react-router";

function Logout() {
  const dispatch = useAppDispatch();
  return (
    <button
      className="p-1 px-2 bg-red-500 hover:cursor-pointer hover:bg-red-600 text-white"
      onClick={() => {
        dispatch(logout());
        return <Navigate to="/" replace />;
      }}
    >
      Logout
    </button>
  );
}

export default Logout;
