
export const uploadResume = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("http://127.0.0.1:8000/match", {
    method: "POST",
    body: formData,
  });

  const data = await res.json();
  return data; // 🔥 return clean json
};