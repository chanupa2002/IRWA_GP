import React, { useEffect, useState } from "react";
import { AuthAPI } from "../api";

export default function Account() {
  const [me, setMe] = useState(null);

  useEffect(() => {
    AuthAPI.me().then(setMe).catch(() => setMe(null));
  }, []);

  return (
    <div className="container">
      <div className="card">
        <h2 className="section-title">Account Management</h2>
        <div className="subtle">Manage your profile and security.</div>

        <div className="stack" style={{ marginTop: 16 }}>
          <div><b>User:</b> {me?.username ?? "—"}</div>

          <div className="card">
            <div className="label">Change Password</div>
            <div className="row">
              <input className="input" type="password" placeholder="New password" />
              <button className="btn">Update</button>
            </div>
            <div className="subtle" style={{ marginTop: 6 }}>
              (Wire this to your backend endpoint, e.g., <code>/auth/change-password</code>)
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
