import { useState } from "react";
import FeedbackForm from "./FeedbackForm";
import "./StickyFeedback.css";

export default function StickyFeedback() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        className="feedback-fab"
        onClick={() => setOpen(true)}
        title="Give Feedback"
      >
        💬
      </button>

      {open && (
        <div className="feedback-modal">
          <div className="feedback-modal-content">
            <button className="close-btn" onClick={() => setOpen(false)}>
              ✖
            </button>
            <FeedbackForm />
          </div>
        </div>
      )}
    </>
  );
}
