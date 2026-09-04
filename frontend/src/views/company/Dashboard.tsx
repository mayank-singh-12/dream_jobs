import { useEffect, useState, type ReactElement } from "react";
import { useAppSelector } from "@/lib/hooks";
import { selectUserData } from "@/lib/features/auth/authSlice";
import { Link } from "react-router";
import { useAppDispatch } from "@/lib/hooks";
import { updateCompanyStatus } from "@/lib/features/auth/authSlice";

interface Company {
  company_profile: {
    about: string;
    id: number;
    location: string;
    name: string;
    status: "approved" | "pending" | "rejected";
    website: string;
  };
  email: string;
  id: number;
  role: "company";
  student_profile: null;
  username: string;
}

function CompanyDashboard() {
  const userData = useAppSelector(selectUserData);
  const dispatch = useAppDispatch();

  const [companyLoading, setCompanyLoading] = useState<boolean>(false);
  const [company, setCompany] = useState<Company>();
  const [companyError, setCompanyError] = useState<string | null>();

  useEffect(() => {
    async function fetchCompanyData() {
      try {
        setCompanyLoading(true);
        const response = await fetch(
          `${import.meta.env.VITE_COMPANY_API}/details`,
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
        setCompany(data);
        dispatch(updateCompanyStatus(data.company_profile.status));
      } catch (e) {
        setCompanyError(e);
      } finally {
        setCompanyLoading(false);
      }
    }
    fetchCompanyData();
  }, []);

  function renderDashboardTitle(company: Company): ReactElement {
    if (company && company.company_profile.status === "approved") {
      return (
        <div className="flex flex-col">
          <Link
            to="/company/jobs/new"
            className="p-2 bg-gray-950 self-start border-1 border-white rounded-sm"
          >
            Create Placement Drive
          </Link>
          <p className="p-2 border-1 self-start rounded-sm">
            Add new Job Component
          </p>

          <p className="p-2 border-1 self-start rounded-sm">
            Accepted Jobs Component
          </p>
          <p className="p-2 border-1 self-start rounded-sm">
            Pending Jobs Component
          </p>
        </div>
      );
    } else if (company && company.company_profile.status === "pending") {
      return (
        <div>
          <p className="text-yellow-500">
            Company is not yet approved by Admin. Please wait until its
            approved...
          </p>
        </div>
      );
    } else {
      return (
        <div>
          <p className=" text-red-500">Admin rejected your company!</p>
        </div>
      );
    }
  }

  return (
    <>
      {companyLoading && <p>Loading...</p>}
      {!companyLoading && companyError && <p>{companyError}</p>}
      {!companyLoading && company && (
        <>
          <div>
            <h1 className="text-[3rem] font-bold">
              {company.company_profile.name}
            </h1>
            <h1 className="text-[2rem] font-light ms-[8rem]">
              {company.company_profile.location}
            </h1>
            <Link
              className="text-blue-400"
              to={company?.company_profile?.website}
            >
              {company.company_profile.name}
            </Link>
            <p>{company.company_profile.about}</p>
          </div>
          {renderDashboardTitle(company)}
        </>
      )}
    </>
  );
}

export default CompanyDashboard;
