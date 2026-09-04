import { useState, type SubmitEvent } from "react";
import { useNavigate } from "react-router";
import { useAppSelector } from "@/lib/hooks";
import { selectUserData } from "@/lib/features/auth/authSlice";
import { toast } from "react-toastify";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
  FieldLegend,
  FieldSet,
} from "@/components/ui/field";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
  SelectLabel,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";

function NewJob() {
  const navigate = useNavigate();
  const userData = useAppSelector(selectUserData);

  const [title, setTitle] = useState("");
  const [location, setLocation] = useState("");
  const [mode, setMode] = useState("on-site");
  const [jobType, setJobType] = useState("full-time");
  const [description, setDescription] = useState("");
  const [requiredCgpa, setRequiredCgpa] = useState("");
  const [deadline, setDeadline] = useState("");

  const jobModes = [
    { label: "Select Job Mode", value: null },
    { label: "On-site", value: "on-site" },
    { label: "Remote", value: "remote" },
    { label: "Hybrid", value: "hybrid" },
  ];

  const jobTypes = [
    { label: "Select Job Type", value: null },
    { label: "Full-time", value: "full-time" },
    { label: "Part-time", value: "part-time" },
    { label: "Contract", value: "contract" },
  ];

  async function handleSubmit(e: SubmitEvent<HTMLFormElement>) {
    e.preventDefault();

    const jobData = {
      title,
      location,
      mode,
      job_type: jobType,
      description,
      required_cgpa: requiredCgpa ? Number(requiredCgpa) : null,
      deadline: deadline || null,
    };

    try {
      const response = await fetch(`${import.meta.env.VITE_COMPANY_API}/jobs`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${userData.token}`,
        },
        body: JSON.stringify(jobData),
      });

      if (!response.ok) {
        const error = await response.json();
        throw error.message;
      }

      const { message } = await response.json();
      toast.success(message);
      navigate("/company/dashboard");
    } catch (e) {
      toast.error(e);
    }
  }

  return (
    <>
      <form onSubmit={handleSubmit}>
        <FieldSet>
          <FieldLegend>Job Details</FieldLegend>
          <FieldDescription>
            Fill all the details of a new job.
          </FieldDescription>

          <FieldGroup>
            <Field>
              <FieldLabel htmlFor="input-job-title">Job Title</FieldLabel>
              <Input
                id="input-job-title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
              />
            </Field>

            <Field>
              <FieldLabel htmlFor="input-location">Location</FieldLabel>
              <Input
                id="input-location"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                required
              />
            </Field>

            <Field>
              <FieldLabel htmlFor="input-job-mode">Mode</FieldLabel>
              <Select
                required
                items={jobModes}
                value={mode}
                onValueChange={(val) => setMode(val)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectGroup>
                    <SelectLabel>Job Mode</SelectLabel>
                    {jobModes.map((mode) => (
                      <SelectItem key={mode.value} value={mode.value}>
                        {mode.label}
                      </SelectItem>
                    ))}
                  </SelectGroup>
                </SelectContent>
              </Select>
            </Field>

            <Field>
              <FieldLabel htmlFor="input-job-type">Type</FieldLabel>
              <Select
                required
                items={jobTypes}
                value={jobType}
                onValueChange={(val) => setJobType(val)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectGroup>
                    <SelectLabel>Job Type</SelectLabel>
                    {jobTypes.map((type) => (
                      <SelectItem key={type.value} value={type.value}>
                        {type.label}
                      </SelectItem>
                    ))}
                  </SelectGroup>
                </SelectContent>
              </Select>
            </Field>

            <Field>
              <FieldLabel htmlFor="input-description">Description</FieldLabel>
              <Textarea
                id="input-description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                required
              />
            </Field>

            <Field>
              <FieldLabel htmlFor="input-required-cgpa">
                Required CGPA
              </FieldLabel>
              <Input
                type="number"
                min={0}
                max={10}
                step={0.1}
                id="input-required-cgpa"
                value={requiredCgpa}
                onChange={(e) => setRequiredCgpa(e.target.value)}
                required
              />
            </Field>

            <Field>
              <FieldLabel htmlFor="input-deadline">Deadline</FieldLabel>
              <Input
                type="date"
                id="input-deadline"
                value={deadline}
                onChange={(e) => setDeadline(e.target.value)}
                required
              />
            </Field>

            <Button type="submit">Submit</Button>
          </FieldGroup>
        </FieldSet>
      </form>
    </>
  );
}

export default NewJob;
