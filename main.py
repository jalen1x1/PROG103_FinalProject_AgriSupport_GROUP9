#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agriculture Support System for Sierra Leone Farmers
PROG103 Final Project – Principles of Structured Programming

This GUI application helps farmers estimate crop yield, fertilizer needs,
and profit margins based on farm size, crop type, and soil quality.
It supports multiple record entries, summary statistics, and CSV export.

SDG Alignment:
- SDG 2 (Zero Hunger): Improves crop planning and resource efficiency.
- SDG 8 (Decent Work & Economic Growth): Boosts farm profitability.

Open-source license: MIT
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import csv
from datetime import datetime

# ------------------------- CONSTANTS -------------------------
CROP_YIELD_BASE = {"Rice": 2.5, "Maize": 3.0, "Cassava": 10.0}        # tons per hectare
CROP_FERT_BASE = {"Rice": 4.0, "Maize": 3.0, "Cassava": 2.0}          # bags per hectare
SOIL_YIELD_FACTOR = {"Low": 0.7, "Medium": 1.0, "High": 1.3}
SOIL_FERT_FACTOR = {"Low": 1.2, "Medium": 1.0, "High": 0.8}
OTHER_COST_PER_HA = 100_000.0    # Leones (other operational costs)
PROFIT_THRESHOLD = 500_000.0     # Leones – minimum "good profit" level

# Global list to store all farm records
farm_records = []

# ------------------------- CORE LOGIC FUNCTIONS -------------------------
def calculate_yield_and_fertilizer(crop, area_ha, soil_quality):
    """
    Calculate estimated yield (kg) and required fertilizer bags.
    Uses structured decision (if-elif-else) and mathematical processing.
    """
    if crop not in CROP_YIELD_BASE:
        raise ValueError("Unsupported crop type")
    base_yield_tons = CROP_YIELD_BASE[crop]
    yield_factor = SOIL_YIELD_FACTOR.get(soil_quality, 1.0)
    estimated_yield_kg = area_ha * base_yield_tons * yield_factor * 1000.0   # convert to kg

    base_fert_bags = CROP_FERT_BASE[crop]
    fert_factor = SOIL_FERT_FACTOR.get(soil_quality, 1.0)
    fertilizer_bags = area_ha * base_fert_bags * fert_factor
    fertilizer_bags = round(fertilizer_bags, 1)   # realistic half-bag allowed

    return estimated_yield_kg, fertilizer_bags

def calculate_profit(yield_kg, fertilizer_bags, price_per_kg, cost_per_bag, area_ha):
    """
    Compute total revenue, total cost, and net profit.
    Includes decision structure for profit classification.
    """
    revenue = yield_kg * price_per_kg
    other_costs = area_ha * OTHER_COST_PER_HA
    total_cost = (fertilizer_bags * cost_per_bag) + other_costs
    net_profit = revenue - total_cost

    # Decision structure for profit level
    if net_profit < 0:
        profit_level = "LOSS – Review costs or improve yield"
    elif net_profit < PROFIT_THRESHOLD:
        profit_level = "Low profit – consider optimization"
    else:
        profit_level = " Good profit – sustainable operation"

    return revenue, total_cost, net_profit, profit_level

def add_record_to_storage(name, crop, area_ha, soil, fert_bags, yield_kg,
                          revenue, cost, net_profit, price_kg, cost_bag):
    """Add a validated farm record to the global list."""
    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "farmer_name": name,
        "crop": crop,
        "area_ha": area_ha,
        "soil_quality": soil,
        "fertilizer_bags": fert_bags,
        "yield_kg": yield_kg,
        "price_per_kg": price_kg,
        "cost_per_bag": cost_bag,
        "revenue_Le": revenue,
        "total_cost_Le": cost,
        "net_profit_Le": net_profit
    }
    farm_records.append(record)

# ------------------------- GUI APPLICATION -------------------------
class AgricultureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agriculture Support System – Sierra Leone")
        self.root.geometry("950x650")
        self.root.resizable(True, True)

        # Style
        style = ttk.Style()
        style.theme_use('clam')

        # ---------- Input Frame (Left side) ----------
        input_frame = ttk.LabelFrame(root, text="Farm Data Entry", padding=10)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Farmer Name
        ttk.Label(input_frame, text="Farmer Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = ttk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=5)

        # Crop Type
        ttk.Label(input_frame, text="Crop Type:").grid(row=1, column=0, sticky="w", pady=5)
        self.crop_var = tk.StringVar()
        crop_combo = ttk.Combobox(input_frame, textvariable=self.crop_var, values=list(CROP_YIELD_BASE.keys()), state="readonly")
        crop_combo.grid(row=1, column=1, pady=5)
        crop_combo.current(0)

        # Farm Area (hectares)
        ttk.Label(input_frame, text="Farm Area (hectares):").grid(row=2, column=0, sticky="w", pady=5)
        self.area_entry = ttk.Entry(input_frame, width=30)
        self.area_entry.grid(row=2, column=1, pady=5)

        # Soil Quality
        ttk.Label(input_frame, text="Soil Quality:").grid(row=3, column=0, sticky="w", pady=5)
        self.soil_var = tk.StringVar()
        soil_combo = ttk.Combobox(input_frame, textvariable=self.soil_var, values=["Low", "Medium", "High"], state="readonly")
        soil_combo.grid(row=3, column=1, pady=5)
        soil_combo.current(1)

        # Fertilizer Cost per Bag (Leones)
        ttk.Label(input_frame, text="Fertilizer Cost (Leones/bag):").grid(row=4, column=0, sticky="w", pady=5)
        self.fert_cost_entry = ttk.Entry(input_frame, width=30)
        self.fert_cost_entry.grid(row=4, column=1, pady=5)

        # Expected Price per kg (Leones)
        ttk.Label(input_frame, text="Expected Price (Leones/kg):").grid(row=5, column=0, sticky="w", pady=5)
        self.price_entry = ttk.Entry(input_frame, width=30)
        self.price_entry.grid(row=5, column=1, pady=5)

        # Buttons (Calculate, Add, Clear, Export, Exit)
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=15)

        self.calc_btn = ttk.Button(btn_frame, text="Calculate", command=self.calculate_current)
        self.calc_btn.grid(row=0, column=0, padx=5)

        self.add_btn = ttk.Button(btn_frame, text="Add Record", command=self.add_current_record)
        self.add_btn.grid(row=0, column=1, padx=5)

        self.clear_btn = ttk.Button(btn_frame, text="Clear Fields", command=self.clear_inputs)
        self.clear_btn.grid(row=0, column=2, padx=5)

        self.summary_btn = ttk.Button(btn_frame, text="Show Summary", command=self.show_summary)
        self.summary_btn.grid(row=0, column=3, padx=5)

        self.export_btn = ttk.Button(btn_frame, text="Export CSV", command=self.export_to_csv)
        self.export_btn.grid(row=0, column=4, padx=5)

        self.exit_btn = ttk.Button(btn_frame, text="Exit", command=self.root.destroy)
        self.exit_btn.grid(row=0, column=5, padx=5)

        # ---------- Output Area (Right side) ----------
        output_frame = ttk.LabelFrame(root, text="Results & System Output", padding=10)
        output_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.output_text = scrolledtext.ScrolledText(output_frame, width=55, height=28, font=("Consolas", 9))
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # Configure grid weights for resizing
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=2)
        root.rowconfigure(0, weight=1)

        # Initial message
        self.output_text.insert(tk.END, "=== Agriculture Support System (Sierra Leone) ===\n")
        self.output_text.insert(tk.END, "SDG 2: Zero Hunger | SDG 8: Economic Growth\n\n")
        self.output_text.insert(tk.END, "Enter farm details and click 'Calculate' to see projections.\n")
        self.output_text.insert(tk.END, "Use 'Add Record' to save each farm for summary.\n")

    # ---------- Helper: Validate GUI inputs ----------
    def validate_inputs(self):
        """Check that all required fields are valid; return (bool, error_msg)"""
        name = self.name_entry.get().strip()
        if not name:
            return False, "Farmer name is required."

        crop = self.crop_var.get()
        if crop not in CROP_YIELD_BASE:
            return False, "Select a valid crop."

        try:
            area = float(self.area_entry.get())
            if area <= 0:
                return False, "Farm area must be > 0 hectares."
        except ValueError:
            return False, "Farm area must be a positive number."

        soil = self.soil_var.get()
        if soil not in SOIL_YIELD_FACTOR:
            return False, "Select soil quality."

        try:
            fert_cost = float(self.fert_cost_entry.get())
            if fert_cost <= 0:
                return False, "Fertilizer cost must be > 0."
        except ValueError:
            return False, "Fertilizer cost must be a number."

        try:
            price_kg = float(self.price_entry.get())
            if price_kg <= 0:
                return False, "Expected price must be > 0."
        except ValueError:
            return False, "Expected price must be a number."

        return True, (name, crop, area, soil, fert_cost, price_kg)

    # ---------- Calculate and display current projection ----------
    def calculate_current(self):
        """Perform processing for current inputs (without saving to records)."""
        valid = self.validate_inputs()
        if not valid[0]:
            messagebox.showerror("Input Error", valid[1])
            return

        name, crop, area, soil, fert_cost, price_kg = valid[1]

        # Processing: yield & fertilizer
        try:
            yield_kg, fert_bags = calculate_yield_and_fertilizer(crop, area, soil)
            revenue, total_cost, net_profit, profit_level = calculate_profit(
                yield_kg, fert_bags, price_kg, fert_cost, area
            )
        except Exception as e:
            messagebox.showerror("Calculation Error", str(e))
            return

        # Display output
        self.output_text.insert(tk.END, "\n" + "="*60 + "\n")
        self.output_text.insert(tk.END, f"PROJECTION FOR: {name}\n")
        self.output_text.insert(tk.END, f"Crop: {crop} | Area: {area} ha | Soil: {soil}\n")
        self.output_text.insert(tk.END, f"Estimated yield: {yield_kg:,.0f} kg\n")
        self.output_text.insert(tk.END, f"Recommended fertilizer: {fert_bags} bags\n")
        self.output_text.insert(tk.END, f"Revenue: Le {revenue:,.2f}\n")
        self.output_text.insert(tk.END, f"Total cost: Le {total_cost:,.2f}\n")
        self.output_text.insert(tk.END, f"Net profit: Le {net_profit:,.2f}\n")
        self.output_text.insert(tk.END, f"Status: {profit_level}\n")
        self.output_text.insert(tk.END, "="*60 + "\n")
        self.output_text.see(tk.END)

        # Store current calculation data temporarily for "Add Record"
        self.last_calc = {
            "name": name, "crop": crop, "area": area, "soil": soil,
            "fert_bags": fert_bags, "yield_kg": yield_kg, "revenue": revenue,
            "total_cost": total_cost, "net_profit": net_profit,
            "price_kg": price_kg, "fert_cost": fert_cost
        }

    # ---------- Add current farm data to the records list ----------
    def add_current_record(self):
        """Saves the currently displayed/calculated record to global list."""
        if not hasattr(self, 'last_calc') or self.last_calc is None:
            messagebox.showwarning("No data", "Please click 'Calculate' first to generate a projection.")
            return

        # Use stored last_calc values
        lc = self.last_calc
        add_record_to_storage(
            lc["name"], lc["crop"], lc["area"], lc["soil"],
            lc["fert_bags"], lc["yield_kg"], lc["revenue"],
            lc["total_cost"], lc["net_profit"], lc["price_kg"], lc["fert_cost"]
        )
        self.output_text.insert(tk.END, f"\n Record for {lc['name']} added to summary.\n")
        self.output_text.see(tk.END)
        # Optionally reset last_calc to avoid double-add without recalc
        # but we keep it; user must recalc for new data

    # ---------- Show summary of all records (iteration + decision statistics) ----------
    def show_summary(self):
        """Display aggregated summary using loops and decision logic."""
        if not farm_records:
            self.output_text.insert(tk.END, "\n No records yet. Add some farm records first.\n")
            return

        total_farmers = len(farm_records)
        total_profit = sum(rec["net_profit_Le"] for rec in farm_records)
        avg_profit = total_profit / total_farmers if total_farmers else 0
        total_yield_kg = sum(rec["yield_kg"] for rec in farm_records)

        # Decision based on overall profitability
        if avg_profit < 0:
            region_status = " CRITICAL: Average loss – urgent intervention needed"
        elif avg_profit < PROFIT_THRESHOLD:
            region_status = "Moderate – profit improvement recommended"
        else:
            region_status = " Healthy – farmers are profitable"

        self.output_text.insert(tk.END, "\n" + ""*60 + "\n")
        self.output_text.insert(tk.END, " FARM RECORDS SUMMARY (Multiple entries)\n")
        self.output_text.insert(tk.END, f"Total farmers recorded: {total_farmers}\n")
        self.output_text.insert(tk.END, f"Total yield: {total_yield_kg:,.0f} kg\n")
        self.output_text.insert(tk.END, f"Total net profit: Le {total_profit:,.2f}\n")
        self.output_text.insert(tk.END, f"Average profit per farmer: Le {avg_profit:,.2f}\n")
        self.output_text.insert(tk.END, f"Regional status: {region_status}\n")
        self.output_text.insert(tk.END, "\n--- Individual Records ---\n")
        # Loop through each record (iteration)
        for idx, rec in enumerate(farm_records, 1):
            profit_class = "LOSS" if rec["net_profit_Le"] < 0 else "PROFIT"
            self.output_text.insert(tk.END,
                f"{idx}. {rec['farmer_name']} | {rec['crop']} | Area: {rec['area_ha']} ha | "
                f"Profit: Le {rec['net_profit_Le']:,.2f} ({profit_class})\n"
            )
        self.output_text.insert(tk.END, ""*60 + "\n")
        self.output_text.see(tk.END)

    # ---------- Export all records to CSV (interoperability) ----------
    def export_to_csv(self):
        if not farm_records:
            messagebox.showinfo("No Data", "No farm records to export.")
            return
        filename = f"farm_records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ["timestamp", "farmer_name", "crop", "area_ha", "soil_quality",
                              "fertilizer_bags", "yield_kg", "price_per_kg", "cost_per_bag",
                              "revenue_Le", "total_cost_Le", "net_profit_Le"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(farm_records)
            messagebox.showinfo("Export Successful", f"Data exported to {filename}")
            self.output_text.insert(tk.END, f"\n Exported {len(farm_records)} records to {filename}\n")
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not save CSV: {str(e)}")

    # ---------- Clear all input fields ----------
    def clear_inputs(self):
        self.name_entry.delete(0, tk.END)
        self.area_entry.delete(0, tk.END)
        self.fert_cost_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.crop_var.set("Rice")
        self.soil_var.set("Medium")
        if hasattr(self, 'last_calc'):
            self.last_calc = None
        # Optionally clear output area? We'll keep for reference, but user can manually clear.
        # Uncomment next line if output clearing desired:
        # self.output_text.delete(1.0, tk.END)

# ------------------------- MAIN EXECUTION -------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AgricultureApp(root)
    root.mainloop()