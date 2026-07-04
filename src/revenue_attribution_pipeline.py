from __future__ import annotations
import sqlite3
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'data'/'processed'
DB=ROOT/'data'/'database'/'revenue_attribution_case.sqlite'
CHANNELS=[('ch_paid_search','Paid Search','Paid',492000,900,.58,.38,.52,.18,42000,.86,.76),('ch_organic','Organic','Owned',87000,300,.63,.55,.61,.27,39000,.91,.78),('ch_referral','Referral','Earned',48000,130,.76,.70,.72,.40,48000,.94,.80),('ch_paid_social','Paid Social','Paid',264000,980,.42,.18,.36,.11,25000,.75,.70),('ch_events','Events','Offline',372000,210,.68,.61,.70,.16,89000,.88,.77),('ch_partner','Partner','Partner',138000,260,.69,.62,.66,.30,52000,.95,.79),('ch_webinar','Webinar','Owned',108000,360,.60,.34,.56,.13,33000,.82,.74)]
SPECS={'ch_paid_search':[('paid_search_core','Search - Core Intent',.45,1.10),('paid_search_broad','Search - Broad Match',.55,.58)],'ch_organic':[('organic_seo_bottom','SEO - Bottom Funnel',.55,1.24),('organic_content_hub','Content Hub',.45,.94)],'ch_referral':[('referral_customer','Customer Referral',.70,1.34),('referral_advisor','Advisor Referral',.30,1.12)],'ch_paid_social':[('paid_social_lead_ads','Lead Ads - Benchmark Report',.65,.42),('paid_social_retargeting','Retargeting - Product Proof',.35,.85)],'ch_events':[('events_flagship','Industry Flagship Event',.75,1.12),('events_field','Field Dinner Series',.25,1.22)],'ch_partner':[('partner_cloud','Cloud Marketplace Co-sell',.56,1.18),('partner_consulting','Consulting Partner Motion',.44,1.08)],'ch_webinar':[('webinar_exec','Executive Webinar',.44,1.28),('webinar_ops','Ops Practitioner Webinar',.56,.76)]}
def generate_data():
 P.mkdir(parents=True,exist_ok=True); DB.parent.mkdir(parents=True,exist_ok=True); months=pd.date_range('2026-01-01',periods=6,freq='MS')
 channels=pd.DataFrame(CHANNELS,columns=['channel_id','channel_name','channel_type','spend','lead_count','mql_rate','sql_rate','opp_rate','win_rate','arr_mean','retention_rate','gross_margin']); channels['strategic_role']=['captura de demanda','demanda orgânica','indicação qualificada','volume pago','enterprise pipeline','ecossistema','educação e nutrição']
 campaigns=[]; spend=[]; leads=[]; opps=[]; customers=[]; revenue=[]; touches=[]; li=oi=ci=1
 for _,ch in channels.iterrows():
  for campaign_id,campaign_name,share,quality in SPECS[ch.channel_id]:
   campaigns.append({'campaign_id':campaign_id,'channel_id':ch.channel_id,'campaign_name':campaign_name,'campaign_type':ch.channel_type,'spend_share':share,'quality_factor':quality,'start_date':'2026-01-01','end_date':'2026-06-30','objective':'pipeline'})
   for m in months: spend.append({'spend_id':f'sp_{campaign_id}_{m:%Y%m}','campaign_id':campaign_id,'channel_id':ch.channel_id,'spend_date':f'{m:%Y-%m-%d}','spend_month':f'{m:%Y-%m}','spend_amount':round(ch.spend*share/6,2),'budget_owner':'Marketing'})
   lead_total=int(ch.lead_count*share); mql_total=int(lead_total*min(.95,ch.mql_rate*quality)); sql_total=int(mql_total*min(.90,ch.sql_rate*quality)); opp_total=int(sql_total*min(.88,ch.opp_rate*quality)); win_total=max(1,int(opp_total*min(.70,ch.win_rate*quality)))
   if campaign_id=='events_flagship': win_total=max(1,int(opp_total*.10))
   for i in range(lead_total):
    lid=f'lead_{li:05d}'; acct=f'acct_{li:05d}'; dt=months[i%6]+pd.Timedelta(days=i%25); li+=1; non=(i/max(lead_total,1))<(.35 if campaign_id=='paid_social_lead_ads' else .20 if campaign_id=='paid_search_broad' else .07)
    leads.append({'lead_id':lid,'account_id':acct,'created_date':f'{dt:%Y-%m-%d}','created_month':f'{dt:%Y-%m}','channel_id':ch.channel_id,'campaign_id':campaign_id,'lead_source':ch.channel_name,'is_mql':i<mql_total,'is_sql':i<sql_total,'is_icp':not non,'company_size':['SMB','Mid-Market','Enterprise'][i%3],'intent_score':round(45+quality*25+i%9,1)})
    first=ch.channel_id; last=ch.channel_id
    if ch.channel_id in ['ch_paid_social','ch_paid_search','ch_webinar'] and i%3==0: last=['ch_organic','ch_partner','ch_referral'][i%3]
    touches.append({'touchpoint_id':f'tp_{lid}_1','lead_id':lid,'account_id':acct,'touch_date':f'{dt:%Y-%m-%d}','channel_id':first,'campaign_id':campaign_id,'touch_order':1,'is_first_touch':True,'is_last_touch':first==last})
    if first!=last: touches.append({'touchpoint_id':f'tp_{lid}_2','lead_id':lid,'account_id':acct,'touch_date':f'{dt+pd.Timedelta(days=8):%Y-%m-%d}','channel_id':last,'campaign_id':campaign_id,'touch_order':2,'is_first_touch':False,'is_last_touch':True})
    if i<opp_total:
     oid=f'opp_{oi:05d}'; oi+=1; arr=round(ch.arr_mean*(.85+(i%6)*.06),2); close=dt+pd.Timedelta(days=35+(i%50)); won=i<win_total
     opps.append({'opportunity_id':oid,'lead_id':lid,'account_id':acct,'channel_id':ch.channel_id,'campaign_id':campaign_id,'created_date':f'{dt+pd.Timedelta(days=7):%Y-%m-%d}','close_date':f'{close:%Y-%m-%d}','stage':'closed_won' if won else ('closed_lost' if i%2 else 'proposal'),'pipeline_value':round(arr*(1.7+(i%3)*.2),2),'expected_arr':arr,'sales_cycle_days':int((close-dt).days)})
     if won:
      cid=f'cust_{ci:05d}'; ci+=1; retained=(i%100)/100<ch.retention_rate; nrr=0 if not retained else round(.93+ch.retention_rate*.15+(i%4)*.01,3)
      customers.append({'customer_id':cid,'lead_id':lid,'opportunity_id':oid,'account_id':acct,'acquisition_channel_id':ch.channel_id,'campaign_id':campaign_id,'acquisition_date':f'{close:%Y-%m-%d}','cohort_month':f'{close:%Y-%m}','arr':arr,'gross_margin':ch.gross_margin,'retained_90d':retained,'churned_90d':not retained,'nrr_90d':nrr})
      revenue.append({'revenue_id':f'rev_{cid}','customer_id':cid,'opportunity_id':oid,'channel_id':ch.channel_id,'campaign_id':campaign_id,'revenue_date':f'{close:%Y-%m-%d}','revenue_month':f'{close:%Y-%m}','new_arr':arr,'recognized_revenue':round(arr/12,2),'gross_margin':ch.gross_margin})
 frames={'campaigns':pd.DataFrame(campaigns),'channels':channels,'leads':pd.DataFrame(leads),'opportunities':pd.DataFrame(opps),'customers':pd.DataFrame(customers),'revenue':pd.DataFrame(revenue),'marketing_spend':pd.DataFrame(spend),'touchpoints':pd.DataFrame(touches)}
 cohorts=frames['customers'].groupby(['cohort_month','acquisition_channel_id'],as_index=False).agg(customers=('customer_id','nunique'),retained_90d=('retained_90d','sum'),churned_90d=('churned_90d','sum'),avg_nrr_90d=('nrr_90d','mean'),avg_arr=('arr','mean')); cohorts['retention_rate_90d']=cohorts.retained_90d/cohorts.customers
 base=frames['revenue'].merge(frames['customers'][['customer_id','lead_id']],on='customer_id'); touch=frames['touchpoints'].merge(base[['lead_id','customer_id','new_arr']],on='lead_id'); attrs=[]
 for model,flag in [('first_touch','is_first_touch'),('last_touch','is_last_touch')]:
  part=touch[touch[flag]].groupby('channel_id',as_index=False).agg(attributed_revenue=('new_arr','sum'),customer_count=('customer_id','nunique')); part['model_name']=model; attrs.append(part)
 touch['touches']=touch.groupby('lead_id').touchpoint_id.transform('count'); touch['weighted_revenue']=touch.new_arr/touch.touches; mt=touch.groupby('channel_id',as_index=False).agg(attributed_revenue=('weighted_revenue','sum'),customer_count=('customer_id','nunique')); mt['model_name']='multi_touch_equal'; attrs.append(mt)
 frames['attribution_models']=pd.concat(attrs,ignore_index=True)[['model_name','channel_id','attributed_revenue','customer_count']]; frames['cohorts']=cohorts
 with sqlite3.connect(DB) as conn:
  for name,df in frames.items(): df.to_csv(P/f'{name}.csv',index=False); df.to_sql(name,conn,if_exists='replace',index=False)
 return frames
if __name__=='__main__':
 frames=generate_data(); print(f"Generated {len(frames['leads'])} leads, {len(frames['opportunities'])} opportunities and {len(frames['customers'])} customers."); print(f'SQLite database generated at {DB}')
