# Z-Facilities Flask Sample

Workflow: Search equipment → open equipment record → create PM/DM work order → view service history.

Run locally:
1. `pip install -r requirements.txt`
2. `python app.py`
3. Open http://127.0.0.1:5000

This sample keeps work orders in memory for demonstration. Restarting the Flask app resets newly created work orders. The next step is persistent storage (Excel or Supabase).
