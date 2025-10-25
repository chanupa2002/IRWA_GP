import { useState } from "react";
import FeedbackForm from "./FeedbackForm"; // your existing feedback form
import "./StickyFeedback.css";

export default function StickyFeedback() {
  const [open, setOpen] = useState(false);

  return (
    <>
      {/* Floating Chat Button */}
      <button
        className="chat-fab"
        onClick={() => setOpen(!open)}
        title="Give Feedback"
      >
        💬
      </button>

      {/* Chat Popup Box */}
      {open && (
        <div className="chat-popup">
          <div className="chat-header">
            <h4>Feedback</h4>
            <button className="close-btn" onClick={() => setOpen(false)}>
              ✖
            </button>
          </div>
          <div className="chat-body">
            <FeedbackForm />
          </div>
        </div>
      )}
    </>
  );
}
