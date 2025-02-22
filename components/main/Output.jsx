"use client";
import React from "react";
import JSONPretty from "react-json-pretty";
import "@/app/json.css"
import { Button } from "../ui/button";
import { RefreshCcw } from "lucide-react";
import Spinner from "../ui/spinner";// Assuming you have a Spinner component

const Output = ({ data, isLoading, onRefreshClick }) => {
  return (
    <div className="flex flex-col size-full">
      <div className="h-16 shrink-0 border-b-2 p-4 items-center justify-between flex w-full border-border">
        Output JSON
        <div><Button variant="" onClick={onRefreshClick}>Reset to Original<RefreshCcw></RefreshCcw></Button></div>
      </div>
      <div className="flex size-full overflow-y-auto overflow-x-hidden p-2">
        <div id="mono-font" className="bg-accent/40 h-fit w-full rounded-lg p-2 ">
          {" "}
          {isLoading ? (
            <div className="flex justify-center items-center h-full">
              <Spinner />
            </div>
          ) : (
            <JSONPretty
              style={{fontFamily: "monospace"}}
              data={data ? JSON.stringify(data, null, 2) : `{}`}
            ></JSONPretty>
          )}
        </div>
      </div>
    </div>
  );
};

export default Output;
