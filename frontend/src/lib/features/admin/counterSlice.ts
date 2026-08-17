import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import { createAppAsyncThunk } from "../../hooks";
import type { RootState } from "../../store";

interface AdminDashboardCount {
  companies: number;
  students: number;
  jobs: number;
}

interface AdminDashboardCountState {
  count: AdminDashboardCount;
  status: "idle" | "pending" | "succeeded" | "failed";
  error: string | null;
}

const initialState: AdminDashboardCountState = {
  count: {
    companies: 0,
    students: 0,
    jobs: 0,
  },
  status: "idle",
  error: null,
};

const counterSlice = createSlice({
  name: "counter",
  initialState,
  reducers: {
    adminDashboardCount: {
      reducer(state, action: PayloadAction<AdminDashboardCount>) {
        state.count = action.payload;
      },
      prepare(companies: number, students: number, jobs: number) {
        return {
          payload: { companies, students, jobs },
        };
      },
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchAdminCounts.pending, (state, _) => {
        state.status = "pending";
      })
      .addCase(fetchAdminCounts.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.count = action.payload;
      })
      .addCase(fetchAdminCounts.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.error.message ?? "unknown Error";
      });
  },
});

export const fetchAdminCounts = createAppAsyncThunk(
  "admin/fetchCounts",
  async () => {
    const res = await fetch(`${import.meta.env.VITE_ADMIN_API}/count`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${import.meta.env.VITE_ADMIN_JWT}`,
      },
    });
    const data = await res.json();
    return data;
  },
);

export const {} = counterSlice.actions;
export const selectCount = (state: RootState) => state.counter.count;
export const selectCountStatus = (state: RootState) => state.counter.status;
export const selectCountError = (state: RootState) => state.counter.error;
export default counterSlice.reducer;
