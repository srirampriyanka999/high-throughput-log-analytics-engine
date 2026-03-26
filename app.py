# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import json
# import time

# st.set_page_config(page_title="Log Analytics Engine", layout="wide", page_icon="🔍")

# st.title("🔍 Log Analytics & Monitoring Engine")
# st.markdown("Real-time log monitoring and anomaly detection dashboard")

# mode = st.sidebar.selectbox("Select Mode", ["History", "Live"])

# # ─────────────────────────────────────────────
# # HISTORY MODE
# # ─────────────────────────────────────────────
# if mode == "History":
#     st.subheader("📂 Historical Log Analysis")

#     try:
#         with open("output_logs.json", "r") as f:
#             logs = json.load(f)
#     except:
#         st.error("output_logs.json not found! Run main.py first.")
#         st.stop()

#     from pipeline.anomaly.detector import detect_zscore

#     df = pd.DataFrame(logs)
#     anomalies = detect_zscore(logs)
#     anomaly_df = pd.DataFrame(anomalies) if anomalies else pd.DataFrame()

#     # ── Summary Cards ──
#     st.markdown("### 📊 Overview")
#     col1, col2, col3, col4, col5 = st.columns(5)
#     col1.metric("📋 Total Logs", len(df))
#     col2.metric("🚨 Anomalies", len(anomaly_df))
#     col3.metric("🏢 Services", df["Service Name"].nunique())
#     col4.metric("❌ Errors", len(df[df["Level"] == "ERROR"]))
#     col5.metric("💀 Criticals", len(df[df["Level"] == "CRITICAL"]))

#     st.divider()

#     # ── Row 1: Log Level Distribution + Service Distribution ──
#     st.markdown("### 📈 Log Distribution")
#     col1, col2 = st.columns(2)

#     with col1:
#         st.subheader("Log Level Distribution")
#         fig = px.pie(df, names="Level", hole=0.4,
#                      color="Level",
#                      color_discrete_map={
#                          "INFO": "#00CC96",
#                          "WARNING": "#FFA15A",
#                          "ERROR": "#EF553B",
#                          "CRITICAL": "#AB63FA"
#                      })
#         st.plotly_chart(fig, use_container_width=True)

#     with col2:
#         st.subheader("Logs per Service")
#         service_counts = df["Service Name"].value_counts().reset_index()
#         fig = px.bar(service_counts, x="Service Name", y="count",
#                      color="Service Name")
#         st.plotly_chart(fig, use_container_width=True)

#     st.divider()

#     # ── Row 2: Status Code Distribution + Log Level per Service ──
#     st.markdown("### 🔢 Status Code & Service Analysis")
#     col1, col2 = st.columns(2)

#     with col1:
#         st.subheader("Status Code Distribution")
#         fig = px.histogram(df, x="Status_code", nbins=20,
#                            color_discrete_sequence=["#636EFA"])
#         st.plotly_chart(fig, use_container_width=True)

#     with col2:
#         st.subheader("Log Level per Service")
#         fig = px.histogram(df, x="Service Name", color="Level",
#                            barmode="group",
#                            color_discrete_map={
#                                "INFO": "#00CC96",
#                                "WARNING": "#FFA15A",
#                                "ERROR": "#EF553B",
#                                "CRITICAL": "#AB63FA"
#                            })
#         st.plotly_chart(fig, use_container_width=True)

#     st.divider()

#     # ── Row 3: Anomaly Visualizations ──
#     st.markdown("### 🚨 Anomaly Analysis")

#     if not anomaly_df.empty:
#         col1, col2 = st.columns(2)

#         with col1:
#             st.subheader("Anomalies per Service")
#             fig = px.bar(anomaly_df["Service Name"].value_counts().reset_index(),
#                          x="Service Name", y="count", color="Service Name")
#             st.plotly_chart(fig, use_container_width=True)

#         with col2:
#             st.subheader("Anomalies by Level")
#             fig = px.bar(anomaly_df["Level"].value_counts().reset_index(),
#                          x="Level", y="count", color="Level",
#                          color_discrete_map={
#                              "ERROR": "#EF553B",
#                              "CRITICAL": "#AB63FA"
#                          })
#             st.plotly_chart(fig, use_container_width=True)

#         # ── Z-score scatter plot ──
#         st.subheader("Z-Score Distribution of Anomalies")
#         fig = px.scatter(anomaly_df, x="timestamp", y="zscore",
#                          color="Service Name", size="Status_code",
#                          hover_data=["Level", "message"],
#                          title="Anomaly Z-Scores over Time")
#         st.plotly_chart(fig, use_container_width=True)

#     else:
#         st.success("No anomalies detected in historical logs!")

#     st.divider()

#     # ── Full Log Table with Filters ──
#     st.markdown("### 📋 Full Log Table")
#     col1, col2 = st.columns(2)
#     with col1:
#         level_filter = st.multiselect("Filter by Level",
#                                       options=df["Level"].unique(),
#                                       default=df["Level"].unique())
#     with col2:
#         service_filter = st.multiselect("Filter by Service",
#                                         options=df["Service Name"].unique(),
#                                         default=df["Service Name"].unique())

#     filtered_df = df[df["Level"].isin(level_filter) &
#                      df["Service Name"].isin(service_filter)]
#     st.dataframe(filtered_df, use_container_width=True)

#     # ── Anomaly Table ──
#     if not anomaly_df.empty:
#         st.markdown("### 🚨 Detected Anomalies Table")
#         st.dataframe(anomaly_df, use_container_width=True)

# # ─────────────────────────────────────────────
# # LIVE MODE
# # ─────────────────────────────────────────────
# elif mode == "Live":
#     st.subheader("⚡ Live Log Monitoring")
#     st.info("Run `python main.py` in a separate terminal to start streaming!")

#     # load anomalies from file
#     try:
#         with open("anomalies.json", "r") as f:
#             all_anomalies = json.load(f)
#     except:
#         all_anomalies = []

#     # ── Summary Cards ──
#     st.markdown("### 📊 Live Overview")
#     col1, col2, col3 = st.columns(3)
#     col1.metric("🚨 Total Anomalies", len(all_anomalies))
#     col2.metric("🏢 Services Affected",
#                 len(set(a["Service Name"] for a in all_anomalies)) if all_anomalies else 0)
#     col3.metric("💀 Critical Count",
#                 len([a for a in all_anomalies if a["Level"] == "CRITICAL"]) if all_anomalies else 0)

#     st.divider()

#     if all_anomalies:
#         anomaly_df = pd.DataFrame(all_anomalies)

#         # ── Charts ──
#         st.markdown("### 📈 Live Anomaly Charts")
#         col1, col2 = st.columns(2)

#         with col1:
#             fig = px.bar(anomaly_df["Service Name"].value_counts().reset_index(),
#                          x="Service Name", y="count", color="Service Name",
#                          title="🚨 Anomalies per Service")
#             st.plotly_chart(fig, use_container_width=True)

#         with col2:
#             fig = px.bar(anomaly_df["Level"].value_counts().reset_index(),
#                          x="Level", y="count", color="Level",
#                          color_discrete_map={
#                              "ERROR": "#EF553B",
#                              "CRITICAL": "#AB63FA"},
#                          title="🚨 Anomalies by Level")
#             st.plotly_chart(fig, use_container_width=True)

#         # ── Z-score timeline ──
#         st.subheader("Z-Score Timeline (Live)")
#         fig = px.scatter(anomaly_df, x="timestamp", y="zscore",
#                          color="Service Name", size="Status_code",
#                          hover_data=["Level", "message"])
#         st.plotly_chart(fig, use_container_width=True)

#         # ── Pie chart ──
#         st.subheader("Anomaly Level Distribution")
#         fig = px.pie(anomaly_df, names="Level", hole=0.4,
#                      color="Level",
#                      color_discrete_map={
#                          "ERROR": "#EF553B",
#                          "CRITICAL": "#AB63FA"
#                      })
#         st.plotly_chart(fig, use_container_width=True)

#         # ── Latest anomalies table ──
#         st.subheader("Latest 20 Anomalies")
#         st.dataframe(anomaly_df.tail(20), use_container_width=True)

#     else:
#         st.warning("No anomalies detected yet! Make sure main.py is running.")

#     # auto refresh every 5 seconds
#     time.sleep(5)
#     st.rerun()


# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import json
# import time
# from datetime import datetime

# st.set_page_config(page_title="Log Analytics Engine", layout="wide", page_icon="🔍")

# # ── Header ──
# st.title("🔍 Log Analytics & Monitoring Engine")
# st.markdown("Real-time system health monitoring dashboard")
# st.divider()

# # ── Load Data ──
# try:
#     with open("anomalies.json", "r") as f:
#         all_anomalies = json.load(f)
# except:
#     all_anomalies = []

# try:
#     with open("output_logs.json", "r") as f:
#         all_logs = json.load(f)
# except:
#     all_logs = []

# df_logs = pd.DataFrame(all_logs) if all_logs else pd.DataFrame()
# df_anomalies = pd.DataFrame(all_anomalies) if all_anomalies else pd.DataFrame()

# # ── Sidebar Filters ──
# st.sidebar.title("🔧 Filters")
# st.sidebar.markdown("Drill down into specific issues")

# selected_services = st.sidebar.multiselect(
#     "Filter by Service",
#     options=df_anomalies["Service Name"].unique().tolist() if not df_anomalies.empty else [],
#     default=df_anomalies["Service Name"].unique().tolist() if not df_anomalies.empty else []
# )

# selected_levels = st.sidebar.multiselect(
#     "Filter by Level",
#     options=df_anomalies["Level"].unique().tolist() if not df_anomalies.empty else [],
#     default=df_anomalies["Level"].unique().tolist() if not df_anomalies.empty else []
# )

# # apply filters
# if not df_anomalies.empty:
#     filtered_anomalies = df_anomalies[
#         df_anomalies["Service Name"].isin(selected_services) &
#         df_anomalies["Level"].isin(selected_levels)
#     ]
# else:
#     filtered_anomalies = pd.DataFrame()

# # ── System Health Banner ──
# st.markdown("### 🏥 System Health Status")

# if not filtered_anomalies.empty:
#     critical_count = len(filtered_anomalies[filtered_anomalies["Level"] == "CRITICAL"])
#     error_count = len(filtered_anomalies[filtered_anomalies["Level"] == "ERROR"])
    
#     if critical_count > 0:
#         st.error(f"🚨 CRITICAL ALERT — {critical_count} critical issues detected! Immediate action required!")
#     elif error_count > 0:
#         st.warning(f"⚠️ WARNING — {error_count} errors detected! Investigation needed!")
#     else:
#         st.success("✅ System is healthy — No major anomalies detected!")
# else:
#     st.success("✅ System is healthy — No anomalies detected!")

# st.divider()

# # ── Summary Cards ──
# st.markdown("### 📊 Live Overview")
# col1, col2, col3, col4, col5 = st.columns(5)

# col1.metric(
#     "📋 Total Logs Processed",
#     len(df_logs) if not df_logs.empty else 0
# )
# col2.metric(
#     "🚨 Total Anomalies",
#     len(filtered_anomalies)
# )
# col3.metric(
#     "💀 Critical Issues",
#     len(filtered_anomalies[filtered_anomalies["Level"] == "CRITICAL"]) if not filtered_anomalies.empty else 0
# )
# col4.metric(
#     "❌ Errors",
#     len(filtered_anomalies[filtered_anomalies["Level"] == "ERROR"]) if not filtered_anomalies.empty else 0
# )
# col5.metric(
#     "🏢 Affected Services",
#     filtered_anomalies["Service Name"].nunique() if not filtered_anomalies.empty else 0
# )

# st.divider()

# if not filtered_anomalies.empty:

#     # ── Row 1: Which service is failing + How severe ──
#     st.markdown("### 🔥 What Is Failing?")
#     col1, col2 = st.columns(2)

#     with col1:
#         st.subheader("Anomalies per Service")
#         service_counts = filtered_anomalies["Service Name"].value_counts().reset_index()
#         service_counts.columns = ["Service Name", "Anomaly Count"]
#         fig = px.bar(service_counts,
#                      x="Service Name", y="Anomaly Count",
#                      color="Service Name",
#                      title="Which service has the most issues?")
#         st.plotly_chart(fig, use_container_width=True)

#     with col2:
#         st.subheader("Issue Severity Breakdown")
#         level_counts = filtered_anomalies["Level"].value_counts().reset_index()
#         level_counts.columns = ["Level", "Count"]
#         fig = px.pie(level_counts,
#                      names="Level", values="Count",
#                      hole=0.4,
#                      color="Level",
#                      color_discrete_map={
#                          "ERROR": "#EF553B",
#                          "CRITICAL": "#AB63FA"
#                      },
#                      title="How severe are the issues?")
#         st.plotly_chart(fig, use_container_width=True)

#     st.divider()

#     # ── Row 2: When did it happen + Which service per level ──
#     st.markdown("### ⏰ When Did It Happen?")
#     col1, col2 = st.columns(2)

#     with col1:
#         st.subheader("Anomaly Timeline")
#         timeline_df = filtered_anomalies.copy()
#         timeline_df["timestamp"] = pd.to_datetime(timeline_df["timestamp"])
#         timeline_df = timeline_df.sort_values("timestamp")
#         fig = px.scatter(timeline_df,
#                          x="timestamp", y="Service Name",
#                          color="Level",
#                          symbol="Level",
#                          size="Status_code",
#                          hover_data=["message", "Status_code"],
#                          color_discrete_map={
#                              "ERROR": "#EF553B",
#                              "CRITICAL": "#AB63FA"
#                          },
#                          title="Timeline of anomalies by service")
#         st.plotly_chart(fig, use_container_width=True)

#     with col2:
#         st.subheader("Error vs Critical per Service")
#         fig = px.histogram(filtered_anomalies,
#                            x="Service Name",
#                            color="Level",
#                            barmode="group",
#                            color_discrete_map={
#                                "ERROR": "#EF553B",
#                                "CRITICAL": "#AB63FA"
#                            },
#                            title="Which service has errors vs criticals?")
#         st.plotly_chart(fig, use_container_width=True)

#     st.divider()

#     # ── Row 3: Status code analysis ──
#     st.markdown("### 🔢 Status Code Analysis")
#     col1, col2 = st.columns(2)

#     with col1:
#         st.subheader("Status Code Distribution")
#         fig = px.histogram(filtered_anomalies,
#                            x="Status_code",
#                            color="Service Name",
#                            nbins=20,
#                            title="What status codes are being thrown?")
#         st.plotly_chart(fig, use_container_width=True)

#     with col2:
#         st.subheader("Average Status Code per Service")
#         avg_status = filtered_anomalies.groupby("Service Name")["Status_code"].mean().reset_index()
#         avg_status.columns = ["Service Name", "Avg Status Code"]
#         fig = px.bar(avg_status,
#                      x="Service Name", y="Avg Status Code",
#                      color="Service Name",
#                      title="Which service has highest avg status code?")
#         st.plotly_chart(fig, use_container_width=True)

#     st.divider()

#     # ── Decision Support Table ──
#     st.markdown("### 🎯 Action Required — Latest Anomalies")
#     st.markdown("*These are the most recent issues that need immediate attention:*")
    
#     display_df = filtered_anomalies[["timestamp", "Service Name", "Level", "Status_code", "message"]].tail(20)
#     display_df = display_df.sort_values("timestamp", ascending=False)
    
#     st.dataframe(
#         display_df.style.applymap(
#             lambda x: "background-color: #ffcccc" if x == "CRITICAL" else (
#                       "background-color: #ffe0cc" if x == "ERROR" else ""),
#             subset=["Level"]
#         ),
#         use_container_width=True
#     )

# else:
#     st.info("⏳ Waiting for anomalies... Make sure main.py is running in another terminal!")

# # ── Footer ──
# st.divider()
# st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} — Auto-refreshing every 5 seconds*")

# # ── Auto Refresh ──
# time.sleep(5)
# st.rerun()



import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import pandas as pd
import plotly.express as px
import json
import time
from datetime import datetime

# -------------------- Config --------------------
st.set_page_config(page_title="Log Analytics Engine", layout="wide")

PRIMARY_COLOR = "#636EFA"
ERROR_COLOR = "#EF553B"
BG_COLOR = "#0E1117"
TEXT_COLOR = "#EAEAEA"

# -------------------- Styling --------------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
h1, h2, h3 {
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# -------------------- Title --------------------
st.title("Log Analytics and Monitoring Engine")
st.caption("Real-time monitoring of system logs and anomalies")
st.divider()

# -------------------- Load Data --------------------
try:
    with open("anomalies.json", "r") as f:
        all_anomalies = json.load(f)
except:
    all_anomalies = []

try:
    with open("output_logs.json", "r") as f:
        all_logs = json.load(f)
except:
    all_logs = []

df_logs = pd.DataFrame(all_logs) if all_logs else pd.DataFrame()
df_anomalies = pd.DataFrame(all_anomalies) if all_anomalies else pd.DataFrame()

# -------------------- Sidebar --------------------
st.sidebar.title("Filters")

selected_services = st.sidebar.multiselect(
    "Service Name",
    options=df_anomalies["Service Name"].unique().tolist() if not df_anomalies.empty else [],
    default=df_anomalies["Service Name"].unique().tolist() if not df_anomalies.empty else []
)

selected_levels = st.sidebar.multiselect(
    "Log Level",
    options=df_anomalies["Level"].unique().tolist() if not df_anomalies.empty else [],
    default=df_anomalies["Level"].unique().tolist() if not df_anomalies.empty else []
)

# Apply filters
if not df_anomalies.empty:
    filtered_anomalies = df_anomalies[
        df_anomalies["Service Name"].isin(selected_services) &
        df_anomalies["Level"].isin(selected_levels)
    ]
else:
    filtered_anomalies = pd.DataFrame()

# -------------------- System Status --------------------
st.markdown("## System Health Status")

if not filtered_anomalies.empty:
    critical_count = len(filtered_anomalies[filtered_anomalies["Level"] == "CRITICAL"])
    error_count = len(filtered_anomalies[filtered_anomalies["Level"] == "ERROR"])

    if critical_count > 0:
        st.error(f"Critical issues detected: {critical_count}")
    elif error_count > 0:
        st.warning(f"Errors detected: {error_count}")
    else:
        st.success("System is operating normally")
else:
    st.success("No anomalies detected")

st.divider()

# -------------------- Metrics --------------------
st.markdown("## Overview")
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Logs", f"{len(df_logs):,}")
col2.metric("Total Anomalies", f"{len(filtered_anomalies):,}")
col3.metric("Critical Issues", f"{len(filtered_anomalies[filtered_anomalies['Level'] == 'CRITICAL']) if not filtered_anomalies.empty else 0}")
col4.metric("Errors", f"{len(filtered_anomalies[filtered_anomalies['Level'] == 'ERROR']) if not filtered_anomalies.empty else 0}")
col5.metric("Affected Services", f"{filtered_anomalies['Service Name'].nunique() if not filtered_anomalies.empty else 0}")

st.divider()

if not filtered_anomalies.empty:

    # -------------------- Service Analysis --------------------
    st.markdown("## Service Analysis")
    st.caption("Distribution of anomalies across services")

    col1, col2 = st.columns(2)

    with col1:
        service_counts = filtered_anomalies["Service Name"].value_counts().reset_index()
        service_counts.columns = ["Service Name", "Anomaly Count"]

        fig = px.bar(
            service_counts,
            x="Service Name",
            y="Anomaly Count",
            color="Service Name"
        )

        fig.update_layout(
            plot_bgcolor=BG_COLOR,
            paper_bgcolor=BG_COLOR,
            font=dict(color=TEXT_COLOR),
            title="Anomalies by Service"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        level_counts = filtered_anomalies["Level"].value_counts().reset_index()
        level_counts.columns = ["Level", "Count"]

        fig = px.pie(
            level_counts,
            names="Level",
            values="Count",
            color="Level",
            color_discrete_map={
                "ERROR": ERROR_COLOR,
                "CRITICAL": PRIMARY_COLOR
            }
        )

        fig.update_layout(
            plot_bgcolor=BG_COLOR,
            paper_bgcolor=BG_COLOR,
            font=dict(color=TEXT_COLOR),
            title="Severity Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # -------------------- Timeline --------------------
    st.markdown("## Timeline Analysis")

    col1, col2 = st.columns(2)

    with col1:
        timeline_df = filtered_anomalies.copy()
        timeline_df["timestamp"] = pd.to_datetime(timeline_df["timestamp"])
        timeline_df = timeline_df.sort_values("timestamp")

        fig = px.scatter(
            timeline_df,
            x="timestamp",
            y="Service Name",
            color="Level",
            size="Status_code",
            hover_data=["message"],
            color_discrete_map={
                "ERROR": ERROR_COLOR,
                "CRITICAL": PRIMARY_COLOR
            }
        )

        fig.update_layout(
            plot_bgcolor=BG_COLOR,
            paper_bgcolor=BG_COLOR,
            font=dict(color=TEXT_COLOR),
            title="Timeline of Anomalies"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.histogram(
            filtered_anomalies,
            x="Service Name",
            color="Level",
            barmode="group",
            color_discrete_map={
                "ERROR": ERROR_COLOR,
                "CRITICAL": PRIMARY_COLOR
            }
        )

        fig.update_layout(
            plot_bgcolor=BG_COLOR,
            paper_bgcolor=BG_COLOR,
            font=dict(color=TEXT_COLOR),
            title="Error vs Critical Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # -------------------- Status Code Analysis --------------------
    st.markdown("## Status Code Analysis")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(
            filtered_anomalies,
            x="Status_code",
            color="Service Name",
            nbins=20
        )

        fig.update_layout(
            plot_bgcolor=BG_COLOR,
            paper_bgcolor=BG_COLOR,
            font=dict(color=TEXT_COLOR),
            title="Status Code Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        avg_status = filtered_anomalies.groupby("Service Name")["Status_code"].mean().reset_index()
        avg_status.columns = ["Service Name", "Average Status Code"]

        fig = px.bar(
            avg_status,
            x="Service Name",
            y="Average Status Code",
            color="Service Name"
        )

        fig.update_layout(
            plot_bgcolor=BG_COLOR,
            paper_bgcolor=BG_COLOR,
            font=dict(color=TEXT_COLOR),
            title="Average Status Code per Service"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # -------------------- Recent Anomalies --------------------
    st.markdown("## Recent Anomalies")

    display_df = filtered_anomalies[
        ["timestamp", "Service Name", "Level", "Status_code", "message"]
    ].sort_values("timestamp", ascending=False).head(20)

    st.dataframe(display_df, use_container_width=True, height=350)

else:
    st.info("No anomaly data available. Ensure the data pipeline is running.")

# -------------------- Footer --------------------
st.divider()
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# -------------------- Auto Refresh --------------------
time.sleep(5)
st.rerun()