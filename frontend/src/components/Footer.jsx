import "./Footer.css";

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <p>© {new Date().getFullYear()} Paper Forge</p>
        <p className="footer-tagline">
          Academic Literature Review AI Agent | Empowering researchers with AI-driven literature insights
        </p>
      </div>
    </footer>
  );
}
