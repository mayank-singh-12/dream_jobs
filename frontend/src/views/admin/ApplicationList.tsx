import { useEffect, useRef, useState, type SubmitEvent } from "react";
import { Input } from "@/components/ui/input";
import { type StudentProfile } from "./StudentList";

interface Company {
  id: number;
  name: string;
}

interface Job {
  id: number;
  title: string;
  location: string;
  mode: string;
  job_type: string;
  required_cgpa: number;
  company: Company;
}

type ApplicationStudentProfile = Omit<StudentProfile, "resume_path" | "status">;

interface Application {
  id: number;
  student_id: number;
  job_id: number;
  status: string;
  applied_at: string;
  student: ApplicationStudentProfile;
  job: Job;
}

function ApplicationList() {
  const queryInputRef = useRef(null);

  const [isApplicationsLoading, setIsApplicationsLoading] =
    useState<boolean>(false);
  const [applicationsError, setApplicationsError] = useState<string | null>();
  const [applications, setApplications] = useState<Array<Application>>([]);

  const [query, setQuery] = useState<string>("");
  const [search, setSearch] = useState<boolean>(false);

  useEffect(() => {
    async function fetchApplications() {
      setIsApplicationsLoading(true);
      setApplicationsError(null);
      try {
        const response = await fetch(
          `${import.meta.env.VITE_ADMIN_API}/applications?q=${query}`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${import.meta.env.VITE_ADMIN_JWT}`,
            },
          },
        );
        if (!response.ok) {
          const error = await response.json();
          throw error.message;
        }
        const data = await response.json();
        setApplications(data);
      } catch (e) {
        setApplicationsError(e);
      } finally {
        setIsApplicationsLoading(false);
      }
    }

    fetchApplications();
  }, [search]);

  function handleSearch(e: SubmitEvent<HTMLFormElement>) {
    e.preventDefault();
    setQuery(queryInputRef.current.value);
    setSearch((search) => !search);
  }

  const applicationRecords = applications?.map((application) => (
    <li
      className="bg-card min-w-[14rem] max-w-[15rem] my-2 p-5 rounded-sm"
      key={application.id}
    >
      <div className="text-card-foreground">
        <p>
          {application.student.first_name} {application.student.last_name}
        </p>
        <p className="text-gray-500">{application.job.title}</p>
        <p className="text-gray-500">{application.job.company.name}</p>
        <p className="text-gray-500">{application.job.location}</p>
        <p className="text-gray-500">{application.job.mode}</p>
        <p className="text-gray-500">{application.job.job_type}</p>
      </div>
    </li>
  ));

  return (
    <>
      <div className="flex justify-center">
        <h1 className="text-2xl font-medium text-white">Applications</h1>
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
          {isApplicationsLoading == true && <p>Loading...</p>}
          {isApplicationsLoading == false && (
            <ul className="grid 2xl:grid-cols-6 xl:grid-cols-5 lg:grid-cols-4 md:grid-cols-3  sm:grid-cols-2 gap-[1rem] bg-rose-900">
              {applicationRecords}
            </ul>
          )}
          {applicationsError == null && <p>{applicationsError}</p>}
        </div>
      </div>
    </>
  );
}

export default ApplicationList;
