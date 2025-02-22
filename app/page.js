"use client";

import { Button } from "@/components/ui/button";
import React, { useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { RefreshCcw, Send } from "lucide-react";
import Chat from "@/components/main/Chat";
import Output from "@/components/main/Output";

const page = () => {
  const fileInputRef = useRef(null);
  const [isFileUploaded, setIsFileUploaded] = useState(true);

  const handleButtonClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    console.log(file);
    setIsFileUploaded(true);
  };

  return (
    <div className="flex flex-col size-full items-center justify-center ">
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

              <div className="flex h-16 shrink-0 w-full border-b-2 border-border items-center justify-center p-4" >

                NL2SQL
                <div className="ml-auto flex justify-center items-center gap-2" >
                  <Button variant="outline">Upload another  </Button>
                  <Button variant=""><RefreshCcw></RefreshCcw></Button>
                </div>
              </div>
            <div className="flex h-full">
              <div className="flex items-center justify-center flex-col w-[50vw] h-full border-r-2 border-border relative">
                <Chat></Chat>
              </div>
              <div className="flex items-center justify-center flex-col w-[50vw] h-full">
                <Output></Output>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default page;
