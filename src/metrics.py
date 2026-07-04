from __future__ import annotations
from pathlib import Path
import pandas as pd
try:
 from src.utils import safe_divide
except ModuleNotFoundError:
 from utils import safe_divide
ROOT=Path(__file__).resolve().parents[1]; PROCESSED=ROOT/'data'/'processed'; TODAY=pd.Timestamp('2026-07-04'); OPEN={'Prospecting','Discovery','Solution','Proposal','Negotiation','Procurement','Contract'}; ADV={'Negotiation','Procurement','Contract'}
def load_table(n,base_path=PROCESSED):
 p=base_path/f'{n}.csv'; return pd.read_csv(p) if p.exists() else pd.DataFrame()
def load_all(base_path=PROCESSED): return {n:load_table(n,base_path) for n in ['leads','accounts','contacts','opportunities','users','activities','forecast_categories','stages','crm_audit_log','data_quality_checks','remediation_tasks']}
def blank(s): return s.isna()|s.astype(str).str.strip().eq('')
def duplicate_rate(df,subset):
 subset=[subset] if isinstance(subset,str) else subset; return safe_divide(int(df.duplicated(subset=subset,keep=False).sum()),len(df)) if not df.empty and set(subset).issubset(df.columns) else 0.0
def lead_missing_source_rate(df): return safe_divide(int(blank(df['source']).sum()),len(df)) if not df.empty and 'source' in df else 0.0
def duplicate_leads(df): return df[df.duplicated(['email'],keep=False)].copy() if not df.empty and 'email' in df else pd.DataFrame()
def duplicate_accounts(df): return df[df.duplicated(['account_name','domain'],keep=False)].copy() if not df.empty and {'account_name','domain'}.issubset(df.columns) else pd.DataFrame()
def contacts_without_account(df): return df[blank(df['account_id'])].copy() if not df.empty and 'account_id' in df else pd.DataFrame()
def accounts_without_owner(df): return df[blank(df['owner_id'])].copy() if not df.empty and 'owner_id' in df else pd.DataFrame()
def opportunities_without_owner(df): return df[blank(df['owner_id'])].copy() if not df.empty and 'owner_id' in df else pd.DataFrame()
def opportunities_without_close_date(df): return df[blank(df['close_date'])].copy() if not df.empty and 'close_date' in df else pd.DataFrame()
def open_opportunities(df): return df[df['stage'].isin(OPEN)].copy() if not df.empty and 'stage' in df else pd.DataFrame()
def opportunities_without_next_step(df):
 o=open_opportunities(df); return o[blank(o['next_step'])].copy() if not o.empty and 'next_step' in o else pd.DataFrame()
def stale_opportunities(df,days=20):
 o=open_opportunities(df); return o[(TODAY-pd.to_datetime(o['last_stage_change_date'],errors='coerce')).dt.days>days].copy() if not o.empty else pd.DataFrame()
def advanced_stage_without_activity(o,a,days=14):
 if o.empty or a.empty: return pd.DataFrame()
 last=a.groupby('related_object_id',as_index=False).agg(last_activity_date=('activity_date','max')); m=o.merge(last,left_on='opportunity_id',right_on='related_object_id',how='left'); d=pd.to_datetime(m['last_activity_date'],errors='coerce'); return m[m['stage'].isin(ADV)&(d.isna()|((TODAY-d).dt.days>days))].copy()
def closed_won_without_amount(df):
 amount=pd.to_numeric(df['amount'],errors='coerce') if not df.empty and 'amount' in df else pd.Series(dtype=float); return df[df['stage'].eq('Closed Won')&(amount<=0)].copy() if not df.empty and 'stage' in df else pd.DataFrame()
def closed_lost_without_loss_reason(df): return df[df['stage'].eq('Closed Lost')&blank(df['loss_reason'])].copy() if not df.empty and {'stage','loss_reason'}.issubset(df.columns) else pd.DataFrame()
def opportunities_with_zero_amount(df): return df[pd.to_numeric(df['amount'],errors='coerce').fillna(0)<=0].copy() if not df.empty and 'amount' in df else pd.DataFrame()
def open_opportunities_with_past_close_date(df):
 o=open_opportunities(df); return o[pd.to_datetime(o['close_date'],errors='coerce')<TODAY].copy() if not o.empty else pd.DataFrame()
def forecast_category_inconsistencies(df): return df[((df['stage']=='Discovery')&(df['forecast_category']!='Pipeline'))|((df['stage']=='Negotiation')&(~df['forecast_category'].isin(['Best Case','Commit'])))].copy() if not df.empty and {'stage','forecast_category'}.issubset(df.columns) else pd.DataFrame()
def invalid_stage_probability_combinations(df): return df[pd.to_numeric(df['probability'],errors='coerce')>.95].copy() if not df.empty and 'probability' in df else pd.DataFrame()
def manual_close_date_change_rate(df): return safe_divide(int(df['field_changed'].eq('close_date').sum()),len(df)) if not df.empty and 'field_changed' in df else 0.0
def remediation_completion_rate(df): return safe_divide(int(df['status'].eq('completed').sum()),len(df)) if not df.empty and 'status' in df else 0.0
def overdue_remediation_tasks(df): return df[(pd.to_datetime(df['due_date'],errors='coerce')<TODAY)&~df['status'].eq('completed')].copy() if not df.empty and {'due_date','status'}.issubset(df.columns) else pd.DataFrame()
def data_quality_issues_by_owner(t): return pd.DataFrame()
def data_quality_issues_by_object(t):
 l,a,c,o=t['leads'],t['accounts'],t['contacts'],t['opportunities']; return pd.DataFrame([{'object':'leads','issue_count':len(duplicate_leads(l))+int(lead_missing_source_rate(l)*len(l))},{'object':'accounts','issue_count':len(duplicate_accounts(a))+len(accounts_without_owner(a))},{'object':'contacts','issue_count':len(contacts_without_account(c))},{'object':'opportunities','issue_count':len(opportunities_without_owner(o))+len(opportunities_without_close_date(o))+len(opportunities_without_next_step(o))+len(stale_opportunities(o))+len(opportunities_with_zero_amount(o))+len(open_opportunities_with_past_close_date(o))+len(invalid_stage_probability_combinations(o))+len(forecast_category_inconsistencies(o))}])
def revenue_at_risk_from_data_quality(o): return float(pd.to_numeric(o.loc[blank(o['owner_id'])|blank(o['close_date'])|blank(o['next_step'])|(pd.to_numeric(o['amount'],errors='coerce').fillna(0)<=0),'amount'],errors='coerce').fillna(0).clip(lower=0).sum()) if not o.empty else 0.0
def forecast_reliability_score(o,a=None): return max(0,min(100,100-(len(opportunities_without_close_date(o))+len(forecast_category_inconsistencies(o))+len(invalid_stage_probability_combinations(o))+len(open_opportunities_with_past_close_date(o)))*1.2)) if not o.empty else 100.0
def pipeline_hygiene_score(o,a=None): return max(0,min(100,100-(len(opportunities_without_next_step(o))+len(stale_opportunities(o))+len(opportunities_without_owner(o))+len(opportunities_with_zero_amount(o)))*1.1)) if not o.empty else 100.0
def object_quality_score(obj,t):
 df=t.get(obj,pd.DataFrame()); issues=data_quality_issues_by_object(t).set_index('object').loc[obj,'issue_count'] if not df.empty else 0; return max(0,min(100,100-safe_divide(issues,len(df))*100)) if not df.empty else 0.0
def crm_data_quality_score(t):
 o=t['opportunities']; a=t.get('activities',pd.DataFrame()); vals=[object_quality_score(x,t) for x in ['leads','accounts','contacts','opportunities']]+[forecast_reliability_score(o,a),pipeline_hygiene_score(o,a)]; return round(sum(vals)/len(vals),2)
def missing_required_fields(t):
 req={'leads':['lead_id','source'],'accounts':['account_id','owner_id'],'contacts':['contact_id','account_id'],'opportunities':['opportunity_id','account_id','owner_id','amount','close_date','stage','forecast_category','probability'],'users':['user_id'],'activities':['activity_id','related_object_id'],'forecast_categories':['forecast_category'],'stages':['stage'],'crm_audit_log':['event_id'],'data_quality_checks':['check_id'],'remediation_tasks':['task_id']}; rows=[]
 for tbl,cols in req.items():
  df=t.get(tbl,pd.DataFrame())
  for col in cols:
   m=len(df) if col not in df else int(blank(df[col]).sum()); rows.append({'object':tbl,'field':col,'missing_count':m,'missing_rate':safe_divide(m,len(df))})
 return pd.DataFrame(rows)
def critical_issue_count(g): return int(g.get('severity',pd.Series(dtype=str)).eq('critical').sum())
def high_issue_count(g): return int(g.get('severity',pd.Series(dtype=str)).eq('high').sum())
def executive_summary_metrics(t):
 o=t['opportunities']; a=t.get('activities',pd.DataFrame()); return {'crm_data_quality_score':crm_data_quality_score(t),'forecast_reliability_score':forecast_reliability_score(o,a),'pipeline_hygiene_score':pipeline_hygiene_score(o,a),'revenue_at_risk_from_data_quality':revenue_at_risk_from_data_quality(o),'lead_missing_source_rate':lead_missing_source_rate(t['leads']),'duplicate_lead_rate':duplicate_rate(t['leads'],'email'),'duplicate_account_rate':duplicate_rate(t['accounts'],['account_name','domain']),'manual_close_date_change_rate':manual_close_date_change_rate(t['crm_audit_log']),'remediation_completion_rate':remediation_completion_rate(t['remediation_tasks'])}
