import { useAppSelector } from "@/lib/hooks";
import { selectUserData } from "@/lib/features/auth/authSlice";
import { Navigate, Outlet } from "react-router";

function ProtectedRoute({ allowedRole }) {
  const userData = useAppSelector(selectUserData);

  if (userData.user.id === null) {
    return <Navigate to="/login" replace />;
  }

  if (userData.user.role !== allowedRole) {
    return (
      <Navigate
        to={`${import.meta.env.VITE_API}/${userData.user.role}/dashboard`}
        replace
      />
    );
  }
  return <Outlet />;
}

export default ProtectedRoute;
