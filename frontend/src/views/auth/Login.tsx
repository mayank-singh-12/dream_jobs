// import { Field, FieldDescription, FieldLabel } from "@";
import { useRef, useState } from "react";
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
import { redirect } from "react-router";

function Login() {
  const dispatch = useAppDispatch();

  const userData = useAppSelector(selectUserData);
  const loginStatus = useAppSelector(selectLoginStatus);
  const loginErrorMessage = useAppSelector(selectLoginErrorMessage);

  const emailInput = useRef(null);
  const passwordInput = useRef(null);

  async function handleLogin() {
    const email = emailInput.current.value;
    const password = passwordInput.current.value;

    if (loginStatus !== "pending") {
      await dispatch(login({ email, password }));
    }
    return redirect("/admin/companies");
  }
  console.log(userData);
  console.log(loginStatus);
  return (
    <>
      <Field>
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
          disabled={loginStatus === "pending" || loginStatus === "success"}
          onClick={() => handleLogin()}
        >
          login
        </Button>
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
