import type { RootState } from "@/lib/store";
import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import { createAppAsyncThunk } from "@/lib/hooks";
import { redirect } from "react-router";

interface UserData {
  id: number | null;
  email: string | null;
  role: "admin" | "company" | "student";
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
  email: string;
  password: string;
}

const initialState: AuthState = {
  data: {
    message: null,
    token: localStorage.getItem("token") || null,
    user: JSON.parse(localStorage.getItem("user")) || {
      id: null,
      email: null,
      role: "student",
    },
  },
  status: "idle",
  errorMessage: null,
};

export const login = createAppAsyncThunk(
  "auth/fetchLogin",
  async ({ email, password }: LoginRequest) => {
    const res = await fetch(`${import.meta.env.VITE_API}/login`, {
      method: "POST",
      body: JSON.stringify({ email, password }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!res.ok) {
      const errMsg = await res.json();
      throw new Error(errMsg.error);
    }
    const data = await res.json();
    return data;
  },
);

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state, _) => {
        state.status = "pending";
        console.log("slice pending");
      })
      .addCase(login.fulfilled, (state, action) => {
        state.status = "success";
        state.data = action.payload;
        localStorage.setItem("token", JSON.stringify(state.data.token));
        localStorage.setItem("user", JSON.stringify(state.data.user));
      })
      .addCase(login.rejected, (state, action) => {
        state.status = "failed";
        console.log(action);
        state.errorMessage = action.error.message;
      });
  },
});

export default authSlice.reducer;

export const selectUserData = (state: RootState) => state.auth.data;
export const selectLoginStatus = (state: RootState) => state.auth.status;
export const selectLoginErrorMessage = (state: RootState) =>
  state.auth.errorMessage;
