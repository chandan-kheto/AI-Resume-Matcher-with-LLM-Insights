
import React, { useState } from "react";
import UploadBox from "../components/UploadBox";
import ResultCard from "../components/ResultCard";
import Loader from "../components/Loader";
import { uploadResume } from "../services/api";

function Home() {
  const [results, setResults] = useState({
    top: null,
    others: []
  });

  const [loading, setLoading] = useState(false);

  // 🔥 HANDLE UPLOAD
  const handleUpload = async (file) => {
    setLoading(true);

    try {
      const res = await uploadResume(file);

      console.log("FULL RESPONSE:", res);

      // ✅ FIXED: correct structure
      setResults({
        top: res.matches?.top_match || null,
        others: res.matches?.others || []
      });

    } catch (err) {
      console.error("Upload error:", err);
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white px-6 py-10">
      <div className="max-w-3xl mx-auto text-center">

        {/* TITLE */}
        <h1 className="text-3xl font-bold mb-2">
          🧠 AI Resume Matcher
        </h1>

        <p className="text-gray-300 text-xs pl-5 mb-5">
          Upload your resume and get AI-powered job matches instantly
        </p>

        {/* UPLOAD */}
        <UploadBox onUpload={handleUpload} />

        {/* LOADING */}
        {loading && <Loader />}

        {/* RESULTS */}
        {!loading && results.top && (
          <div className="mt-8 space-y-6 text-left">

            {/* 🏆 TOP MATCH */}
            <div>
              <h2 className="text-xl font-bold text-cyan-300 mb-3">
                🏆 Top Match
              </h2>

              <ResultCard job={results.top} index={0} isTop />
            </div>

            {/* 💡 OTHER OPTIONS */}
            {results.others.length > 0 && (
              <div>
                <h2 className="text-lg font-semibold text-blue-400 mb-3">
                  💡 Other Opportunities
                </h2>

                <div className="space-y-4">
                  {results.others.map((job, index) => (
                    <ResultCard
                      key={index}
                      job={job}
                      index={index + 1}
                    />
                  ))}
                </div>
              </div>
            )}

          </div>
        )}

        {/* ❌ NO RESULT */}
        {!loading && !results.top && (
          <p className="text-gray-400 text-xs mt-1">
            Upload your resume to see matches
          </p>
        )}

      </div>
    </div>
  );
}

export default Home;