import { useState } from "react";
import { useAppDispatch, useAppSelector } from "../../lib/hooks";
import {
  increment,
  decrement,
  incrementByAmount,
} from "../../lib/features/counter/counterSlice";

function AdminDashboard() {
  const count = useAppSelector((state) => state.counter.value);
  const dispatch = useAppDispatch();
  const [inputDigit, setInputDigit] = useState<number>(0);
  return (
    <>
      <h1>Counter Dashboard</h1>
      <p>{count}</p>
      <input
        type="number"
        onChange={(e) => setInputDigit(parseInt(e.target.value))}
      />
      <button
        className="border-purple-200 text-purple-600"
        onClick={() => dispatch(increment())}
      >
        +
      </button>
      <button
        className="border-purple-200 text-purple-600"
        onClick={() => dispatch(decrement())}
      >
        -
      </button>
      <button
        className="border-purple-200 text-purple-600"
        onClick={() => dispatch(incrementByAmount(inputDigit))}
      >
        Add
      </button>
    </>
  );
}

export default AdminDashboard;
