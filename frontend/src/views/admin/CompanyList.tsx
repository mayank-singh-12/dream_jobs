import { useState, useEffect, useRef } from "react";
import { Link } from "react-router";

export interface CompanyProfile {
  id: number;
  name: string;
  status: string;
  location: string;
  website: string;
  about: string;
}

interface Company {
  id: number;
  role: "company";
  username: string;
  email: string;
  company_profile: CompanyProfile;
}

function CompanyList() {
  const [isCompaniesLoading, setCompaniesLoading] = useState<boolean>(false);
  const [companiesError, setCompaniesError] = useState<string | null>(null);
  const [companies, setCompanies] = useState<Array<Company>>([]);

  const [query, setQuery] = useState<string>("");
  const [search, setSearch] = useState<boolean>(true);
  const queryInputRef = useRef(null);

  useEffect(() => {
    async function fetchCompanies() {
      setCompaniesLoading(true);
      setCompaniesError(null);
      try {
        const res = await fetch(
          `${import.meta.env.VITE_ADMIN_API}/company?q=${query}`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${import.meta.env.VITE_ADMIN_JWT}`,
            },
          },
        );
        if (!res.ok) {
          throw new Error("Error while fetching companies!");
        }
        const { data } = await res.json();
        setCompanies(data);
      } catch (e) {
        setCompaniesError(e.message);
        console.error(e);
      } finally {
        setCompaniesLoading(false);
      }
    }
    fetchCompanies();
    return () => {
      console.log("Clean up time!");
    };
  }, [search]);

  function handleSearch() {
    setQuery(queryInputRef.current.value);
    setSearch((search) => !search);
  }

  const companyRecords = companies.map((company) => (
    <Link to="/" key={company.id}>
      <li className="hover:bg-pink-400 md:min-w-[40rem] lg:min-w-[60rem] xl:min-w-[75rem] border-b-1 last:border-b-0 border-slate-500">
        <div className="flex justify-between items-center p-5">
          <div>
            <p className="text-xl">{company.company_profile.name}</p>
            <p>Location: {company.company_profile.location}</p>
            <p className="md:hidden text-slate-500">{company.email}</p>
          </div>
          <div className="hidden md:inline">
            <p className="text-slate-500">{company.email}</p>
          </div>
          <div className="bg-green-200 px-5 py-2 border-2 rounded-sm">
            <p className="text-emerald-950 font-medium">
              {company.company_profile.status}
            </p>
          </div>
        </div>
      </li>
    </Link>
  ));

  return (
    <>
      <div className="flex justify-center">
        <h1 className="text-2xl font-medium">COMPANIES</h1>
      </div>

      <div className="bg-red-500">
        <div className="flex justify-center">
          <input
            type="text"
            className="bg-white p-2 outline min-w-[18.5rem] md:min-w-[30rem] lg:min-w-[50rem] xl:min-w-[65rem]"
            placeholder="search companies"
            ref={queryInputRef}
          />
          <button
            onClick={() => handleSearch()}
            className="bg-yellow-400 min-w-[4rem] md:min-w-[10rem] lg:min-w-[10rem] xl:min-w-[10rem] px-2"
          >
            search
          </button>
        </div>
        <div className="flex justify-center overflow-auto">
          {isCompaniesLoading == true && <p>Loading...</p>}
          {isCompaniesLoading == false && <ul>{companyRecords}</ul>}
          {companiesError == null && <p>{companiesError}</p>}
        </div>
      </div>
    </>
  );
}

export default CompanyList;
