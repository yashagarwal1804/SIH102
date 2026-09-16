import { useEffect, useState } from "react";
import axios from "axios";
import {
  ShieldAlert,
  AlertTriangle,
  Activity,
  ClipboardList,
} from "lucide-react";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Legend,
} from "recharts";

import "./App.css";

function App() {

  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCase, setSelectedCase] = useState(null);
  const [investigationStarted, setInvestigationStarted] = useState(false);
  const [investigationStatus, setInvestigationStatus] =
    useState("Under Review");

  const [officerRemarks, setOfficerRemarks] = useState("");
  const [investigations, setInvestigations] = useState([]);
  const loadInvestigation = (caseItem) => {
    const existing = investigations.find(
      (item) =>
        item.constituency === caseItem.constituency &&
        item.year === caseItem.year
    );

    if (existing) {
      setInvestigationStarted(true);
      setInvestigationStatus(existing.status);
      setOfficerRemarks(existing.officer_remarks || "");
    } else {
      setInvestigationStarted(false);
      setInvestigationStatus("Under Review");
      setOfficerRemarks("");
    }
  };
  const saveInvestigation = async () => {
    if (!selectedCase) return;

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/investigations",
        {
          constituency: selectedCase.constituency,
          year: selectedCase.year,
          risk_score: selectedCase.risk_score,
          risk_category: selectedCase.risk_category,
          status: investigationStatus,
          officer_remarks: officerRemarks
        }
      );

      alert(response.data.message);

    } catch (error) {
      console.error(error);
      alert("Failed to save investigation.");
    }
  };
  const fetchInvestigations = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/api/investigations"
      );

      setInvestigations(response.data);
      console.log("Investigations from PostgreSQL:", response.data);
    } catch (error) {
      console.error("Failed to fetch investigations:", error);
    }
  };

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/anomalies")
      .then((response) => {
        setCases(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("API Error:", error);
        setLoading(false);
      });
  }, []);
  useEffect(() => {
    fetchInvestigations();
  }, []);

  const highRisk = cases.filter(
    (item) => item.risk_category === "HIGH"
  ).length;

  const mediumRisk = cases.filter(
    (item) => item.risk_category === "MEDIUM"
  ).length;

  const lowRisk = cases.filter(
    (item) => item.risk_category === "LOW"
  ).length;

  const totalPending = cases.reduce(
    (sum, item) => sum + item.pending_works,
    0
  );

  const averageUtilisation =
    cases.length > 0
      ? cases.reduce(
        (sum, item) => sum + item.pct_utilisation,
        0
      ) / cases.length
      : 0;

  const riskData = [
    {
      name: "High Risk",
      value: highRisk,
    },
    {
      name: "Medium Risk",
      value: mediumRisk,
    },
    {
      name: "Low Risk",
      value: lowRisk,
    },
  ];

  const performanceData = cases.slice(0, 8).map((item) => ({
    name: item.constituency,
    completion: Number(item.pct_completed.toFixed(1)),
    utilisation: Number(item.pct_utilisation.toFixed(1)),
  }));

  return (
    <div className="dashboard">

      {/* HEADER */}
      <header className="header">
        <div>
          <h1>MPLADS AI Monitor</h1>
          <p>
            AI-powered anomaly & risk detection system
          </p>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          System Online
        </div>
      </header>


      {/* KPI CARDS */}
      <section className="stats">

        <div className="stat-card">
          <Activity size={30} />
          <div>
            <p>Flagged Cases</p>
            <h2>{cases.length}</h2>
          </div>
        </div>

        <div className="stat-card high">
          <ShieldAlert size={30} />
          <div>
            <p>High Risk</p>
            <h2>{highRisk}</h2>
          </div>
        </div>

        <div className="stat-card medium">
          <AlertTriangle size={30} />
          <div>
            <p>Pending Works</p>
            <h2>
              {totalPending.toLocaleString()}
            </h2>
          </div>
        </div>

        <div className="stat-card">
          <ClipboardList size={30} />
          <div>
            <p>Avg Utilisation</p>
            <h2>
              {averageUtilisation.toFixed(1)}%
            </h2>
          </div>
        </div>

      </section>


      {/* CHARTS */}
      {!loading && (
        <section className="charts">

          {/* RISK CHART */}
          <div className="chart-card">

            <div className="chart-header">
              <h2>Risk Distribution</h2>
              <p>AI classified flagged cases</p>
            </div>

            <div className="chart">
              <ResponsiveContainer
                width="100%"
                height={280}
              >
                <PieChart>

                  <Pie
                    data={riskData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={95}
                    label
                  >

                    {riskData.map(
                      (entry, index) => (
                        <Cell
                          key={index}
                          fill={index === 0
                            ? "#dc2626"
                            : index === 1
                              ? "#f59e0b"
                              : "#16a34a"
                          }
                        />
                      )
                    )}

                  </Pie>

                  <Tooltip />

                </PieChart>
              </ResponsiveContainer>
            </div>

          </div>


          {/* PERFORMANCE CHART */}
          <div className="chart-card">

            <div className="chart-header">
              <h2>Work Performance</h2>
              <p>
                Completion vs fund utilisation
              </p>
            </div>

            <div className="chart">

              <ResponsiveContainer
                width="100%"
                height={280}
              >

                <BarChart
                  data={performanceData}
                >

                  <CartesianGrid
                    strokeDasharray="3 3"
                  />

                  <XAxis
                    dataKey="name"
                    angle={-35}
                    textAnchor="end"
                    height={80}
                  />

                  <YAxis />

                  <Tooltip />

                  <Legend />

                  <Bar
                    dataKey="completion"
                    name="Completion %"
                  />

                  <Bar
                    dataKey="utilisation"
                    name="Utilisation %"
                  />

                </BarChart>

              </ResponsiveContainer>

            </div>

          </div>

        </section>
      )}


      {/* CASE TABLE */}
      <section className="cases">

        <div className="section-header">

          <div>
            <h2>🚨 High-Risk Cases</h2>

            <p>
              Cases identified by the AI anomaly detection engine
            </p>
          </div>

        </div>


        {loading ? (
          <p className="loading">
            Loading AI results...
          </p>
        ) : (

          <div className="table-container">

            <table>

              <thead>

                <tr>
                  <th>Constituency</th>
                  <th>Year</th>
                  <th>Risk Score</th>
                  <th>Pending Works</th>
                  <th>Utilisation</th>
                  <th>Completion</th>
                  <th>Risk</th>
                  <th>Investigation</th>
                </tr>

              </thead>

              <tbody>

                {cases.map((item, index) => (

                  <tr
                    key={index}
                    onClick={() => {
                      setSelectedCase(item);
                      loadInvestigation(item);
                    }}
                    className="case-row"
                  >

                    <td>
                      <strong>
                        {item.constituency}
                      </strong>
                    </td>

                    <td>
                      {item.year}
                    </td>

                    <td>
                      <strong>
                        {item.risk_score}
                      </strong>
                    </td>

                    <td>
                      {item.pending_works}
                    </td>

                    <td>
                      {item.pct_utilisation.toFixed(2)}%
                    </td>

                    <td>
                      {item.pct_completed.toFixed(2)}%
                    </td>

                    <td>
                      <span
                        className={`badge ${item.risk_category.toLowerCase()}`}
                      >
                        {item.risk_category}
                      </span>
                    </td>

                    <td>
                      {(() => {
                        const investigation = investigations.find(
                          (inv) =>
                            inv.constituency === item.constituency &&
                            inv.year === item.year
                        );

                        return investigation ? (
                          <span className="investigation-status-badge">
                            {investigation.status}
                          </span>
                        ) : (
                          <span className="not-investigated">
                            Not Investigated
                          </span>
                        );
                      })()}
                    </td>

                  </tr>

                ))}

              </tbody>

            </table>

          </div>

        )}

      </section>
      {selectedCase && (
        <div className="investigation-overlay">

          <div className="investigation-panel">

            <button
              className="close-btn"
              onClick={() => setSelectedCase(null)}
            >
              ✕
            </button>

            <div className="investigation-header">

              <div>
                <p className="panel-label">
                  AI INVESTIGATION
                </p>

                <h2>
                  {selectedCase.constituency}
                </h2>

                <p>
                  Year {selectedCase.year}
                </p>
              </div>

              <span
                className={`badge ${selectedCase.risk_category.toLowerCase()}`}
              >
                {selectedCase.risk_category}
              </span>

            </div>


            {/* RISK SCORE */}

            <div className="risk-score-box">

              <p>AI Risk Score</p>

              <h1>
                {selectedCase.risk_score}
                <span>/100</span>
              </h1>

            </div>


            {/* METRICS */}

            <div className="investigation-metrics">

              <div>
                <span>Pending Works</span>
                <strong>
                  {selectedCase.pending_works.toLocaleString()}
                </strong>
              </div>

              <div>
                <span>Utilisation</span>
                <strong>
                  {selectedCase.pct_utilisation.toFixed(2)}%
                </strong>
              </div>

              <div>
                <span>Completion</span>
                <strong>
                  {selectedCase.pct_completed.toFixed(2)}%
                </strong>
              </div>

            </div>


            {/* AI REASONS */}

            <div className="reasons">

              <h3>
                Why AI Flagged This Case
              </h3>

              {selectedCase.reasons.map(
                (reason, index) => (

                  <div
                    className="reason"
                    key={index}
                  >
                    <span>⚠</span>

                    <p>{reason}</p>
                  </div>

                )
              )}

            </div>


            {/* ACTION */}
            {investigationStarted && (
              <div className="investigation-status">

                <div className="status-icon">
                  ✓
                </div>

                <div>
                  <strong>Investigation Started</strong>

                  <p>
                    Case has been assigned for officer review.
                  </p>
                </div>

              </div>
            )}
            {investigationStarted && (
              <div className="investigation-form">

                <label>Investigation Status</label>

                <select
                  value={investigationStatus}
                  onChange={(e) =>
                    setInvestigationStatus(e.target.value)
                  }
                >
                  <option>Under Review</option>
                  <option>Field Verification</option>
                  <option>Verified</option>
                  <option>Irregularity Found</option>
                  <option>False Positive</option>
                </select>


                <label>Officer Remarks</label>

                <textarea
                  value={officerRemarks}
                  onChange={(e) =>
                    setOfficerRemarks(e.target.value)
                  }
                  placeholder="Enter investigation remarks..."
                  rows="4"
                />


                <button
                  className="save-investigation"
                  onClick={saveInvestigation}
                >
                  Save Investigation
                </button>

              </div>
            )}

            <button
              className={`investigate-btn ${investigationStarted ? "started" : ""
                }`}
              onClick={() => setInvestigationStarted(true)}
            >
              {investigationStarted
                ? "✓ Investigation Started"
                : "Start Investigation"}
            </button>

          </div>

        </div>
      )}

    </div>
  );
}

export default App;