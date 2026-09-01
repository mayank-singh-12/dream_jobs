import { useEffect, useRef, useState, type SubmitEvent } from "react";
import { Input } from "@/components/ui/input";
import { type CompanyProfile } from "./CompanyList";

interface Job {
  id: number;
  title: string;
  location: string;
  mode: string;
  job_type: string;
  job_status: string;
  required_cgpa: string;
  deadline: string;
  description: string;
  company: CompanyProfile;
}

function JobList() {
  const queryInputRef = useRef(null);

  const [isJobsLoading, setIsJobsLoading] = useState<boolean>(false);
  const [jobsError, setJobsError] = useState<string | null>();
  const [jobs, setJobs] = useState<Array<Job>>([]);

  const [query, setQuery] = useState<string>("");
  const [search, setSearch] = useState<boolean>(false);

  useEffect(() => {
    async function fetchApplications() {
      setIsJobsLoading(true);
      setJobsError(null);
      try {
        const response = await fetch(
          `${import.meta.env.VITE_ADMIN_API}/jobs?q=${query}`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${import.meta.env.VITE_ADMIN_JWT}`,
            },
          },
        );
        if (!response.ok) {
          const error = await response.json();
          throw error.msg;
        }
        const data = await response.json();
        setJobs(data);
      } catch (e) {
        setJobsError(e);
      } finally {
        setIsJobsLoading(false);
      }
    }

    fetchApplications();
  }, [search]);

  function handleSearch(e: SubmitEvent<HTMLFormElement>) {
    e.preventDefault();
    setQuery(queryInputRef.current.value);
    setSearch((search) => !search);
  }

  const jobRecords = jobs?.map((job) => (
    <li
      className="bg-card min-w-[14rem] max-w-[15rem] my-2 p-5 rounded-sm"
      key={job.id}
    >
      <div className="text-card-foreground">
        <p>{job.title}</p>
        <p className="text-gray-500">{job.company.name}</p>
        <p className="text-gray-500">{job.location}</p>
        <p className="text-gray-500">{job.mode}</p>
        <p className="text-gray-500">{job.job_type}</p>
      </div>
    </li>
  ));

  return (
    <>
      <div className="flex justify-center">
        <h1 className="text-2xl font-medium text-white">Jobs</h1>
      </div>
      <div className="">
        <form onSubmit={handleSearch}>
          <div className="flex justify-center">
            <Input
              type="text"
              placeholder="search applications by title"
              ref={queryInputRef}
            />
            <button
              className="bg-yellow-400 min-w-[4rem] md:min-w-[10rem] lg:min-w-[10rem] xl:min-w-[10rem] px-2"
              //   disabled={isStudentsLoading}
            >
              search
            </button>
          </div>
        </form>
        <div>
          {isJobsLoading == true && <p>Loading...</p>}
          {isJobsLoading == false && (
            <ul className="grid 2xl:grid-cols-6 xl:grid-cols-5 lg:grid-cols-4 md:grid-cols-3  sm:grid-cols-2 gap-[1rem] gap-[1rem] bg-rose-900">
              {jobRecords}
            </ul>
          )}
          {jobsError == null && <p>{jobsError}</p>}
        </div>
      </div>
    </>
  );
}

export default JobList;
