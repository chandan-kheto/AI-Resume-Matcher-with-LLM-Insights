
import React, { useState } from "react";

function UploadBox({ onUpload }) {
  const [file, setFile] = useState(null);

  return (
    <div className="bg-slate-900 p-6 rounded-2xl border border-slate-700 text-center">

      {/* File Input */}
      <div className="flex flex-col pl-27 items-center justify-center mb-4">

        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          className="text-gray-300 text-center"
        />

        {file && (
          <p className="text-sm text-gray-400 mt-2">
            Selected: {file.name}
          </p>
        )}

      </div>

      {/* Button */}
      <div className="flex mt-8 justify-center">
        <button
          onClick={() => {
            console.log("Analyze clicked 🔥");
            file && onUpload(file);
          }}
          disabled={!file}
          className={`px-2 py-3 text-xs rounded-lg font-semibold transition ${
            file
              ? "bg-green-500 text-white"
              : "bg-green-500 text-white cursor-not-allowed"
          }`}
        >
          Analyze Resume 🚀
        </button>
      </div>

    </div>
  );
}

export default UploadBox;