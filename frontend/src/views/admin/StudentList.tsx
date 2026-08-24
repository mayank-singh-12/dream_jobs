import { useEffect, useRef, useState } from "react";
import { Input } from "@/components/ui/input";

interface StudentProfile {
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

  useEffect(() => {
    async function fetchStudents() {
      setIsStudentsLoading(true);
      setStudentsError(null);

      try {
        const response = await fetch(
          `${import.meta.env.VITE_ADMIN_API}/students`,
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
  }, []);

  const studentRecords = students.map((student) => (
    <li className="bg-card my-2 p-5" key={student.id}>
      <div className="text-card-foreground">
        <p>
          {student.student_profile.first_name}{" "}
          {student.student_profile.last_name}
        </p>
        <p className="text-gray-500">{student.student_profile.school}</p>
        <p className="text-gray-500">{student.student_profile.cgpa}</p>
        <p className="text-gray-500">{student.username}</p>
        <p className="text-gray-500">{student.email}</p>
        <p className="text-gray-500">{student.student_profile.resume_path}</p>
      </div>
    </li>
  ));

  return (
    <>
      <div className="flex justify-center">
        <h1 className="text-2xl font-medium text-white">STUDENTS</h1>
      </div>
      {/* bg-red-500 */}
      <div className="">
        <div className="flex justify-center">
          <Input
            type="text"
            placeholder="search companies"
            ref={queryInputRef}
          />

          <button
            // onClick={() => handleSearch()}
            className="bg-yellow-400 min-w-[4rem] md:min-w-[10rem] lg:min-w-[10rem] xl:min-w-[10rem] px-2"
          >
            search
          </button>
        </div>
        <div className="flex justify-center overflow-auto">
          {isStudentsLoading == true && <p>Loading...</p>}
          {isStudentsLoading == false && <ul>{studentRecords}</ul>}
          {studentsError == null && <p>{studentsError}</p>}
        </div>
      </div>
    </>
  );
}

export default StudenList;
