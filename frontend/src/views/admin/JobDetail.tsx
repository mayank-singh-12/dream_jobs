import { useEffect, useState, type Dispatch, type SetStateAction } from "react";
import { useParams } from "react-router";
import type { Job } from "./JobList";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { toast } from "react-toastify";
import { useAppSelector } from "@/lib/hooks";
import { selectUserData } from "@/lib/features/auth/authSlice";

type ChangeJobStatusProps = {
  job: Job;
  open: boolean;
  setOpen: Dispatch<SetStateAction<boolean>>;
};

function ChangeJobStatus({ job, open, setOpen }: ChangeJobStatusProps) {
  console.log(open);
  const userData = useAppSelector(selectUserData);

  const [jobStatus, setJobStatus] = useState<Job["job_status"]>(job.job_status);

  const [updateStatusLoading, setUpdateStatusLoading] =
    useState<boolean>(false);

  const status = [
    { label: "Select status", value: null },
    { label: "Approved", value: "approved" },
    { label: "Pending", value: "pending" },
    { label: "Rejected", value: "rejected" },
  ];

  async function updateJobStatus(jobId: number, jobStatus: Job["job_status"]) {
    try {
      setUpdateStatusLoading(true);
      const response = await fetch(
        `${import.meta.env.VITE_ADMIN_API}/job/${jobId}/${jobStatus}`,
        {
          method: "POST",
          headers: { Authorization: `Bearer ${userData.token}` },
        },
      );
      if (!response.ok) {
        const error = await response.json();
        throw error.message;
      }
      const { message } = await response.json();
      toast.success(message);
      setOpen(false);
    } catch (e) {
      toast.error(e);
    } finally {
      setUpdateStatusLoading(false);
    }
  }

  useEffect(() => {
    if (!open) {
      setJobStatus(job.job_status);
    }
  }, [open]);

  return (
    <>
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="sm:max-w-sm">
          <DialogHeader>
            <DialogTitle>Edit Status</DialogTitle>
            <DialogDescription>
              Change the status of application.
            </DialogDescription>
          </DialogHeader>

          <Select
            items={status}
            onValueChange={(s) => setJobStatus(s)}
            value={jobStatus}
          >
            <SelectTrigger className="w-full mb-[1rem]">
              <SelectValue />
            </SelectTrigger>

            <SelectContent>
              <SelectGroup>
                <SelectLabel>Status</SelectLabel>
                {status.map((s) => (
                  <SelectItem key={status.indexOf(s)} value={s.value}>
                    {s.label}
                  </SelectItem>
                ))}
              </SelectGroup>
            </SelectContent>
          </Select>

          <DialogFooter>
            <DialogClose render={<Button variant="outline">Cancel</Button>} />
            <Button
              type="submit"
              disabled={
                jobStatus === job.job_status ||
                !jobStatus ||
                updateStatusLoading
              }
              onClick={() => updateJobStatus(job.id, jobStatus)}
            >
              Update status
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}

function JobDetail() {
  const { jobId } = useParams();
  const userData = useAppSelector(selectUserData);

  const [jobLoading, setJobLoading] = useState<boolean>(false);
  const [jobError, setJobError] = useState<string | null>(null);
  const [job, setJob] = useState<Job>();

  const [open, setOpen] = useState<boolean>(false);

  async function getJobDetails(jobId: number) {
    try {
      setJobLoading(true);
      const response = await fetch(
        `${import.meta.env.VITE_ADMIN_API}/jobs/${jobId}`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${userData.token}`,
          },
        },
      );
      if (!response.ok) {
        const error = await response.json();
        throw error.message;
      }
      const { data } = await response.json();
      setJob(data);
    } catch (e) {
      setJobError(e);
    } finally {
      setJobLoading(false);
    }
  }

  useEffect(() => {
    if (!open) {
      getJobDetails(parseInt(jobId));
    }
  }, [open]);

  return (
    <>
      <h1>Job Detail</h1>
      {jobLoading && <p>Loading...</p>}
      {jobError && <p>{jobError}</p>}
      {!jobLoading && job && (
        <>
          <ChangeJobStatus open={open} setOpen={setOpen} job={job} />
          <h1 className="text-2xl font-bold">{job.title}</h1>
          <h3 className="text-xl font-medium">{job.company.name}</h3>
          <p>{job.job_status}</p>
          <br />
          <Button
            variant="outline"
            disabled={job.job_status === "closed"}
            onClick={() => setOpen(true)}
          >
            Edit Status
          </Button>
        </>
      )}
    </>
  );
}

export default JobDetail;
