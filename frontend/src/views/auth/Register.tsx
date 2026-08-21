import { Field, FieldLegend } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useRef, useState } from "react";
import { Link } from "react-router";
import { Label } from "@/components/ui/label";
import { FieldLabel } from "@/components/ui/field";
import { useNavigate } from "react-router";

function Register() {
  const [confirmPasswordError, setConfirmPasswordError] = useState<string>();
  const [formError, setFormError] = useState<string>();
  const [formSuccess, setFormSuccess] = useState<string>();

  const navigate = useNavigate();

  async function registerStudent(formData) {
    setFormSuccess(undefined);
    setFormError(undefined);

    console.log("Inside Form -> ", formData);

    const response = await fetch(
      `${import.meta.env.VITE_API}/register/student`,
      {
        method: "POST",
        body: formData,
      },
    );
    if (!response.ok) {
      const error = await response.json();
      throw error.error;
    }
    const data = await response.json();
    return data;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    if (formData.get("password") !== formData.get("confirm_password")) {
      return setConfirmPasswordError("Passwords doesn't match");
    }
    if (confirmPasswordError !== undefined) {
      setConfirmPasswordError(undefined);
    }
    try {
      const data = await registerStudent(formData);
      setFormSuccess(data);
      navigate("/login");
    } catch (e) {
      console.log("Error->", e);
      setFormError(e);
    }
  }
  console.log(confirmPasswordError);
  console.log("FORM ERROR ->", formError);
  console.log("FORM SUCCESS ->", formSuccess);

  return (
    <>
      <FieldLegend className="text-2xl">Register</FieldLegend>
      <div className="max-w-[40rem]">
        <form onSubmit={handleSubmit}>
          <div className="mb-2">
            <Label htmlFor="input-first-name">FirstName</Label>
            <Input
              id="input-first-name"
              type="text"
              name="first_name"
              placeholder="first name"
              required
            />
          </div>

          <div className="mb-2">
            <FieldLabel htmlFor="input-last-name">Last Name</FieldLabel>
            <Input
              id="input-last-name"
              type="text"
              name="last_name"
              placeholder="last name"
              required
            />
          </div>

          <div className="mb-2">
            <FieldLabel htmlFor="input-username">Username</FieldLabel>
            <Input
              id="input-username"
              type="text"
              name="username"
              placeholder="username"
              required
            />
          </div>

          <div className="mb-2">
            <FieldLabel htmlFor="input-email">Email</FieldLabel>
            <Input
              id="input-email"
              type="email"
              name="email"
              placeholder="email"
              required
            />
          </div>

          <div className="mb-2">
            <FieldLabel htmlFor="input-school">School</FieldLabel>
            <Input
              id="input-school"
              type="text"
              name="school"
              placeholder="school"
              required
            />
          </div>

          <div className="mb-2">
            <FieldLabel htmlFor="input-cgpa">CGPA</FieldLabel>
            <Input
              id="input-cgpa"
              type="number"
              name="cgpa"
              placeholder="cgpa"
              step={0.1}
              min={0}
              max={10}
              required
            />
          </div>

          <div className="mb-2">
            <FieldLabel htmlFor="input-password">Password</FieldLabel>
            <Input
              id="input-password"
              type="text"
              name="password"
              placeholder="password"
              required
            />
          </div>

          <div className="mb-2">
            <FieldLabel htmlFor="input-confirm-password">
              Confirm Password
            </FieldLabel>
            <Input
              id="input-confirm-password"
              type="text"
              name="confirm_password"
              placeholder="confirm-password"
              required
            />
          </div>

          <div className="mb-2">
            <FieldLabel htmlFor="input-confirm-password">
              Phone number
            </FieldLabel>
            <Input
              id="input-confirm-password"
              type="number"
              name="phone_number"
              placeholder="phone-number"
              min={1111111111}
              max={9999999999}
              required
            />
          </div>

          <div className="mb-2">
            <FieldLabel htmlFor="input-cv">CV</FieldLabel>
            <Input id="input-cv" type="file" name="cv" accept=".pdf" required />
          </div>
          {confirmPasswordError && (
            <p className="text-red-500 text-[12px]">{confirmPasswordError}</p>
          )}
          {formError && <p className="text-red-500 text-[12px]">{formError}</p>}
          {formSuccess && (
            <p className="text-green-500 text-[12px]">{formSuccess}</p>
          )}
          <Button type="submit">Register</Button>
        </form>
      </div>
      <Link to="/login" className="text-gray-400 underline">
        Login
      </Link>
    </>
  );
}

export default Register;
