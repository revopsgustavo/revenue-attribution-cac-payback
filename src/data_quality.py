from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; P=ROOT/'data'/'processed'; OUTPUT=P/'data_quality_report.csv'
REQ={'campaigns':['campaign_id','channel_id'],'channels':['channel_id'],'leads':['lead_id','channel_id','campaign_id','created_date'],'opportunities':['opportunity_id','lead_id','channel_id','pipeline_value'],'customers':['customer_id','lead_id','opportunity_id','acquisition_channel_id'],'revenue':['customer_id','revenue_date','new_arr'],'marketing_spend':['campaign_id','channel_id','spend_date','spend_amount'],'touchpoints':['lead_id','account_id','channel_id'],'attribution_models':['model_name','channel_id','attributed_revenue'],'cohorts':['cohort_month','acquisition_channel_id']}
def load(n):
    path=P/f'{n}.csv'; return pd.read_csv(path) if path.exists() else pd.DataFrame()
def validate():
    rows=[]; tables={n:load(n) for n in REQ}
    for n,cols in REQ.items():
        path=P/f'{n}.csv'; df=tables[n]; rows.append({'table_name':n,'check_name':'file_exists','status':'pass' if path.exists() else 'fail','details':str(path)})
        for c in cols:
            rows.append({'table_name':n,'check_name':f'column_exists:{c}','status':'pass' if c in df.columns else 'fail','details':c})
            if c in df.columns and c.endswith('_id'): rows.append({'table_name':n,'check_name':f'not_null:{c}','status':'pass' if df[c].notna().all() else 'fail','details':c})
    channels=set(tables['channels'].get('channel_id',pd.Series(dtype=object)))
    for n,c in [('campaigns','channel_id'),('leads','channel_id'),('marketing_spend','channel_id'),('touchpoints','channel_id')]:
        df=tables[n]; rows.append({'table_name':n,'check_name':'valid_channel_id','status':'pass' if c in df.columns and set(df[c]).issubset(channels) else 'fail','details':c})
    return pd.DataFrame(rows)
def main():
    r=validate(); r.to_csv(OUTPUT,index=False); print(f'Data quality report generated. Failures: {int((r.status=="fail").sum())}')
if __name__=='__main__': main()
