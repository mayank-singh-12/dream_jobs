import { FieldLegend } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useState, useRef, type SubmitEvent } from "react";
import { Link } from "react-router";
import { Label } from "@/components/ui/label";
import { FieldLabel } from "@/components/ui/field";
import { useNavigate } from "react-router";
import { Textarea } from "@/components/ui/textarea";

function RegisterStudent() {
  const [confirmPasswordError, setConfirmPasswordError] = useState<string>();
  const [formError, setFormError] = useState<string>();
  const [formSuccess, setFormSuccess] = useState<string>();

  const navigate = useNavigate();

  async function register(formData: FormData) {
    setFormSuccess(undefined);
    setFormError(undefined);

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

  async function handleSubmit(e: SubmitEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.target);
    if (formData.get("password") !== formData.get("confirm_password")) {
      return setConfirmPasswordError("Passwords doesn't match");
    }
    if (confirmPasswordError !== undefined) {
      setConfirmPasswordError(undefined);
    }
    try {
      const data = await register(formData);
      setFormSuccess(data.message);
      navigate("/login");
    } catch (e) {
      console.log("Error->", e);
      setFormError(e);
    }
  }
  return (
    <>
      <div className="max-w-[40rem] mb-[30px]">
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
    </>
  );
}

interface RegisterCompanyData {
  username: string;
  website: string;
  location: string;
  email: string;
  password: string;
  name: string;
  about: string;
}

function RegisterCompany() {
  const [confirmPasswordError, setConfirmPasswordError] = useState<string>();
  const [formError, setFormError] = useState<string>();
  const [formSuccess, setFormSuccess] = useState<string>();
  const [loadingRegister, setLoadingRegister] = useState<boolean>(false);

  const companyNameInput = useRef(null);
  const companyWebsiteInput = useRef(null);
  const usernameInput = useRef(null);
  const locationInput = useRef(null);
  const emailInput = useRef(null);
  const passwordInput = useRef(null);
  const confirmPasswordInput = useRef(null);
  const aboutInput = useRef(null);

  const navigate = useNavigate();

  async function register(formData: RegisterCompanyData) {
    const response = await fetch(
      `${import.meta.env.VITE_API}/register/company`,
      {
        method: "POST",
        body: JSON.stringify(formData),
        headers: {
          "Content-Type": "application/json",
        },
      },
    );
    if (!response.ok) {
      const error = await response.json();
      throw error.error;
    }
    const data = await response.json();
    return data;
  }

  async function handleSubmit(e: SubmitEvent<HTMLFormElement>) {
    e.preventDefault();
    setFormSuccess(undefined);
    setFormError(undefined);
    setLoadingRegister(true);

    if (passwordInput.current.value !== confirmPasswordInput.current.value) {
      setLoadingRegister(false);
      return setConfirmPasswordError("Passwords doesn't match");
    }
    const formData: RegisterCompanyData = {
      username: usernameInput.current.value,
      website: companyWebsiteInput.current.value,
      location: locationInput.current.value,
      email: emailInput.current.value,
      password: passwordInput.current.value,
      name: companyNameInput.current.value,
      about: aboutInput.current.value,
    };

    if (confirmPasswordError !== undefined) {
      setConfirmPasswordError(undefined);
    }
    try {
      const data = await register(formData);
      setFormSuccess(data.message);
      navigate("/login");
    } catch (e) {
      console.log("Error->", e);
      setFormError(e);
    } finally {
      setLoadingRegister(false);
    }
  }
  return (
    <>
      <div className="max-w-[40rem]">
        <form onSubmit={handleSubmit}>
          <div className="mb-2">
            <Label htmlFor="input-first-name">Company Name</Label>
            <Input
              id="input-first-name"
              type="text"
              name="company_name"
              placeholder="company name"
              ref={companyNameInput}
              required
            />
          </div>

          <div className="mb-2">
            <Label htmlFor="input-company-website">Website</Label>
            <Input
              id="input-company-website"
              type="url"
              name="website"
              placeholder="website"
              ref={companyWebsiteInput}
              required
            />
          </div>

          <div className="mb-2">
            <FieldLabel htmlFor="input-location">Location</FieldLabel>
            <Input
              id="input-location"
              type="text"
              name="location"
              placeholder="location"
              ref={locationInput}
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
              ref={usernameInput}
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
              ref={emailInput}
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
              ref={passwordInput}
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
              ref={confirmPasswordInput}
              required
            />
          </div>
          <div className="mb-2">
            <FieldLabel htmlFor="input-about">About</FieldLabel>
            <Textarea id="input-about" name="about" ref={aboutInput} required />
          </div>

          {formError && <p className="text-red-500">{formError}</p>}
          {confirmPasswordError && (
            <p className="text-red-500 text-[12px]">{confirmPasswordError}</p>
          )}
          {formError && <p className="text-red-500 text-[12px]">{formError}</p>}
          {formSuccess && (
            <p className="text-green-500 text-[12px]">{formSuccess}</p>
          )}

          <Button type="submit" disabled={loadingRegister}>
            Register
          </Button>
        </form>
      </div>
    </>
  );
}

function Register() {
  const [selectedRole, setSelectedRole] = useState<string>("student");
  return (
    <>
      <FieldLegend className="text-2xl">Register</FieldLegend>

      <div className="mb-3 flex gap-5">
        <label htmlFor="select-user">
          <input
            type="radio"
            name="select_user_role"
            id="select-user"
            value="student"
            onChange={(e) => setSelectedRole(e.target.value)}
            checked={selectedRole === "student"}
          />
          Student
        </label>

        <label htmlFor="select-company">
          <input
            type="radio"
            name="select_user_role"
            id="select-company"
            value="company"
            onChange={(e) => setSelectedRole(e.target.value)}
            checked={selectedRole === "company"}
          />
          Company
        </label>
      </div>

      {selectedRole === "student" && <RegisterStudent />}

      {selectedRole === "company" && <RegisterCompany />}

      <Link to="/login" className="text-gray-400 underline">
        Login
      </Link>
    </>
  );
}

export default Register;
