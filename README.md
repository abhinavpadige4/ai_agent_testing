# AI Agent to Test Websites Automatically Using Natural Language

---

## Milestone Number
**Milestone 1: Foundation Setup and Baseline Agent Implementation (Week 1–2)**

---

## Milestone Details
This milestone focuses on establishing the technical foundation required to build an AI-driven agent capable of testing websites using natural language instructions. The work completed in this phase ensures that the development environment, backend server, agent framework, and basic end-to-end communication pipeline are stable, testable, and extensible for future milestones.

---

## Detailed Explanation of Milestone Points

### 1. Python Environment Setup and Dependency Installation

A dedicated Python virtual environment is created to isolate project dependencies and ensure reproducibility across development machines. Core libraries installed during this phase include:

- **Flask** – Used to build a lightweight backend server for API handling and serving a test UI.
- **LangGraph** – Provides a graph-based framework for building stateful AI agents.
- **Playwright** – Installed in preparation for browser automation and website testing in later milestones.

This step guarantees that all contributors work with consistent library versions and prevents dependency conflicts.

---

### 2. Project Structure Definition

A clean and modular project structure is defined early to support scalability and maintainability. Responsibilities are clearly separated between backend logic, agent logic, static assets, and templates. This structure allows independent evolution of the AI agent, the API layer, and the user interface.

---

### 3. Flask Server Initialization with Static Test Page

A Flask server is initialized as the backend entry point for the system. During this milestone:

- A basic Flask application is created.
- A static HTML test page is served using Flask templates.
- REST endpoints are defined to accept user input via HTTP POST requests.

This setup enables quick manual testing through both the browser and API tools such as Postman, validating request–response flows before introducing complex logic.

---

### 4. Baseline LangGraph Agent Configuration

A baseline AI agent is implemented using LangGraph to validate agent execution and state handling. Key characteristics of this agent include:

- A clearly defined state schema (input and output).
- A single processing node that receives user input and generates a deterministic response.
- Graph compilation and invocation logic isolated from Flask.

At this stage, the agent does not use an LLM. Its purpose is to confirm that the agent framework is correctly wired and can be reliably invoked by the backend.

---

### 5. Flask–Agent Integration (End-to-End Flow)

The Flask backend is connected to the LangGraph agent to complete the full interaction pipeline:

1. User enters a natural language instruction in the UI.
2. The browser sends a POST request to the Flask `/chat` endpoint.
3. Flask forwards the input to the LangGraph agent.
4. The agent processes the input and returns a response.
5. Flask sends the response back to the UI as JSON.

This confirms that the system supports real-time interaction between the user interface and the AI agent.



---

## Milestone Outcome

By completing Milestone 1, the project achieves:

- A stable Python and Flask development environment  
- A working backend server  
- A validated LangGraph agent framework  
- End-to-end communication between UI, backend, and agent  
- A solid foundation for adding LLM reasoning and automated website testing  

This milestone serves as the technical baseline upon which all future AI-driven testing capabilities will be built.

---
## Milestone Number
**Milestone 2: Foundation Setup and Baseline Agent Implementation (Week 2–4)**

**Prepared by:** ABHINAV PADIGE
