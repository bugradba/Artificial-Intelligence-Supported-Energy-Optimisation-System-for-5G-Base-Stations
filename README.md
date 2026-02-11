# 🌿 Green-Tensor-Core

**Sustainable Hybrid (CPU + PIM) Computing Architecture for Next-Gen AI Workloads**

> *"Moving the processor to the data, instead of moving data to the processor."*

[View Demo](#) • [Documentation](#) • [Report Bug](#)

---

## 🚀 Executive Summary

**Green-Tensor-Core** is a simulation framework for a **Hybrid Computing Architecture** designed to tackle one of the biggest challenges in modern computing: **Data Movement Energy Costs**.

In traditional Von Neumann architectures, up to **62.7% of total system energy** is wasted on moving data between **Memory (DRAM)** and the **Processor (CPU/GPU)**.  
This project proposes a sustainable solution by integrating **Processing-in-Memory (PIM)** accelerators with a host CPU.

By offloading heavy **vector-matrix operations** to the memory module and keeping control logic on the CPU, **Green-Tensor-Core** aims to drastically reduce the **carbon footprint** of:

- 5G/6G Networks  
- Green Data Centers  
- Autonomous Systems  
- Edge AI & IoT Devices  

---

## 🧠 System Architecture

The system follows a **heterogeneous computing model** with three main layers:

> 📌 *(Place your architecture diagram in `docs/architecture_diagram.png` and reference it here)*

### 1. Host CPU (Control Plane)

- **Role:** Manages OS, I/O requests, and light serial processing  
- **Logic:** Acts as the *"brain"* and decides which tasks should be offloaded  

### 2. PIM Accelerator (Data Plane)

- **Role:** Performs high-intensity parallel computations (e.g., Deep Learning Inference, FFT) directly inside memory  
- **Benefit:** Near-zero data movement cost for large datasets  

### 3. Intelligent Hybrid Scheduler ⚡

**Core Innovation:**  
A runtime scheduler that analyzes incoming tasks:

- If task is **Data-Intensive** (e.g., Matrix Multiplication) → Offload to **PIM**
- If task is **Control-Intensive** (e.g., Branching Logic) → Execute on **CPU**

---

## 🌍 Potential Use Cases

| Domain | Problem | Green-Tensor-Core Solution |
|--------|---------|----------------------------|
| 📡 5G & 6G Networks | Base stations consume massive power for signal processing | Reduces energy per bit via in-memory processing |
| ☁️ Green Data Centers | AI training (LLMs) causes high heat & carbon emissions | Lowers cooling cost and TDP |
| 🛸 Autonomous Systems | Limited battery for AI workloads | Extends flight time / driving range |
| 🔒 Edge AI & IoT | Cloud offloading is slow and risky | Enables secure, low-latency on-device AI |

---

## 📊 Simulation Results

Benchmarked against **CPU-only architectures** using synthetic workloads (ResNet-50-like matrix operations):

- ⚡ **Energy Savings:** ~**42%** reduction in total energy consumption  
- ⏱️ **Latency:** **1.8× speedup** for large batch workloads  
- 📉 **Bus Utilization:** **60% reduction** in memory bus traffic  

---

## 🛠️ Installation & Quick Start

### Prerequisites

- Python **3.8+**
- `pip`

### Steps

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/bugradba/Green-Tensor-Core.git
cd Green-Tensor-Core
pip install -r requirements.txt
python src/main.py --mode hybrid --workload large_matrix


Green-Tensor-Core/
├── PIM SIMULATOR/
│   ├── Q_Learning/                 # Q-Learning based scheduling utilities
│   │   ├── (Q_Learning içerikleri) # Q-learning scripts & helpers
│   │
│   ├── adaptive_scheduler.py       # Adaptive scheduler module
│   ├── baseline_models.py          # Baseline (CPU-only) models
│   ├── hybrid_scheduler.py         # Hybrid CPU + PIM scheduler logic
│   ├── pim_simulator.py            # Core processing-in-memory simulation engine
│   ├── adaptive_precision.py       # Precision/energy trade-off experiments
│   ├── test_simulator.py           # Simulation tests & benchmarks
│   └── visualize_scheduler.py      # Visualization tools for scheduler behavior
├── README.md                       # Project overview and docs
└── requirements.txt                # Python dependencies

```


##  System Architecture

The final hardware and software architecture of the project is built upon a heterogeneous computing framework. The system is controlled by a **Q-Learning-based Smart Hybrid Scheduler** that manages workload distribution between the **CPU** and **PIM (Processing-in-Memory)** units.

The architectural diagram below illustrates the details of this integration:

<p align="center">
  <img src="System Architecture.png" alt="Proposed Smart Hybrid Scheduler and PIM Architecture" width="800">
</p>

### ⚙️ Operational Logic
To overcome the **Memory Wall** bottleneck, the scheduler dynamically analyzes tasks (profiling) and routes them based on the following logic:

```math
IF (\text{data\_intensive}) \rightarrow \text{PIM (Processing-in-Memory)}
ELSE \rightarrow \text{CPU (Host Processor)}



###Contact & Acknowledgements

- **Developer: Muhammed Buğra Demirbaş
- **Context: Developed for Tomorrow's Technology Leaders (Sustainability Track).

- **LinkedIn: https://www.linkedin.com/in/m-bugra-demirbas/

- **Email: mbugrademirbas@gmail.com



