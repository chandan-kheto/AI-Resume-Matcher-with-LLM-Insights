
import React from "react";

function ResultCard({ job, index, isTop }) {
  const score = job["Match Score"];
  const confidence = job["Confidence"];

  const color =
    confidence === "High"
      ? "bg-green-500"
      : confidence === "Medium"
      ? "bg-yellow-500"
      : "bg-red-500";

  return (
    <div className="bg-slate-900 p-5 rounded-2xl border border-slate-700 text-left">

         {/* TITLE */}
      <h3 className="text-white text-sm font-semibold mb-2">
        #{index + 1} 💼 {job["Job Title"]}

      </h3>

      {/* DESCRIPTION */}
      <p className="text-yellow-200 mb-3 text-sm line-clamp-3">
        {job["Job Description"]?.slice(0, 200)}...
      </p>

      {/* SCORE */}
      <p className="mb-2 text-sm text-emerald-300 font-medium">
        Match Score: {score.toFixed(2)}%
      </p>
               {/* PROGRESS BAR */}
      <div className="w-full bg-slate-700 h-2 rounded-full mb-2">
        <div
          className={`${color} h-2 rounded-full`}
          style={{ width: `${score}%` }}
        />
      </div>

             {/* CONFIDENCE */}
      <p className="text-sm text-cyan-300">
        Confidence: {confidence}
      </p>

       {/* WHY MATCHED */}
      {job["Why Matched"] && (
        <p className="text-blue-300 text-sm mt-2">
          {job["Why Matched"]}
        </p>
      )}

       {/* MATCHED SKILLS */}
      {job["Matched Skills"]?.length > 0 && (
        <p className="text-green-400 text-sm mt-2">
          Skills: {job["Matched Skills"].join(", ")}
        </p>
      )}

      {job["Missing Skills"]?.length > 0 && (
        <p className="text-red-400 text-sm mt-2">
          Missing: {job["Missing Skills"].join(", ")}
        </p>
      )}

    </div>
  );
}

export default ResultCard;