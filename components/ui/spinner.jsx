import { Loader2 } from "lucide-react";
import React from "react";

const Spinner = () => {
  return (
    <div className="spinner-border animate-spin inline-block w-8 h-8 border-4 rounded-full" role="status">
      <span className="visually-hidden"><Loader2></Loader2></span>
    </div>
  );
};

export default Spinner;
