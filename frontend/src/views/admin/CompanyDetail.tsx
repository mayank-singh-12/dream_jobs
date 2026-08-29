import { useState, useEffect, type SubmitEvent } from "react";
import { useParams } from "react-router";
import { useAppSelector } from "@/lib/hooks";
import { selectUserData } from "@/lib/features/auth/authSlice";
import type { CompanyProfile } from "./CompanyList";
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
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

interface CompanyDetail {
  id: number;
  company_profile: CompanyProfile;
  role: string;
  username: string;
}

function CompanyDetail() {
  const { companyId } = useParams();
  const { token } = useAppSelector(selectUserData);
  const [isCompanyLoading, setIsCompanyLoading] = useState<boolean>(false);
  const [companyError, setcompanyError] = useState<string | null>(null);
  const [company, setCompany] = useState<CompanyDetail>();
  const [open, setOpen] = useState<boolean>(false);

  const [companyStatus, setCompanyStatus] = useState<string>();

  useEffect(() => {
    fetchCompanyDetails(parseInt(companyId));
  }, []);

  async function fetchCompanyDetails(companyId: number) {
    try {
      setIsCompanyLoading(true);
      const response = await fetch(
        `${import.meta.env.VITE_ADMIN_API}/company/${companyId}`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );
      if (!response.ok) {
        const error = await response.json();
        throw error.message;
      }
      const { data } = await response.json();
      setCompany(data);
      setCompanyStatus(data.company_profile.status);
    } catch (e) {
      setcompanyError(e);
    } finally {
      setIsCompanyLoading(false);
    }
  }

  async function handleSelectStatus(
    e: SubmitEvent<HTMLFormElement>,
    companyId: number,
    updatedStatus: string,
  ) {
    e.preventDefault();
    try {
      const response = await fetch(
        `${import.meta.env.VITE_ADMIN_API}/company/${companyId}/${updatedStatus}`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );
      if (!response.ok) {
        const error = await response.json();
        throw error.message;
      }
      const { message } = await response.json();
      toast.success(message);
      fetchCompanyDetails(companyId);
      setOpen(false);
    } catch (e) {
      toast.error(e);
    }
  }

  const status = [
    { label: "Select status", value: null },
    { label: "Approved", value: "approve" },
    { label: "Pending", value: "pending" },
    { label: "Rejected", value: "reject" },
    { label: "Blacklist", value: "blacklist" },
  ];

  const companyProfileCard = company && (
    <div>
      <h1 className="text-3xl">{company.company_profile.name}</h1>
      <p className="text-white">{company.company_profile.website}</p>
      <p className="text-white">{company.company_profile.about}</p>
      <p className="">{company.company_profile.status}</p>
      <br />

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogTrigger
          render={<Button variant="outline">Edit Status</Button>}
        />
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Edit company status</DialogTitle>
            <DialogDescription>
              Change the status of this company.
            </DialogDescription>
          </DialogHeader>

          <form
            onSubmit={(e) =>
              handleSelectStatus(e, parseInt(companyId), companyStatus)
            }
          >
            <Select
              items={status}
              onValueChange={(s) => setCompanyStatus(s)}
              value={companyStatus}
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
            <Button type="submit">Update Status</Button>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
  return (
    <>
      {isCompanyLoading && <p>Loading...</p>}
      {companyError && <p className="text-red-500">{companyError}</p>}
      {company && <>{companyProfileCard}</>}
    </>
  );
}

export default CompanyDetail;
