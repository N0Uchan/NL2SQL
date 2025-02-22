"use client";
import React from "react";
import JSONPretty from "react-json-pretty";
import "@/app/json.css"

const Output = () => {
  return (
    <div className="flex flex-col size-full">
      <div className="h-16 shrink-0 border-b-2 p-4 items-center flex w-full border-border">
        Output JSON
      </div>
      <div className="flex size-full overflow-y-auto overflow-x-hidden p-2">
        <div id="mono-font" className="bg-accent/40  w-full rounded-lg p-2 ">
          {" "}
          <JSONPretty
          style={{fontFamily: "monospace"}}
            data={`{
    "users": {"columns": ["id", "name", "email", "signup_date"]},
    "orders": {"columns": ["id", "user_id", "amount", "status"]},
    "products": {"columns": ["id", "name", "price", "stock"]}
}`}
          ></JSONPretty>
        </div>
      </div>
    </div>
  );
};

export default Output;
