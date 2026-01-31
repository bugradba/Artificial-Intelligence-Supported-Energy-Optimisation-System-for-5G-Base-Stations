# ⚡ PIM Simulator for Energy-Efficient 5G Base Stations

> **Artificial Intelligence Supported Energy Optimisation System for 5G Base Stations**
> *Edge AI + Processing-in-Memory (PIM) for energy-aware baseband acceleration*

---

## 📌 Motivation

5G base stations operate **24/7** and are among the most energy-hungry components of modern mobile networks. Even a **5–10% energy saving** at scale translates into **millions of TL in operational cost reduction** and a **significant decrease in carbon footprint**.

With the growth of AI-driven services and high-throughput baseband processing, **energy efficiency at the edge of the network** has become critical. This project explores how **Processing-in-Memory (PIM)** and **precision-scalable computing (8-bit / 4-bit)** can be combined with **AI-driven decision mechanisms** to reduce energy consumption while keeping performance within acceptable limits.

> **System is designed to operate at the edge of the 5G network, close to base stations, where energy efficiency is critical.**

---

## 🏗️ Where This Fits in 5G Architecture

This simulator targets the **edge side of the 5G network**, where latency and energy constraints are the strictest:

```
           ┌───────────────────────────┐
           │        Core Network       │
           └─────────────┬─────────────┘
                         │
                 ┌───────▼────────┐
                 │   Near-RT RIC   │  (RAN Intelligent Controller)
                 └───────┬────────┘
                         │  Control / Optimization Decisions
           ┌─────────────▼─────────────┐
           │        Edge Cloud          │
           │  (AI Inference & Control)  │
           └─────────────┬─────────────┘
                         │
           ┌─────────────▼─────────────┐
           │ Baseband Processing Unit   │
           │ (PIM / GPU / CPU Compute)  │
           └───────────────────────────┘
```

In this context:

* **Near-RT RIC / Edge Cloud**: Makes intelligent decisions about *how* and *where* computations should run.
* **Baseband Processing Unit (BBU)**: Executes compute-intensive operations such as CNN layers, MAC operations, and signal processing kernels.
* **This project** simulates how **PIM clusters** with **precision scaling (8-bit vs 4-bit)** can reduce energy consumption in the BBU while maintaining acceptable performance.

---

## 🚀 Key Ideas

* **Processing-in-Memory (PIM)**: Reduce data movement by performing MAC operations inside or near memory.
* **Precision Scaling (8-bit / 4-bit)**: Trade numerical precision for **lower energy and latency**.
* **Cluster-Based PIM Architecture**: 8-bit MAC is decomposed into multiple 4-bit operations executed in parallel across a 3×3 (9-core) PIM cluster.
* **Energy & Latency Modeling**: Each operation reports:

  * Energy consumption
  * Latency
  * Effective power
* **5G-Oriented Workloads**: Includes CNN layer examples (e.g., AlexNet Conv1) representing baseband / edge AI workloads.

---

## 🧠 Why This Matters for Operators (e.g., Turkcell)

* 📡 **Base stations run 24/7** → even small efficiency gains matter
* 💰 **5–10% energy saving** → **millions of TL** in OPEX reduction at national scale
* 🌱 **Lower carbon footprint** → greener mobile networks
* 🤖 **Edge AI + PIM** → future-proof architecture for 5G-Advanced and 6G
* ⚡ **Less data movement, more compute near memory** → better performance per watt

This project demonstrates, at a simulator level, **how hardware-aware AI and PIM architectures can be used together** to move toward more sustainable mobile networks.

---

## 🧩 Project Structure

```
PIM SIMULATOR/
├── pim_core.py          # 4-bit MAC model, energy & latency per operation
├── pim_cluster.py       # 9-core PIM cluster, 8-bit & 4-bit precision MAC
├── cnn_layers.py        # CNN layer abstractions (e.g., Conv, ReLU, FC)
├── test_simulator.py    # End-to-end tests and benchmarks
└── ...
```

---

## ▶️ How to Run

```bash
python test_simulator.py
```

This will:

* Test a single PIM core
* Test a PIM cluster (8-bit vs 4-bit precision)
* Run a sample CNN layer workload
* Compare energy, latency, and power against a GPU baseline

---

## 📊 Example Results (From Simulator)

* **8-bit vs 4-bit PIM MAC**:

  * ~**77% energy saving** for 4-bit precision
  * ~**2× lower latency**
* **CNN Layer (AlexNet Conv1)**:

  * PIM shows significantly lower energy than GPU
  * Precision scaling further reduces energy with acceptable approximation

These results highlight the **energy–accuracy–latency trade-off** that is critical in edge and baseband processing.

---

## 🔮 Future Work

* Integrate a **learning-based scheduler (e.g., Q-Learning / RL)** to decide dynamically:

  * PIM vs GPU execution
  * 8-bit vs 4-bit precision
* Add **accuracy-aware cost functions** (Energy–Delay–Accuracy trade-off)
* Extend workload set to more **5G baseband and AI models**
* Calibrate the simulator with **real hardware measurements**

---

## 📚 References

* pPIM: *A Programmable Processor-in-Memory Architecture With Precision-Scaling for Deep Learning*
* 5G RAN Architecture (Near-RT RIC, Edge Cloud, BBU concepts)

---

## ✍️ Author

**Buğra Demirbaş**
Computer Engineering Student
Focus: 5G/6G Networks, Edge AI, Processing-in-Memory, Energy-Efficient Architectures

---

If you are interested in **energy-efficient edge computing for 5G and beyond**, this simulator provides a concrete and extensible starting point.
