import { useAppSelector } from "@/lib/hooks";
import { selectUserData } from "@/lib/features/auth/authSlice";
import { useNavigate } from "react-router";
import { useEffect } from "react";
import { Link } from "react-router";

function LandingPage() {
  const userData = useAppSelector(selectUserData);
  const navigate = useNavigate();

  useEffect(() => {
    if (userData.user.id !== null) {
      navigate(`/${userData.user.role}/dashboard`);
    }
  }, []);

  return (
    <>
      <h1>Dream Jobs</h1>
      <Link to={"/login"} className="text-blue-400 underline">
        Login
      </Link>
      <br />
      <Link to={"/register"} className="text-blue-400 underline">
        Register
      </Link>
    </>
  );
}

export default LandingPage;
