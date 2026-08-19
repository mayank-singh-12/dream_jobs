import { useEffect, useRef } from "react";
import { Field, FieldLegend } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  login,
  selectUserData,
  selectLoginErrorMessage,
  selectLoginStatus,
} from "@/lib/features/auth/authSlice";
import { useAppDispatch, useAppSelector } from "@/lib/hooks";
import { Link, useNavigate } from "react-router";

function Login() {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const userData = useAppSelector(selectUserData);
  const loginStatus = useAppSelector(selectLoginStatus);
  const loginErrorMessage = useAppSelector(selectLoginErrorMessage);

  const emailInput = useRef(null);
  const passwordInput = useRef(null);

  useEffect(() => {
    if (userData.user.id !== null) {
      navigate(`/${userData.user.role}/dashboard`);
    }
  }, [userData]);

  function handleLogin() {
    const email = emailInput.current.value;
    const password = passwordInput.current.value;

    if (loginStatus !== "pending") {
      dispatch(login({ email, password }));
    }
  }
  return (
    <>
      <Field className="max-w-[40rem]">
        <FieldLegend className={"text-lg"}>Login</FieldLegend>
        <Input
          id="input-username"
          type="text"
          placeholder="username..."
          ref={emailInput}
        />
        <Input
          id="input-password"
          type="text"
          placeholder="password..."
          ref={passwordInput}
        />
        {loginErrorMessage && (
          <p className="text-red-500 text-sm">{loginErrorMessage}</p>
        )}
        <Button
          disabled={loginStatus === "pending"}
          onClick={() => handleLogin()}
        >
          login
        </Button>
        <Link to="/register" className="text-gray-400 underline">
          Register
        </Link>
      </Field>
      <div>
        <p>user data</p>
        <p>id: {userData.user.id}</p>
        <p>username: {userData.user.email}</p>
        <p>role: {userData.user.role}</p>
      </div>
    </>
  );
}

export default Login;
