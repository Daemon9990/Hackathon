def calculate_savings(income, expenses):
    savings = income - expenses
    if savings < 0:
        return f"⚠️ You are overspending! Your deficit is ₹{abs(savings)}"
    elif savings == 0:
        return "💡 You are breaking even. Try saving at least 20% of income."
    else:
        return f"✅ Your monthly savings: ₹{savings}"


def calculate_tax(salary, investments):
    taxable_income = max(salary - investments, 0)

    if taxable_income <= 250000:
        tax = 0
    elif taxable_income <= 500000:
        tax = (taxable_income - 250000) * 0.05
    elif taxable_income <= 1000000:
        tax = 12500 + (taxable_income - 500000) * 0.2
    else:
        tax = 112500 + (taxable_income - 1000000) * 0.3

    return f"💸 Estimated Income Tax: ₹{int(tax)}"


def suggest_investment(risk_level):
    if risk_level == "low":
        return "🟢 Suggested Low-risk investments:\n- Fixed Deposits\n- PPF\n- Government Bonds"
    elif risk_level == "balanced":
        return "🟡 Suggested Balanced investments:\n- Index Funds\n- Mutual Funds\n- REITs"
    elif risk_level == "high":
        return "🔴 Suggested High-risk investments:\n- Stocks\n- Cryptocurrencies\n- Startups"
    else:
        return "❌ Invalid risk level. Use low | balanced | high"


def add_goal(db, user_id, amount, description, deadline):
    if user_id not in db:
        db[user_id] = {"goals": []}

    db[user_id]["goals"].append({
        "amount": amount,
        "description": description,
        "deadline": deadline
    })

    return f"🎯 Goal added: Save ₹{amount} for {description} by {deadline}"


def track_goals(db, user_id):
    if user_id not in db or not db[user_id]["goals"]:
        return "📭 You have no active goals."

    msg = "📊 Your Goals:\n\n"
    for i, g in enumerate(db[user_id]["goals"], 1):
        msg += f"{i}. ₹{g['amount']} for {g['description']} (by {g['deadline']})\n"
    return msg
