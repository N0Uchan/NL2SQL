"use client";
import React from "react";
import { Button } from "../ui/button";
import { Send } from "lucide-react";

const Chat = () => {
  return (
    <>
    <div className="h-16 flex p-4 border-b-2 border-border w-full shrink-0 items-center " >Your Queries</div>
      <div className="h-full w-full p-2 flex flex-col overflow-x-hidden overflow-y-auto">
        <Message type="user">This is a message</Message>
        <Message type="bot">This is a bot message</Message>
      </div>
      <div className="flex w-full shrink-0 h-16  border-t-2 border-border">
        <input
          placeholder="Enter your query here"
          className="w-full  bg-background outline-none border-none p-4 "
        ></input>
        <Button
          variant="ghost"
          className="h-full border-l-2 border-border aspect-square shrink-0 rounded-none"
        >
          <Send></Send>
        </Button>
      </div>
    </>
  );
};

const Message = ({ children, type }) => {
  if (type === "user") {
    return (
      <div className="flex justify-end">
        <div className="w-fit  p-2 px-4 bg-accent rounded-lg">
          {children}
        </div>
      </div>
    );
  }
  else if (type === "bot") {
    return (
      <div className="flex justify-start">
        <div className="w-fit  p-2 px-4 bg-primary/20 rounded-lg">
          {children}
        </div>
      </div>
    );
  }
};

export default Chat;
