import { useAppSelector } from "@/lib/hooks";
import { selectUserData } from "@/lib/features/auth/authSlice";
import { useNavigate } from "react-router";
import { useEffect } from "react";

function LandingPage() {
  const userData = useAppSelector(selectUserData);
  const navigate = useNavigate();

  useEffect(() => {
    if (userData.user.id !== null) {
      navigate(`/${userData.user.role}/dashboard`);
    }
  }, []);

  return <h1>Dream Jobs</h1>;
}

export default LandingPage;
