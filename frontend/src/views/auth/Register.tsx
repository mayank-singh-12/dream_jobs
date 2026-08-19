import { Field, FieldLegend } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useRef } from "react";

function Register() {
  const emailInput = useRef(null);
  const passwordInput = useRef(null);
  return (
    <>
      <h1>Register</h1>
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
      </Field>
    </>
  );
}

export default Register;
