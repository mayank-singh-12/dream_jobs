import { useEffect, useRef, useState, type SubmitEvent } from "react";
import { Input } from "@/components/ui/input";

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

function StudenList() {
  const queryInputRef = useRef(null);

  const [isStudentsLoading, setIsStudentsLoading] = useState<boolean>(false);
  const [studentsError, setStudentsError] = useState<string | null>();
  const [students, setStudents] = useState<Array<Student>>([]);

  const [query, setQuery] = useState<string>("");
  const [search, setSearch] = useState<boolean>(false);

  useEffect(() => {
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

    fetchStudents();
  }, [search]);

  function handleSearch(e: SubmitEvent<HTMLFormElement>) {
    e.preventDefault();
    setQuery(queryInputRef.current.value);
    setSearch((search) => !search);
  }

  const studentRecords = students.map((student) => (
    <li className="bg-card max-w-[28rem] my-2 p-5 rounded-sm" key={student.id}>
      <div className="text-card-foreground">
        <p>
          {student.student_profile.first_name}{" "}
          {student.student_profile.last_name}
        </p>
        <p className="text-gray-500">{student.student_profile.school}</p>
        <p className="text-gray-500">{student.student_profile.cgpa}</p>
        <p className="text-gray-500">{student.username}</p>
        <p className="text-gray-500">{student.email}</p>
        {student.student_profile.resume_path && (
          <a
            className="text-blue-500"
            target="_blank"
            href={student.student_profile.resume_path}
          >
            Resume
          </a>
        )}
      </div>
    </li>
  ));

  return (
    <>
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
            <ul className="grid grid-cols-5 gap-[1rem] bg-rose-900">
              {studentRecords}
            </ul>
          )}
          {studentsError == null && <p>{studentsError}</p>}
        </div>
      </div>
    </>
  );
}

export default StudenList;
