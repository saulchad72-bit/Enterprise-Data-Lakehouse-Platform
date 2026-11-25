import csv, json
from pathlib import Path

def run(source, destination):
    rows=list(csv.DictReader(open(source,newline='')))
    bronze=[dict(r, _ingested_at='batch-demo') for r in rows]
    current={}
    for r in bronze:
        if not r['order_id'] or not r['amount']:
            continue
        try: amount=float(r['amount'])
        except ValueError: continue
        record={'order_id':r['order_id'],'customer_id':r['customer_id'], 'amount':amount,'updated_at':r['updated_at']}
        if r['order_id'] not in current or r['updated_at']>=current[r['order_id']]['updated_at']:
            current[r['order_id']]=record
    silver=list(current.values())
    gold={}
    for r in silver:
        gold[r['customer_id']]=round(gold.get(r['customer_id'],0)+r['amount'],2)
    result={'bronze':bronze,'silver':silver,'gold':[{'customer_id':k,'total_spend':v} for k,v in sorted(gold.items())]}
    Path(destination).write_text(json.dumps(result,indent=2)); return result
