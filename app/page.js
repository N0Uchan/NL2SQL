"use client"

import { Button } from '@/components/ui/button'
import React, { useRef, useState } from 'react'
import {motion,AnimatePresence} from 'framer-motion'

const page = () => {
  const fileInputRef = useRef(null);
  const [isFileUploaded, setIsFileUploaded] = useState(false);

  const handleButtonClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && file.type === "application/json") {
      setIsFileUploaded(true);
    }
  };

  return (
    <div className='flex flex-col size-full items-center justify-center '>
      <div className='mb-4'>Get started by uploading your schema json</div>
      <input
        type="file"
        ref={fileInputRef}
        style={{ display: 'none' }}
        onChange={handleFileChange}
      />
      <Button variant="outline" onClick={handleButtonClick}>Upload file</Button>
      {isFileUploaded && <div className='mt-4'>File uploaded successfully!</div>}
    </div>
  )
}

export default page