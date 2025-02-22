// import Image from "next/image";

export default function Home() {
  return (
    <div className=" font-[family-name:var(--font-geist-sans)]">
      <main className="">
      <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center p-4">
      {/* Top: JSON Schema Input */}
      <div className="w-full max-w-3xl mb-4">
        <label className="block text-lg font-semibold mb-2">Schema (JSON Format)</label>
        <textarea
          className="w-full h-40 bg-gray-800 text-white p-3 rounded-lg border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Paste your schema here..."
        ></textarea>
      </div>
      
      {/* Middle: Placeholder for future content */}
      <div className="w-full max-w-3xl flex-grow bg-gray-800 rounded-lg p-4 flex items-center justify-center border border-gray-700">
        <p className="text-gray-400">(Content will be displayed here)</p>
      </div>
      
      {/* Bottom: NL Query Input */}
      <div className="w-full max-w-3xl mt-4">
        <label className="block text-lg font-semibold mb-2">Enter your query</label>
        <input
          type="text"
          className="w-full p-3 bg-gray-800 text-white rounded-lg border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Type your query..."
        />
      </div>
    </div>
        
      </main>
      <footer className="items-center justify-center">
        
      </footer>
    </div>
  );
}
