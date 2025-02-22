"use client";
// import Image from "next/image";
import { useState } from "react";

export default function Home() {
  const [jsonInput, setJsonInput] = useState("");
  const [processedSchema, setProcessedSchema] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const response = await fetch("/api/process-schema", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ schema: jsonInput }),
      });

      const data = await response.json();
      setProcessedSchema(data.processed_schema);
    } catch (error) {
      console.error("Error processing schema:", error);
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className=' font-[family-name:var(--font-geist-sans)]'>
      <main className=''>
        <div className='min-h-screen bg-gray-900 text-white flex items-center justify-center p-4'>
          {!processedSchema ? (
            // Show JSON input first
            <div className='w-full max-w-3xl'>
              <label className='block text-lg font-semibold mb-2'>
                Schema (JSON Format)
              </label>
              <textarea
                className='w-full h-40 bg-gray-800 text-white p-3 rounded-lg border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500'
                placeholder='Paste your schema here...'
                value={jsonInput}
                onChange={(e) => setJsonInput(e.target.value)}
              ></textarea>
              <button
                className='mt-3 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white font-semibold'
                onClick={handleSubmit}
                disabled={loading}
              >
                {loading ? "Processing..." : "Submit"}
              </button>
            </div>
          ) : (
            // Show processed schema and query UI
            <div className='w-full max-w-6xl grid grid-cols-2 gap-4'>
              {/* Left: Processed Schema */}
              <div className='bg-gray-800 p-4 rounded-lg border border-gray-700'>
                <h2 className='text-lg font-semibold mb-2'>Processed Schema</h2>
                <pre className='text-gray-400 overflow-auto max-h-80'>
                  {JSON.stringify(processedSchema, null, 2)}
                </pre>
              </div>

              {/* Right: Content Box with Query */}
              <div className='bg-gray-800 p-4 rounded-lg border border-gray-700 flex flex-col justify-between'>
                <div className='flex-grow flex items-center justify-center'>
                  <p className='text-gray-400'>
                    (Content will be displayed here)
                  </p>
                </div>
                <div className='mt-4'>
                  <label className='block text-lg font-semibold mb-2'>
                    Enter your query
                  </label>
                  <input
                    type='text'
                    className='w-full p-3 bg-gray-700 text-white rounded-lg border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500'
                    placeholder='Type your query...'
                  />
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
      <footer className='items-center justify-center'></footer>
    </div>
  );
}
