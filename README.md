# 🚗 Agentic OEM Predictive Maintenance System
An **Agentic AI Multi-Agent System** built using **LangGraph, Groq LLM, and Streamlit** to simulate an intelligent OEM vehicle maintenance platform.

The system uses a **Supervisor Agent** to orchestrate multiple specialized AI agents that analyze vehicle telemetry data, predict maintenance risks, schedule service slots, and send notifications.

---

## 🧠 Architecture

The system follows a **Supervisor–Worker Multi-Agent Architecture**:

Supervisor Agent → Controls workflow execution

Worker Agents:
- 🔍 **Sensor Agent** → Processes vehicle sensor data
- 📊 **Data Agent** → Analyzes service history
- 🤖 **Prediction Agent** → Calculates failure risk
- 📅 **Scheduler Agent** → Recommends service slots
- 📩 **Notification Agent** → Generates maintenance alerts

Workflow:


User Input → Sensor Agent → Data Agent → Prediction Agent → Scheduler Agent → Notification Agent → Final Response


---

## ⚙️ Tech Stack

- **LangGraph** → Multi-agent workflow orchestration
- **LangChain** → LLM interaction framework
- **Groq LLM (Llama3)** → AI reasoning
- **Streamlit** → Chatbot UI
- **Python** → Core backend logic

---

## 🚀 Features

✔ Multi-Agent AI system  
✔ Supervisor-based agent orchestration  
✔ Predictive vehicle maintenance simulation  
✔ Vehicle telemetry analysis  
✔ Automated service scheduling  
✔ Notification generation  
✔ Interactive chatbot UI  

---

## 📂 Project Structure


agentic-oem-predictive-maintenance
│
├── backend.py # LangGraph multi-agent workflow
├── ui.py # Streamlit chatbot interface
├── requirements.txt # Python dependencies
└── README.md # Project documentation


---

## 🛠 Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/agentic-oem-predictive-maintenance.git
cd agentic-oem-predictive-maintenance

Create virtual environment:

python -m venv .venv

Activate environment:

Windows

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt
▶️ Run the Application
streamlit run ui.py

Then open the browser at:

http://localhost:8501
🔑 Environment Variables

Set your Groq API key:

GROQ_API_KEY=your_api_key_here
📊 Example Output

The system generates:

Vehicle risk score

Maintenance recommendation

Available service slots

Customer notification message

🌍 Real-World Use Case

Predictive maintenance helps automotive OEMs:

Reduce vehicle breakdowns

Optimize service center workload

Improve customer experience

Predict failures using sensor telemetry

👨‍💻 Author

Vedant Shukla
B.Tech Computer Science

⭐ Future Improvements

Real IoT sensor integration

Advanced ML failure prediction models

Vector database for vehicle history

Autonomous agent decision making

Fleet-level predictive analytics


---

# ⭐ Optional (Highly Recommended)

Add **GitHub Topics** to your repo:


agentic-ai
langgraph
multi-agent-system
predictive-maintenance
streamlit
llm
ai-agents





```markdown
![Python](https://img.shields.io/badge/Python-3.10-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-MultiAgent-green)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![LLM](https://img.shields.io/badge/LLM-Groq-orange)
