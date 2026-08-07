import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import { createAppAsyncThunk } from "../../hooks";

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

export const fetchAdminCounts = createAppAsyncThunk(
  "admin/fetchCounts",
  async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/api/admin/count");
      if (!res.ok) throw Error("something went wrong");
      const data = await res.json();
      return data;
    } catch (e) {
      console.error(e);
    }
  },
);

const counterSlice = createSlice({
  name: "counter",
  initialState,
  reducers: {
    adminDashboardCountReducer: {
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
});

export const {} = counterSlice.actions;
export default counterSlice.reducer;
