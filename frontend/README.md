# TIAA Data Pipeline Hackathon Frontend

This is the frontend for the TIAA-DataPipeline project, a hackathon entry demonstrating the use of AI agents to automate a data pipeline.

## Overview

The TIAA-DataPipeline project showcases a system where different AI agents collaborate to process data. Each agent is responsible for a specific stage of the pipeline:

1. **Ingestion:** Handles data intake.
2. **Cleaning:** Cleans and preprocesses the data.
3. **Transform:** Transforms the data into a suitable format.
4. **Checking:** Performs quality checks on the data.
5. **Report:** Generates reports from the processed data.
6. **Storage:** Stores the data.
7. **Metadata:** Manages metadata for the pipeline.

The backend contains all the AI logic, while this frontend provides a user-friendly interface to interact with the system.

## Features

* **File Upload:** Upload datasets to be processed by the data pipeline.
* **Interactive UI:** Interact with the AI agents and view the pipeline's progress.
* **Data Visualization:** View reports and visualizations generated from the processed data.

## Tech Stack

* **React:** A JavaScript library for building user interfaces.
* **Vite:** A fast build tool for modern web projects.
* **TypeScript:** A typed superset of JavaScript.
* **Tailwind CSS:** A utility-first CSS framework.
* **Recharts:** A composable charting library built on React components.

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

* Node.js (v18 or later)
* npm

### Installation

1. Clone the repo

   ```sh
   git clone https://github.com/spabolu/tiaa-data-pipeline.git
   ```

2. Navigate to the frontend directory

   ```sh
   cd tiaa-data-pipeline/frontend
   ```

3. Install NPM packages

   ```sh
   npm install
   ```

4. Run the development server

   ```sh
   npm run dev
   ```

The application will be available at `http://localhost:5173` (or another port if 5173 is in use).

## Project Structure

```bash
frontend/
├── public/             # Static assets
├── src/
│   ├── assets/         # Images and other assets
│   ├── components/     # Reusable React components
│   │   ├── ui/         # UI components from shadcn/ui
│   │   ├── Charts.tsx
│   │   ├── FileUpload.tsx
│   │   ├── Insights.tsx
│   │   ├── LLMOutput.tsx
│   │   └── Tracker.tsx
│   ├── lib/            # Utility functions
│   ├── App.tsx         # Main application component
│   ├── main.tsx        # Entry point of the application
│   └── index.css       # Global styles
├── .eslintrc.cjs       # ESLint configuration
├── package.json        # Project dependencies and scripts
├── tailwind.config.js  # Tailwind CSS configuration
└── vite.config.ts      # Vite configuration
```
