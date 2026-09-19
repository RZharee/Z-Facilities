from flask import Flask, render_template, request, redirect, url_for, abort
from datetime import datetime

app = Flask(__name__)

# SAMPLE DATA ONLY. Later we can replace this with Excel or Supabase.
devices = [
    {"asset":"C224561","serial":"ECG00125","manufacturer":"GE Healthcare","model":"MAC 5500 HD","category":"ECG","department":"Cardiology","status":"In Service"},
    {"asset":"C224562","serial":"LP150234","manufacturer":"Stryker","model":"LIFEPAK 15","category":"Defibrillator","department":"Emergency","status":"In Service"},
    {"asset":"C224563","serial":"MX450871","manufacturer":"Philips","model":"IntelliVue MX450","category":"Patient Monitor","department":"ICU","status":"In Service"},
    {"asset":"C224564","serial":"ALP45210","manufacturer":"BD","model":"Alaris LVP","category":"Infusion Pump","department":"Medical Unit","status":"Out for Repair"},
    {"asset":"C224565","serial":"N5953392","manufacturer":"Medtronic","model":"Nellcor N-595","category":"Pulse Oximeter","department":"Respiratory","status":"In Service"},
]

workorders = [
    {"wo":"WR001","asset":"C224562","date":"2026-01-15","type":"PM","biomed":"J. Smith","description":"Annual preventive maintenance","work_performed":"Inspection and performance verification completed.","status":"Closed"},
    {"wo":"WR002","asset":"C224562","date":"2026-03-20","type":"DM","biomed":"A. Lee","description":"Battery not holding charge","work_performed":"Battery replaced and unit tested.","status":"Closed"},
]

def get_device(asset):
    return next((d for d in devices if d["asset"].lower() == asset.lower()), None)

@app.route("/")
def home():
    q = request.args.get("q", "").strip().lower()
    results = []
    if q:
        for d in devices:
            haystack = " ".join([d["asset"], d["serial"], d["manufacturer"], d["model"], d["category"]]).lower()
            if q in haystack:
                results.append(d)
    return render_template("home.html", q=request.args.get("q",""), results=results)

@app.route("/device/<asset>")
def device(asset):
    d = get_device(asset)
    if not d:
        abort(404)
    history = [w for w in workorders if w["asset"].lower() == asset.lower()]
    history.sort(key=lambda x: x["date"], reverse=True)
    return render_template("device.html", device=d, history=history)

@app.route("/device/<asset>/workorder", methods=["GET", "POST"])
def create_workorder(asset):
    d = get_device(asset)
    if not d:
        abort(404)
    if request.method == "POST":
        next_number = max([int(w["wo"][2:]) for w in workorders] or [0]) + 1
        wo = f"WR{next_number:03d}"
        workorders.append({
            "wo": wo,
            "asset": asset,
            "date": request.form.get("date") or datetime.now().strftime("%Y-%m-%d"),
            "type": request.form.get("type", "DM"),
            "biomed": request.form.get("biomed", "").strip(),
            "description": request.form.get("description", "").strip(),
            "work_performed": request.form.get("work_performed", "").strip(),
            "status": request.form.get("status", "Open")
        })
        return redirect(url_for("device", asset=asset))
    next_number = max([int(w["wo"][2:]) for w in workorders] or [0]) + 1
    return render_template("workorder.html", device=d, next_wo=f"WR{next_number:03d}", today=datetime.now().strftime("%Y-%m-%d"))

if __name__ == "__main__":
    app.run(debug=True)
