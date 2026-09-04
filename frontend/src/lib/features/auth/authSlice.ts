import type { RootState } from "@/lib/store";
import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import { createAppAsyncThunk } from "@/lib/hooks";

interface UserData {
  id: number | null;
  email: string | null;
  role: "admin" | "company" | "student" | null;
  student_status?: "active" | "blacklisted";
  company_status?: "approved" | "pending" | "rejected";
}
interface AuthResponse {
  message: string | null;
  token: string | null;
  user: UserData;
}

interface AuthState {
  data: AuthResponse;
  status: "idle" | "pending" | "success" | "failed";
  errorMessage: string | null;
}

interface LoginRequest {
  username: string | null;
  email: string | null;
  password: string;
}

const initialState: AuthState = {
  data: {
    message: null,
    token: JSON.parse(localStorage.getItem("token")) || null,
    user: JSON.parse(localStorage.getItem("user")) || {
      id: null,
      email: null,
      role: null,
    },
  },
  status: "idle",
  errorMessage: null,
};

export const login = createAppAsyncThunk(
  "auth/fetchLogin",
  async ({ username, email, password }: LoginRequest) => {
    const res = await fetch(`${import.meta.env.VITE_API}/login`, {
      method: "POST",
      body: JSON.stringify({ username, email, password }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!res.ok) {
      const errMsg = await res.json();
      throw errMsg.error;
    }
    const data = await res.json();
    return data;
  },
);

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    logout: (state) => {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      state.data = {
        message: null,
        token: null,
        user: {
          id: null,
          email: null,
          role: null,
        },
      };
    },
    updateCompanyStatus: (
      state,
      action: PayloadAction<UserData["company_status"]>,
    ) => {
      state.data.user.company_status = action.payload;
    },
    updateStudentStatus: (
      state,
      action: PayloadAction<UserData["student_status"]>,
    ) => {
      state.data.user.student_status = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state, _) => {
        state.status = "pending";
      })
      .addCase(login.fulfilled, (state, action) => {
        state.status = "success";
        state.data = action.payload;
        localStorage.setItem("token", JSON.stringify(state.data.token));
        localStorage.setItem("user", JSON.stringify(state.data.user));
        state.errorMessage = null;
      })
      .addCase(login.rejected, (state, action) => {
        state.status = "failed";
        state.errorMessage = action.error.message;
      });
  },
});

export default authSlice.reducer;

export const { logout, updateCompanyStatus, updateStudentStatus } =
  authSlice.actions;

export const selectUserData = (state: RootState) => state.auth.data;
export const selectLoginStatus = (state: RootState) => state.auth.status;
export const selectLoginErrorMessage = (state: RootState) =>
  state.auth.errorMessage;
