import { useEffect, useRef, useState, type SubmitEvent } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { toast } from "react-toastify";

export interface StudentProfile {
  id: number;
  first_name: string;
  last_name: string;
  school: string;
  cgpa: number;
  status: string;
  resume_path: string;
  phone_number: string;
}

interface Student {
  id: number;
  email: string;
  username: string;
  role: "student";
  student_profile: StudentProfile;
}

function statusVariant(status: string) {
  if (status === "active") {
    return "success";
  } else if (status === "pending") {
    return "warning";
  } else if (status === "rejected") {
    return "destructive";
  } else if (status === "blacklisted") {
    return "secondary";
  }
  return "default";
}

function StudenList() {
  const queryInputRef = useRef(null);

  const [isStudentsLoading, setIsStudentsLoading] = useState<boolean>(false);
  const [studentsError, setStudentsError] = useState<string | null>();
  const [students, setStudents] = useState<Array<Student>>([]);

  const [studentDetail, setStudentDetail] = useState<any>();
  const [open, setOpen] = useState<boolean>();

  const [query, setQuery] = useState<string>("");
  const [search, setSearch] = useState<boolean>(false);

  console.log(open);
  console.log(studentDetail);

  useEffect(() => {
    fetchStudents();
  }, [search]);

  async function fetchStudents() {
    setIsStudentsLoading(true);
    setStudentsError(null);
    try {
      const response = await fetch(
        `${import.meta.env.VITE_ADMIN_API}/students?q=${query}`,
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
      const { data } = await response.json();
      setStudents(data);
    } catch (e) {
      setStudentsError(e);
    } finally {
      setIsStudentsLoading(false);
    }
  }

  function handleSearch(e: SubmitEvent<HTMLFormElement>) {
    e.preventDefault();
    setQuery(queryInputRef.current.value);
    setSearch((search) => !search);
  }

  const studentRecords = students.map((student) => (
    <li
      className="bg-card p-5 justify-self-center rounded-sm w-[14rem] flex-wrap hover:cursor-pointer"
      onClick={() => {
        setStudentDetail(student);
        setOpen(true);
      }}
      key={student.id}
    >
      <div className="text-card-foreground">
        <p>
          {student.student_profile.first_name}{" "}
          {student.student_profile.last_name}
        </p>
        <p className="text-gray-500 mb-2">{student.student_profile.school}</p>
        <p className="text-gray-500/70 text-sm">
          CGPA: {student.student_profile.cgpa}
        </p>
        <p className="text-gray-500/70 text-sm">Username: {student.username}</p>
        <p className="text-gray-500/70 text-sm">Email: {student.email}</p>
        <Button
          className="mt-2"
          variant={statusVariant(student.student_profile.status)}
        >
          {student.student_profile.status}
        </Button>
      </div>
    </li>
  ));

  return (
    <>
      {open && studentDetail && (
        <StudentDetail
          open={open}
          setOpen={setOpen}
          student={studentDetail}
          fetchStudents={fetchStudents}
        />
      )}

      <div className="flex justify-center">
        <h1 className="text-2xl font-medium text-white">STUDENTS</h1>
      </div>
      <div className="">
        <form onSubmit={handleSearch}>
          <div className="flex justify-center">
            <Input
              type="text"
              placeholder="search companies"
              ref={queryInputRef}
            />
            <button
              className="bg-yellow-400 min-w-[4rem] md:min-w-[10rem] lg:min-w-[10rem] xl:min-w-[10rem] px-2"
              disabled={isStudentsLoading}
            >
              search
            </button>
          </div>
        </form>
        <div>
          {isStudentsLoading == true && <p>Loading...</p>}
          {isStudentsLoading == false && (
            <ul className="grid grid-cols-1 2xl:grid-cols-6 xl:grid-cols-5 lg:grid-cols-4 md:grid-cols-3  sm:grid-cols-2 mt-[1rem] gap-[1rem] bg-rose-900">
              {studentRecords}
            </ul>
          )}
          {studentsError == null && <p>{studentsError}</p>}
        </div>
      </div>
    </>
  );
}

export function StudentDetail({ student, open, setOpen, fetchStudents }) {
  const [blacklistStudentLoading, setBlacklistStudentLoading] =
    useState<boolean>();
  const [blacklistStudentError, setBlacklistStudentError] = useState<
    null | string
  >();

  async function blacklistStudent(studentId: number) {
    setBlacklistStudentLoading(true);
    setBlacklistStudentError(null);
    try {
      const response = await fetch(
        `${import.meta.env.VITE_ADMIN_API}/student/${studentId}/blacklist`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${import.meta.env.VITE_ADMIN_JWT}`,
          },
        },
      );
      if (!response.ok) {
        const error = await response.json();
        throw error.message;
      }
      const { message } = await response.json();
      toast.success(message);
      fetchStudents();
      setOpen(false);
    } catch (e) {
      setBlacklistStudentError(e);
      toast.error(e);
    } finally {
      setBlacklistStudentLoading(false);
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <form>
        <DialogContent className="sm:max-w-sm gap-1">
          <DialogHeader>
            <DialogTitle className="text-xl">
              {student.student_profile.first_name}{" "}
              {student.student_profile.last_name}
            </DialogTitle>
          </DialogHeader>
          <p>School: {student.student_profile.school}</p>
          <p>CGPA: {student.student_profile.cgpa}</p>
          <p>username: {student.username}</p>
          <p>email: {student.email}</p>
          <a
            className="text-blue-800 px-2 p-1 bg-blue-200 justify-self-start rounded-sm"
            target="_blank"
            href={student.student_profile.resume_path}
          >
            Resume
          </a>
          <Button
            className="mt-2 justify-self-start"
            variant={statusVariant(student.student_profile.status)}
          >
            {student.student_profile.status}
          </Button>
          <DialogFooter>
            <DialogClose render={<Button variant="outline">Cancel</Button>} />
            <Button
              type="submit"
              onClick={() => blacklistStudent(student.student_profile.id)}
              disabled={
                student.student_profile.status === "blacklisted" ||
                blacklistStudentLoading
              }
            >
              Blacklist
            </Button>
          </DialogFooter>
        </DialogContent>
      </form>
    </Dialog>
  );
}

export default StudenList;
