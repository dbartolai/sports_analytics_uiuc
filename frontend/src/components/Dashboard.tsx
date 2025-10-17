import React from "react";
import "../styles/Dashboard.css";

const Dashboard: React.FC = () => {
  const data = {
    overall: { bets: 8, profit: 40 },
    parlays: { bets: 2, profit: -3.2 },
    moneylines: { bets: 1, profit: 13.2 },
    playerProps: { bets: 4, profit: 15 },
    overUnder: { bets: 1, profit: 25 },
  };

  return (
    <div className="dashboard">
      <nav className="nav-bar">
        <div className="nav-left">
          <h1 className="logo">SAS</h1>
          <ul className="nav-links">
            <li>Dashboard</li>
            <li>History</li>
            <li>Insights</li>
            <li>Popular Picks</li>
            <li>SAS AI</li>
            <li>Sync Books</li>
            <li>About Us</li>
          </ul>
        </div>
        <div className="nav-right">
          <button className="profile-btn">RG</button>
        </div>
      </nav>

      <div className="content">
        <section className="welcome">
          <h2>Welcome, User!</h2>
          <p>Your personalized betting dashboard.</p>
        </section>

        <section className="trend-section">
          <div className="trend-card">
            <h3>Monthly Trendline</h3>
            <div className="chart-placeholder">📈 (Chart Coming Soon)</div>
            <p className="trendline-msg">
              Your profits have increased <span className="highlight">50%</span> in the last month! Keep it up.
            </p>
          </div>
        </section>

        <section className="info-section">
          <h3>Betting Overview</h3>
          <table className="stats-table">
            <thead>
              <tr>
                <th>Category</th>
                <th>Total Bets</th>
                <th>Profit</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(data).map(([key, val]) => (
                <tr key={key}>
                  <td className="label">{key}</td>
                  <td>{val.bets}</td>
                  <td className={val.profit >= 0 ? "profit" : "loss"}>
                    ${val.profit.toFixed(2)}
                  </td>
                  <td>
                    <button className="insights-btn">Insights</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="ai-section">
          <div className="ai-card">
            <h3>SAS AI Insights</h3>
            <p className="ai-text">
              You are <span className="highlight">varying your bet sizes</span> too much.
            </p>
            <ul className="ai-suggestions">
              <li>1. Maintain consistent bet sizes</li>
              <li>2. Avoid large multi-leg parlays</li>
            </ul>
            <div className="ai-buttons">
              <button>View Bet Sizes</button>
              <button>View Parlays</button>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Dashboard;
