# 🌾 Agriculture Support System – Sierra Leone

**PROG103 Final Project**  
*Principles of Structured Programming*  
Faculty of Information and Communication Technology

---

## 📌 Table of Contents

- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [SDG Alignment](#sdg-alignment)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation & Setup](#installation--setup)
- [How to Use the Application](#how-to-use-the-application)
- [Program Structure (Structured Programming)](#program-structure-structured-programming)
- [File Structure](#file-structure)
- [GitHub Commands Used](#github-commands-used)
- [Screenshots](#screenshots)
- [Open Source License](#open-source-license)
- [Data Privacy & Compliance](#data-privacy--compliance)
- [Future Improvements](#future-improvements)
- [Authors](#authors)
- [Acknowledgments](#acknowledgments)

---

## Project Overview

The **Agriculture Support System** is a desktop GUI application built with Python and Tkinter. It helps smallholder farmers in **Sierra Leone** estimate crop yield, calculate required fertilizer, and predict profit margins based on farm size, crop type, and soil quality. The system supports multiple farm records, summary statistics, and CSV export for further analysis.

This project is submitted as the **Final Project** for the *Principles of Structured Programming* course, demonstrating:

- GUI programming (Tkinter)
- Modular program structure
- Decision structures (`if-elif-else`)
- Iteration (loops)
- Multiple user-defined functions
- Data validation
- File export (interoperability)

---

## Problem Statement

In rural Sierra Leone, many smallholder farmers lack access to simple digital tools that can help them:

- Estimate how much harvest they will get from their land.
- Know exactly how many bags of fertilizer to buy (to avoid waste or shortage).
- Calculate whether they will make a profit at current market prices.
- Keep written or digital records of multiple farms.

Without such tools, farmers often **over‑spend on fertilizer** or **under‑estimate yields**, leading to food waste, financial loss, and reduced economic growth. This application provides a **free, easy‑to‑use, offline solution** tailored to local crops (rice, maize, cassava) and local currency (Leones).

---

## SDG Alignment

| Sustainable Development Goal | How This Project Contributes |
|------------------------------|------------------------------|
| **SDG 2 – Zero Hunger** | Helps farmers optimize crop yield and fertilizer use, increasing food production per hectare. |
| **SDG 8 – Decent Work & Economic Growth** | Enables profit calculation and record keeping, supporting better financial planning and economic stability for farming families. |

The system also promotes **open-source practices** (GitHub, MIT license) and **data interoperability** (CSV export), aligning with SDG 9 (Industry, Innovation, and Infrastructure).

---

## Features

- ✅ **Graphical User Interface** (Tkinter) – no terminal needed.
- ✅ **Input Module** – farmer name, crop type, farm area (hectares), soil quality, fertilizer cost, expected price per kg.
- ✅ **Processing Module** – calculates yield, fertilizer bags, revenue, total cost, net profit.
- ✅ **Output Module** – displays formatted results with profit status.
- ✅ **Multiple Record Handling** – save many farm records in memory.
- ✅ **Summary Statistics** – total yield, total profit, average profit, regional status, individual record list.
- ✅ **CSV Export** – export all records to a timestamped CSV file (opens in Excel).
- ✅ **Data Validation** – prevents negative numbers, empty names, invalid crops.
- ✅ **Three+ User Functions** – `calculate_yield_and_fertilizer()`, `calculate_profit()`, `add_record_to_storage()`.
- ✅ **Structured Programming** – constants, variables, decisions, loops, modular design.
- ✅ **Open Source Ready** – MIT license, GitHub repository, README documentation.

---

## Technologies Used

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| GUI Library | Tkinter (built‑in) |
| CSV Export | Python `csv` module |
| Date/Time | Python `datetime` |
| Version Control | Git & GitHub |
| License | MIT |

No external libraries are required – runs with standard Python installation.

---

## Installation & Setup

### Prerequisites
- Python 3.10 or higher installed on your computer.
- Git (optional, for cloning the repository).

### Steps

1. **Clone the repository** (or download the `.py` file):
   ```bash
   git clone https://github.com/jalen1x1/PROG103_FinalProject_AgriSupport.git
   cd PROG103_FinalProject_AgriSupport

## Screenshots
- Farm Data Entry
  <img width="508" height="502" alt="Screenshot 2026-06-13 192113" src="https://github.com/user-attachments/assets/79a13f3a-71b8-4fac-928b-cfc655e47702" />

- Result & System Output
  <img width="435" height="478" alt="Screenshot 2026-06-13 192146" src="https://github.com/user-attachments/assets/74a86e30-51c1-4f62-92c2-706f32eb6536" />

