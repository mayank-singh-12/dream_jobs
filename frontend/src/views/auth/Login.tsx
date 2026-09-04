import { useEffect, useRef, type SubmitEvent } from "react";
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
import { Label } from "@/components/ui/label";
interface LoginData {
  username: string | null;
  email: string | null;
  password: string | null;
}

function Login() {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const userData = useAppSelector(selectUserData);
  const loginStatus = useAppSelector(selectLoginStatus);
  const loginErrorMessage = useAppSelector(selectLoginErrorMessage);

  const emailOrUsernameInputRef = useRef(null);
  const passwordInputRef = useRef(null);

  useEffect(() => {
    if (userData.user.id !== null) {
      navigate(`/${userData.user.role}/dashboard`);
    }
  }, [userData]);

  function buildLoginPayload(
    emailOrUsername: string,
    password: string,
  ): LoginData {
    const atIndex = emailOrUsername.indexOf("@");
    const dotComIndex = emailOrUsername.indexOf(".com");

    let loginData: LoginData = {
      username: null,
      email: null,
      password: null,
    };

    if (atIndex > -1 && dotComIndex > -1 && atIndex < dotComIndex) {
      loginData = { username: null, email: emailOrUsername, password };
    } else {
      loginData = { username: emailOrUsername, email: null, password };
    }

    return loginData;
  }

  function handleLogin(e: SubmitEvent<HTMLFormElement>) {
    e.preventDefault();
    const emailOrUsername = emailOrUsernameInputRef.current.value;
    const password = passwordInputRef.current.value;

    console.log(emailOrUsername);

    const loginData: LoginData = buildLoginPayload(emailOrUsername, password);
    console.log(loginData);
    if (loginStatus !== "pending") {
      dispatch(login(loginData));
    }
  }
  return (
    <>
      <Field className="max-w-[40rem]">
        <FieldLegend className={"text-lg"}>Login</FieldLegend>
        <form onSubmit={handleLogin}>
          <div className="mb-2">
            <Label htmlFor="input-username">Username/Email</Label>
            <Input
              id="input-username"
              type="text"
              placeholder="username"
              autoComplete="username"
              ref={emailOrUsernameInputRef}
              required
            />
          </div>
          <div className="mb-2">
            <Label htmlFor="input-password">Password</Label>
            <Input
              id="input-password"
              type="password"
              placeholder="password"
              ref={passwordInputRef}
              autoComplete="current-password"
              required
            />
          </div>
          {loginErrorMessage && (
            <p className="text-red-500 text-sm">{loginErrorMessage}</p>
          )}
          <Button type="submit" disabled={loginStatus === "pending"}>
            login
          </Button>
        </form>
      </Field>
      <Link to="/register" className="text-gray-400 underline">
        Register
      </Link>
    </>
  );
}

export default Login;
