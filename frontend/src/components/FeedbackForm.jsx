import { useState } from "react";
import "./Feedback.css";

export default function FeedbackForm() {
  const [form, setForm] = useState({ name: "", email: "", message: "" });
  const [status, setStatus] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus("Sending...");

    try {
      const res = await fetch("http://localhost:8000/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      if (!res.ok) throw new Error("Failed to send feedback");

      setStatus("✅ Feedback sent successfully! Thank you");
      setForm({ name: "", email: "", message: "" });

      setTimeout(() => setStatus(""), 5000);
    } catch (err) {
      setStatus("❌ Error sending feedback: " + err.message);
    }
  };

  return (
    <div className="feedback-card">
     
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          placeholder="Your Name"
          value={form.name}
          onChange={handleChange}
          required
        />
        <input
          type="email"
          name="email"
          placeholder="Your Email"
          value={form.email}
          onChange={handleChange}
          required
        />
        <textarea
          name="message"
          placeholder="Write your message..."
          rows="5"
          value={form.message}
          onChange={handleChange}
          required
        />
        <button type="submit" className="btn primary">Send Feedback</button>
      </form>
      {status && (
  <p
    className={`status-msg ${
      status.toLowerCase().includes("thank") ? "success" : "error"
    }`}
  >
    {status}
  </p>
)}

    </div>
  );
}
