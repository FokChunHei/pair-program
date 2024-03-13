import tkinter as tk
from tkinter import messagebox


BASIC_ALLOWANCE = 132000
MARRIED_ALLOWANCE = 264000
CHILD_ALLOWANCE = 120000


MPF_PERCENTAGE = 0.05
MPF_ANNUAL_CAP = 18000


RV_RATES = {
    "Residential": 0.10,
    "2 Rooms": 0.08,
    "1 Room": 0.04
}


TAX_BRACKETS = [
    (50000, 0.02),
    (50000, 0.06),
    (50000, 0.10),
    (50000, 0.14),
    (float('inf'), 0.17)
]


TAX_REDUCTION_CAP = 6000

def calculate_mpf_contribution(income, is_in_scheme):
    if is_in_scheme:
        return MPF_ANNUAL_CAP
    else:
        return min(income * MPF_PERCENTAGE, MPF_ANNUAL_CAP)

def calculate_tax(net_chargeable_income):
    tax = 0
    for bracket in TAX_BRACKETS:
        bracket_income = min(net_chargeable_income, bracket[0])
        tax += bracket_income * bracket[1]
        net_chargeable_income -= bracket_income
        if net_chargeable_income <= 0:
            break
    return tax

def format_currency(value):
    return "${:,.0f}".format(value)

def recommend_assessment(separate_tax, joint_tax):
    if separate_tax < joint_tax:
        return "Separate Taxation is recommended."
    elif separate_tax > joint_tax:
        return "Joint Assessment is recommended."
    else:
        return "Both assessments result in the same tax liability."

def show_results():
    try:
        income_mr = float(self_income_entry.get())
        income_mrs = float(spouse_income_entry.get())
        rent = float(rent_entry.get())
        child_count = int(children_entry.get())
        accommodation_type = accomm_var.get()
        is_mr_in_mpf_scheme = mr_mpf_var.get()
        is_mrs_in_mpf_scheme = mrs_mpf_var.get()


        mpf_mr = calculate_mpf_contribution(income_mr, is_mr_in_mpf_scheme)
        mpf_mrs = calculate_mpf_contribution(income_mrs, is_mrs_in_mpf_scheme)


        rv_mr = (income_mr - rent) * RV_RATES[accommodation_type]
        rv_mrs = (income_mrs - rent) * RV_RATES[accommodation_type]


        taxable_income_mr = income_mr - mpf_mr - BASIC_ALLOWANCE - CHILD_ALLOWANCE * child_count + rv_mr
        taxable_income_mrs = income_mrs - mpf_mrs - BASIC_ALLOWANCE + rv_mrs
        joint_taxable_income = income_mr + income_mrs - mpf_mr - mpf_mrs - MARRIED_ALLOWANCE - CHILD_ALLOWANCE * child_count + rv_mr + rv_mrs


        tax_mr = max(calculate_tax(taxable_income_mr) - TAX_REDUCTION_CAP, 0)
        tax_mrs = max(calculate_tax(taxable_income_mrs) - TAX_REDUCTION_CAP, 0)
        joint_tax = max(calculate_tax(joint_taxable_income) - TAX_REDUCTION_CAP, 0)
        separate_tax = tax_mr + tax_mrs

        recommendation = recommend_assessment(separate_tax, joint_tax)


        result_str = (
            f"Separate Assessment\n"
            f"Husband (ORSO Scheme: {'Yes' if is_mr_in_mpf_scheme else 'No'})\n"
            f"Income: {format_currency(income_mr)}\n"
            f"Less: MPF contributions {format_currency(mpf_mr)}\n"
            f"Less: Rent {format_currency(rent)}\n"
            f"Net Total Income: {format_currency(income_mr - mpf_mr + rv_mr)}\n"
            f"Less: Basic allowance {format_currency(BASIC_ALLOWANCE)}\n"
            f"Less: Child allowance {format_currency(CHILD_ALLOWANCE * child_count)}\n"
            f"Net Chargeable Income: {format_currency(taxable_income_mr)}\n"
            f"Tax thereon: {format_currency(calculate_tax(taxable_income_mr))}\n"
            f"Less: 100% tax reduction (capped at ${TAX_REDUCTION_CAP})\n"
            f"Tax payable: {format_currency(tax_mr)}\n\n"

            f"Wife (ORSO Scheme: {'Yes' if is_mrs_in_mpf_scheme else 'No'})\n"
            f"Income: {format_currency(income_mrs)}\n"
            f"Less: MPF contributions {format_currency(mpf_mrs)}\n"
            f"Less: Rent {format_currency(rent)}\n"
            f"Net Total Income: {format_currency(income_mrs - mpf_mrs + rv_mrs)}\n"
            f"Less: Basic allowance {format_currency(BASIC_ALLOWANCE)}\n"
            f"Net Chargeable Income: {format_currency(taxable_income_mrs)}\n"
            f"Tax thereon: {format_currency(calculate_tax(taxable_income_mrs))}\n"
            f"Less: 100% tax reduction (capped at ${TAX_REDUCTION_CAP})\n"
            f"Tax payable: {format_currency(tax_mrs)}\n\n"

            f"Joint Assessment\n"
            f"Joint Income: {format_currency(income_mr + income_mrs)}\n"
            f"Less: Total MPF contributions {format_currency(mpf_mr + mpf_mrs)}\n"
            f"Less: Total Rent {format_currency(rent * 2)}\n"
            f"Net Total Income: {format_currency(income_mr + income_mrs - mpf_mr - mpf_mrs - rent * 2)}\n"
            f"Less: Married person's allowance {format_currency(MARRIED_ALLOWANCE)}\n"
            f"Less: Child allowance {format_currency(CHILD_ALLOWANCE * child_count)}\n"
            f"Net Chargeable Income: {format_currency(joint_taxable_income)}\n"
            f"Tax thereon: {format_currency(calculate_tax(joint_taxable_income))}\n"
            f"Less: 100% tax reduction (capped at ${TAX_REDUCTION_CAP})\n"
            f"Tax payable: {format_currency(joint_tax)}\n\n"

            f"Recommendation: {recommendation}\n"
        )

        messagebox.showinfo("Tax Computation Results", result_str)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please make sure all inputs are numeric.")

root = tk.Tk()
root.title("Salaries Tax Computation")

tk.Label(root, text="Husband's Income:").grid(row=0, column=0)
self_income_entry = tk.Entry(root)
self_income_entry.grid(row=0, column=1)

tk.Label(root, text="Wife's Income:").grid(row=1, column=0)
spouse_income_entry = tk.Entry(root)
spouse_income_entry.grid(row=1, column=1)

tk.Label(root, text="Number of Children:").grid(row=2, column=0)
children_entry = tk.Entry(root)
children_entry.insert(0, "0")
children_entry.grid(row=2, column=1)

tk.Label(root, text="Rent:").grid(row=3, column=0)
rent_entry = tk.Entry(root)
rent_entry.insert(0, "0")
rent_entry.grid(row=3, column=1)


mr_mpf_var = tk.BooleanVar()
mrs_mpf_var = tk.BooleanVar()
tk.Checkbutton(root, text="Husband in ORSO Scheme?", variable=mr_mpf_var).grid(row=4, column=0, sticky='w')
tk.Checkbutton(root, text="Wife in ORSO Scheme?", variable=mrs_mpf_var).grid(row=4, column=1, sticky='w')


accomm_var = tk.StringVar(value="Residential")
tk.Radiobutton(root, text="Residential unit/serviced apartment", variable=accomm_var, value="Residential").grid(row=5, column=0, sticky='w')
tk.Radiobutton(root, text="2 rooms in a hotel, hostel or boarding house", variable=accomm_var, value="2 Rooms").grid(row=5, column=1, sticky='w')
tk.Radiobutton(root, text="1 room in a hotel, hostel or boarding house", variable=accomm_var, value="1 Room").grid(row=5, column=2, sticky='w')

calculate_button = tk.Button(root, text="Calculate", command=show_results)
calculate_button.grid(row=6, column=0, columnspan=3)

root.mainloop()