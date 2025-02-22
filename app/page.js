"use client";

import { Button } from "@/components/ui/button";
import React, { useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { RefreshCcw, Send } from "lucide-react";
import Chat from "@/components/main/Chat";
import Output from "@/components/main/Output";
import Spinner from "@/components/ui/spinner";

const page = () => {
  const fileInputRef = useRef(null);
  const [isFileUploaded, setIsFileUploaded] = useState(false);
  const [outputData, setOutputData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [chatMessages, setChatMessages] = useState([]);
  const [originalData, setOriginalData] = useState(null);
  const [isChatLoading, setIsChatLoading] = useState(false);

  const handleButtonClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = async (e) => {
      const fileContent = e.target.result;
      console.log(fileContent);

      setIsLoading(true);
      try {
        const response = await fetch("http://127.0.0.1:5000/process_schema", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ input: fileContent }),
        });

        if (response.ok) {
          const data = await response.json();
          console.log("Server response:", data);
          setOutputData(data.schema);
          setOriginalData(data);
        } else {
          console.error("Failed to process schema");
        }
      } catch (error) {
        console.error("Error:", error);
      } finally {
        setIsLoading(false);
      }
    };

    reader.readAsText(file);
    setIsFileUploaded(true);
  };

  const handleSendMessage = async (message) => {
    setChatMessages([...chatMessages, { type: "user", text: message }]);
    setIsChatLoading(true);
    try {
      const response = await fetch(`http://127.0.0.1:5000/process_query?query=${message}`);
      if (response.ok) {
        const data = await response.json();
        console.log("Server response:", data);
        setOutputData(data.selected_tables);
        setChatMessages([...chatMessages, { type: "user", text: message }, { type: "bot", text: "Query processed successfully" }]);
      } else {
        setChatMessages([...chatMessages, { type: "user", text: message }, { type: "bot", text: "Failed to process query, Try again." }]);
      }
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setIsChatLoading(false);
    }
  };

  const handleRefreshClick = () => {
    setOutputData(originalData.schema);
  };

  return (
    <div className="flex flex-col items-center size-full justify-center ">
      <AnimatePresence>
        {isFileUploaded === false && (
          <>
            <motion.div
              initial={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex flex-col absolute size-full items-center justify-center"
            >
              <div className="mb-4">
                Get started by uploading your schema json
              </div>
              <input
                type="file"
                ref={fileInputRef}
                style={{ display: "none" }}
                onChange={handleFileChange}
              />
              <Button variant="outline" onClick={handleButtonClick}>
                Upload file
              </Button>
              {/* {isFileUploaded && <div className='mt-4'>File uploaded successfully!</div>} */}
            </motion.div>
          </>
        )}
      </AnimatePresence>
      <AnimatePresence>
        {isFileUploaded && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="size-full flex flex-col items-center justify-center"
          > 

              
            <div className="flex h-full">
              <div className="flex items-center justify-center flex-col border-r-2 border-border  w-[50vw] relative">
                <Chat onSendMessage={handleSendMessage} messages={chatMessages} isLoading={isLoading || isChatLoading}></Chat>
              </div>
              <div className="flex items-center justify-center flex-col w-[50vw] h-full">
                <Output data={outputData} isLoading={isLoading} onRefreshClick={handleRefreshClick}></Output>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default page;
