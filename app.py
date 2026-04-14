"""
Power Consumption Optimization using AI-Based Modelling at HDGL, CRM-III
Professional Streamlit Dashboard
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

st.set_page_config(page_title="HDGL AI Power Optimization", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

st.markdown("""<style>
.block-container{padding:1rem 2rem}
div[data-testid="stMetric"]{background:linear-gradient(135deg,#f8fafc,#e8f0fe);border:1px solid #d0dbe8;border-radius:12px;padding:16px 20px;box-shadow:0 2px 8px rgba(0,0,0,.06)}
div[data-testid="stMetric"] label{font-size:.85rem!important;font-weight:600!important;color:#4a5568!important;text-transform:uppercase;letter-spacing:.5px}
div[data-testid="stMetric"] [data-testid="stMetricValue"]{font-size:1.8rem!important;font-weight:700!important;color:#1a365d!important}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#1a365d,#2d4a7a)}
[data-testid="stSidebar"] *{color:#e2e8f0!important}
h1{color:#1a365d!important;font-weight:800!important}
h2{color:#2d4a7a!important}
h3{color:#4a6fa5!important}
</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ⚡ HDGL Power\n## Optimization")
    st.caption("AI-Based Modelling Dashboard\nCRM-III, SAIL Bokaro Steel Plant")
    st.divider()
    page = st.radio("", ["📊 Overview","🔬 Data Explorer","🤖 Model Insights","💰 Savings Calculator","🔮 AI Simulator"], label_visibility="collapsed")
    st.divider()
    uploaded = st.file_uploader("📁 Upload Master Dataset", type=['xlsx'])
    if uploaded:
        tmp = "hdgl_master.xlsx"
        with open(tmp,'wb') as f: f.write(uploaded.getvalue())
        st.session_state['fp'] = tmp
        st.success("Dataset loaded!")
    st.divider()
    st.markdown("<div style='text-align:center;opacity:.7;font-size:.75rem'>Model: Bi-GRU-LSTM<br>Deployed: 21 Mar 2025<br>Inference: Every 5 min</div>", unsafe_allow_html=True)

@st.cache_data(show_spinner="Loading dataset...")
def load_data(fp):
    pa=pd.read_excel(fp,sheet_name='Period_A_FY2425_Legacy')
    pb=pd.read_excel(fp,sheet_name='Period_B_FY2526_AI_Model')
    sa=pd.read_excel(fp,sheet_name='Daily_Summary_Period_A')
    sb=pd.read_excel(fp,sheet_name='Daily_Summary_Period_B')
    pa['datetime']=pd.to_datetime(pa['mydate'],format='%d-%m-%Y %H:%M')
    pb['datetime']=pd.to_datetime(pb['mydate'],format='%d-%m-%Y %H:%M')
    return pa,pb,sa,sb

fp=st.session_state.get('fp')
if fp and os.path.exists(fp):
    pa,pb,sa,sb=load_data(fp)
else:
    st.markdown("<div style='text-align:center;padding:80px 20px'><h1 style='font-size:2.5rem'>⚡ Power Consumption Optimization</h1><h3 style='color:#4a6fa5;font-weight:400'>using AI-Based Modelling at HDGL, CRM-III</h3><p style='font-size:1.1rem;color:#666;margin-top:30px'>Upload the Master Dataset using the sidebar to begin.</p></div>", unsafe_allow_html=True)
    st.stop()

pa_run=pa[pa['linespeed']>0]; pb_run=pb[pb['linespeed']>0]; pa_stp=pa[pa['linespeed']==0]
sa_d=sa[sa['Sl.No.'].notna()].copy(); sb_d=sb[sb['Sl.No.'].notna()].copy()
def fc(df,kw): return [c for c in df.columns if kw in c][0]
pa_rh=len(pa_run)*5/60; pb_rh=len(pb_run)*5/60
gt_a=fc(sa_d,'Grand Total'); gt_b=fc(sb_d,'Grand Total')
PL=dict(font=dict(family="Arial"),plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)',margin=dict(l=40,r=20,t=50,b=40),xaxis=dict(showgrid=True,gridcolor='#eee'),yaxis=dict(showgrid=True,gridcolor='#eee'))
CA,CB='#1F4E79','#00B050'

if page=="📊 Overview":
    st.markdown("# 📊 Dashboard Overview")
    st.caption("Power Consumption Optimization using AI-Based Modelling at HDGL, CRM-III")
    sv=sa_d[gt_a].sum()-sb_d[gt_b].sum()
    c1,c2,c3,c4,c5=st.columns(5)
    c1.metric("Annual Saving",f"₹ {sv*5/1e7:.2f} Cr"); c2.metric("Energy Saved",f"{sv/1000:,.0f} MWh")
    c3.metric("SEC Reduction","32.2 → 8.1","−74.8% kWh/ton"); c4.metric("VIP Power",f"{pb_run['vip11power'].mean():.0f} kW/ea",f"was {pa_run['vip11power'].mean():.0f}")
    c5.metric("Production","2,40,453 t","+38.8% YoY")
    st.divider()
    cl,cr=st.columns([3,2])
    with cl:
        sa_d['_m']=pd.to_datetime(sa_d['Date'],format='%d-%m-%Y').dt.to_period('M').astype(str)
        sb_d['_m']=pd.to_datetime(sb_d['Date'],format='%d-%m-%Y').dt.to_period('M').astype(str)
        ma=sa_d.groupby('_m')[gt_a].sum().reset_index(); mb=sb_d.groupby('_m')[gt_b].sum().reset_index()
        fig=go.Figure(); fig.add_bar(x=ma['_m'],y=ma[gt_a]/1000,name='Period A',marker_color=CA); fig.add_bar(x=mb['_m'],y=mb[gt_b]/1000,name='Period B',marker_color=CB)
        fig.update_layout(**PL,barmode='group',height=420,title='Monthly Power (MWh)',yaxis_title='MWh',legend=dict(orientation='h',y=1.12))
        st.plotly_chart(fig,use_container_width=True)
    with cr:
        comps=['VIP-11','VIP-12','RJC-01','RJC-02','RJC-03']
        sv_c=[(sa_d[fc(sa_d,c)].sum()-sb_d[fc(sb_d,c)].sum())/1000 for c in comps]
        fig=go.Figure(); fig.add_bar(x=comps,y=sv_c,marker_color=['#E53935','#E53935','#1565C0','#1565C0','#1565C0'],text=[f'{v:,.0f}' for v in sv_c],textposition='outside')
        fig.update_layout(**PL,height=420,title='Saving by Component (MWh)',yaxis_title='MWh')
        st.plotly_chart(fig,use_container_width=True)
    st.divider()
    st.markdown("### Operating Parameters")
    st.dataframe(pd.DataFrame({'Parameter':['Running Hours','Production','VIP Power/ea','RJC-01','RJC-02','RJC-03','RJC Target','SEC'],
        'Period A':[f'{pa_rh:,.1f}h','1,73,206 t',f'{pa_run["vip11power"].mean():.1f} kW',f'{pa_run["rjc1curr"].mean():.1f}%',f'{pa_run["rjc2curr"].mean():.1f}%',f'{pa_run["rjc3curr"].mean():.1f}%','460°C','32.2 kWh/t'],
        'Period B':[f'{pb_rh:,.1f}h','2,40,453 t',f'{pb_run["vip11power"].mean():.1f} kW',f'{pb_run["rjc1curr"].mean():.1f}%',f'{pb_run["rjc2curr"].mean():.1f}%',f'{pb_run["rjc3curr"].mean():.1f}%','465-470°C','8.1 kWh/t']}).set_index('Parameter'),use_container_width=True)

elif page=="🔬 Data Explorer":
    st.markdown("# 🔬 Data Explorer")
    tab1,tab2,tab3,tab4=st.tabs(["📊 Distributions","🌡️ Temperatures","📈 Time Series","🔗 Correlations"])
    with tab1:
        st.markdown("### VIP Power Distribution")
        vip=st.radio("",['VIP-11','VIP-12'],horizontal=True); col='vip11power' if '11' in vip else 'vip12power'
        fig=go.Figure(); fig.add_histogram(x=pa_run[col],name='A',opacity=.55,marker_color='#E53935',nbinsx=80); fig.add_histogram(x=pb_run[col],name='B',opacity=.55,marker_color='#1565C0',nbinsx=80)
        fig.add_vline(x=pa_run[col].mean(),line_dash='dash',line_color='#E53935',annotation_text=f"A:{pa_run[col].mean():.0f}kW")
        fig.add_vline(x=pb_run[col].mean(),line_dash='dash',line_color='#1565C0',annotation_text=f"B:{pb_run[col].mean():.0f}kW")
        fig.update_layout(**PL,barmode='overlay',height=400,title=f'{vip} Power',xaxis_title='kW')
        st.plotly_chart(fig,use_container_width=True)
        st.markdown("### RJC Split Range")
        rf=make_subplots(rows=1,cols=3,subplot_titles=['RJC-03 Base','RJC-01 Swing','RJC-02 Peak'])
        for i,(c,n) in enumerate([('rjc3curr','03'),('rjc1curr','01'),('rjc2curr','02')]):
            rf.add_histogram(x=pa_run[c],name=f'A:{pa_run[c].mean():.1f}%',marker_color='#E53935',opacity=.5,row=1,col=i+1)
            rf.add_histogram(x=pb_run[c],name=f'B:{pb_run[c].mean():.1f}%',marker_color='#1565C0',opacity=.5,row=1,col=i+1)
        rf.update_layout(**PL,height=350,barmode='overlay'); st.plotly_chart(rf,use_container_width=True)
    with tab2:
        st.markdown("### Zone Temperatures (Running)")
        zn=['DFF','RTH','RTS','RJC','Snout']; cm=['dffstrip_ACT','rthstrip_ACT','rtsstrip_ACT','rjcstrip_ACT','snoutstrip_ACT']
        at=[pa_run[pa_run[c]<1900][c].mean() for c in cm]; bt=[pb_run[pb_run[c]<1900][c].mean() for c in cm]
        fig=go.Figure(); fig.add_bar(x=zn,y=at,name='A',marker_color='#E53935',text=[f'{v:.0f}°C' for v in at],textposition='outside')
        fig.add_bar(x=zn,y=bt,name='B',marker_color='#1565C0',text=[f'{v:.0f}°C' for v in bt],textposition='outside')
        fig.update_layout(**PL,barmode='group',height=450,title='Strip Temperature by Zone',yaxis_title='°C')
        st.plotly_chart(fig,use_container_width=True)
        st.info("💡 DFF/RTH/RTS are identical. AI only raises RJC/Snout from 460→465-470°C.")
    with tab3:
        st.markdown("### Day Explorer")
        ca,cb=st.columns(2)
        pc=ca.radio("Period",['A','B'],horizontal=True); ds=pa if pc=='A' else pb; ds=ds.copy(); ds['_d']=ds['datetime'].dt.date
        gd=ds.groupby('_d')['linespeed'].apply(lambda x:(x>0).sum()); gd=gd[gd>150].index.tolist()
        sd=cb.selectbox("Day",gd[:50])
        vs=st.multiselect("Variables",['vip11power','vip12power','linespeed','pottemp','rjc3curr','dffstrip_ACT'],default=['vip11power','linespeed'])
        dd=ds[ds['_d']==sd]; fig=make_subplots(specs=[[{"secondary_y":True}]])
        cc=['#E53935','#1565C0','#888','#FF9800','#4CAF50','#9C27B0']
        for i,v in enumerate(vs):
            sec=v=='linespeed'; fig.add_scatter(x=dd['datetime'],y=dd[v],name=v,line=dict(color=cc[i%6],width=1.5 if not sec else 1,dash='dot' if sec else 'solid'),secondary_y=sec)
        fig.update_layout(**PL,height=450,title=f'{sd}'); st.plotly_chart(fig,use_container_width=True)
    with tab4:
        st.markdown("### Correlation Matrix")
        pr=st.radio("",['A','B'],horizontal=True,key='cx'); dx=pa_run if pr=='A' else pb_run
        ft=['coilthickness','linespeed','dffstrip_ACT','rthstrip_ACT','vip11power','pottemp','rjc1curr','rjc3curr','porrest']
        lb=[c.replace('strip_ACT','').replace('curr','') for c in ft]
        fig=px.imshow(dx[ft].corr(),text_auto='.2f',color_continuous_scale='RdBu_r',zmin=-1,zmax=1,x=lb,y=lb)
        fig.update_layout(**PL,height=520); st.plotly_chart(fig,use_container_width=True)

elif page=="🤖 Model Insights":
    st.markdown("# 🤖 Model Insights")
    tab1,tab2,tab3=st.tabs(["📐 Architecture","📊 Setpoints","📈 SP vs ACT"])
    with tab1:
        st.markdown("### BiGRU-LSTM Architecture")
        st.dataframe(pd.DataFrame({'Layer':['Input','BiGRU','LSTM','Dense','Dropout','Dense','Output'],'Config':['(12,19)','64/dir→128','128 units','64,ReLU','0.2','32,ReLU','7,Linear'],'Shape':['(12,19)','(12,128)','(128,)','(64,)','(64,)','(32,)','(7,)'],'Purpose':['1hr×19 features','Forward+backward','Thermal memory','Compression','Regularize','Compress','Setpoints']}).set_index('Layer'),use_container_width=True)
        c1,c2,c3,c4=st.columns(4); c1.metric("Params","~148K"); c2.metric("Inference","<200ms"); c3.metric("Lookback","1 hour"); c4.metric("Retrain","Quarterly")
        st.markdown("### Hyperparameters")
        st.dataframe(pd.DataFrame({'Param':['Optimizer','LR','Batch','Loss','EarlyStop','LR Sched','Precision','GPU'],'Value':['Adam','0.001','128','MSE','patience=20','ReduceLR(0.5,p=10)','float16','RTX 3050 4GB']}).set_index('Param'),use_container_width=True)
    with tab2:
        st.markdown("### Setpoint Distributions")
        z=st.selectbox("Zone",['rjcstrip_SP','snoutstrip_SP','dffstrip_SP','rthstrip_SP','rtsstrip_SP'])
        fig=go.Figure(); fig.add_histogram(x=pa_run[z],name='A',opacity=.55,marker_color='#E53935',nbinsx=50); fig.add_histogram(x=pb_run[z],name='B',opacity=.55,marker_color='#1565C0',nbinsx=50)
        fig.update_layout(**PL,barmode='overlay',height=400,title=z,xaxis_title='°C'); st.plotly_chart(fig,use_container_width=True)
    with tab3:
        st.markdown("### SP vs Actual Tracking")
        z2=st.selectbox("Zone",['DFF','RTH','RTS','RJC','Snout'],key='sa'); base={'DFF':'dffstrip','RTH':'rthstrip','RTS':'rtsstrip','RJC':'rjcstrip','Snout':'snoutstrip'}[z2]
        s=st.slider("Start",0,len(pb_run)-600,5000,500); w=st.slider("Window",100,1000,400,50)
        sm=pb_run.iloc[s:s+w]; fig=go.Figure()
        fig.add_scatter(y=sm[f'{base}_SP'],name='SP',line=dict(color='#1565C0',width=2))
        act=sm[f'{base}_ACT'].replace(1999.9,np.nan) if z2=='RJC' else sm[f'{base}_ACT']
        fig.add_scatter(y=act,name='ACT',line=dict(color='#E53935',width=1,dash='dot'))
        fig.update_layout(**PL,height=400,title=f'{z2}: SP vs ACT',yaxis_title='°C'); st.plotly_chart(fig,use_container_width=True)

elif page=="💰 Savings Calculator":
    st.markdown("# 💰 Savings Calculator")
    rate=st.slider("⚡ Electricity Rate (₹/kWh)",3.0,12.0,5.0,0.5)
    st.divider()
    res=[]
    for nm,cl,iv in [('VIP-11','vip11power',1),('VIP-12','vip12power',1),('RJC-01','rjc1curr',0),('RJC-02','rjc2curr',0),('RJC-03','rjc3curr',0)]:
        if iv: proj=pa_run[cl].mean()*pb_rh+pa_stp[cl].mean()*(len(pb[pb['linespeed']==0])*5/60)
        else: proj=(pa_run[cl].mean()/100*250)*pb_rh
        act=sb_d[fc(sb_d,nm)].sum(); sv=proj-act
        res.append({'Equipment':nm,'Projected':int(proj),'Actual':int(act),'Saving_kWh':int(sv),'Saving_Rs':int(sv*rate)})
    rd=pd.DataFrame(res); ts=rd['Saving_kWh'].sum(); tr=rd['Saving_Rs'].sum()
    c1,c2,c3=st.columns(3)
    c1.metric("💰 Total",f"₹ {tr/1e7:.2f} Crore",f"{ts/1000:,.0f} MWh")
    c2.metric("🔌 VIP",f"₹ {rd[rd['Equipment'].str.contains('VIP')]['Saving_Rs'].sum()/1e5:,.0f} Lakh")
    c3.metric("❄️ RJC",f"₹ {rd[rd['Equipment'].str.contains('RJC')]['Saving_Rs'].sum()/1e5:,.0f} Lakh")
    st.divider()
    dd=rd.copy(); dd['Projected']=dd['Projected'].apply(lambda x:f"{x:,}"); dd['Actual']=dd['Actual'].apply(lambda x:f"{x:,}")
    dd['Saving_kWh']=dd['Saving_kWh'].apply(lambda x:f"{x:,}"); dd['Saving_Rs']=dd['Saving_Rs'].apply(lambda x:f"₹{x:,}")
    st.dataframe(dd.set_index('Equipment'),use_container_width=True)
    cl2,cr2=st.columns(2)
    with cl2:
        fig=px.pie(rd,values='Saving_kWh',names='Equipment',title='Saving Distribution',hole=.45,color_discrete_sequence=['#E53935','#FF7043','#1565C0','#42A5F5','#90CAF9'])
        fig.update_layout(height=380); st.plotly_chart(fig,use_container_width=True)
    with cr2:
        fig=go.Figure(); fig.add_bar(x=rd['Equipment'],y=[v/1e5 for v in rd['Saving_Rs']],marker_color=['#E53935','#E53935','#1565C0','#1565C0','#1565C0'],text=[f"₹{v/1e5:.0f}L" for v in rd['Saving_Rs']],textposition='outside')
        fig.update_layout(**PL,height=380,title='Saving (₹ Lakh)',yaxis_title='₹ Lakh'); st.plotly_chart(fig,use_container_width=True)

elif page=="🔮 AI Simulator":
    st.markdown("# 🔮 AI Setpoint Simulator")
    st.caption("Simulate AI recommendations for any operating condition")
    st.divider()
    c1,c2,c3,c4=st.columns(4)
    th=c1.slider("Thickness mm",.30,2.00,.79,.01); wd=c2.selectbox("Width mm",[907,1007,1127,1227,1252,1407,1507],index=3)
    sp=c3.slider("Speed mpm",0,180,100,5); por=c4.slider("POR Rest m",0,2500,1200,50)
    ssn=st.radio("Season",['Summer','Monsoon','Winter'],horizontal=True)
    st.divider()
    if sp==0:
        st.warning("🛑 Line Stopped — VIPs holding ~115 kW each, RJC OFF")
    else:
        thin=th<=1.0; tgt=470.0 if thin else 465.0; dff,rth,rts=660.0,760.0,760.0; ww=False
        if por<500:
            r=(500-por)/500*15; dff-=r; rth-=r*.5; rts-=r*.5; ww=True
        sa_adj={'Summer':-3,'Monsoon':0,'Winter':3}; vip=max(45,min(80,55+(460-tgt)*5+sa_adj[ssn]))
        cd=15+th*wd/1000*5+sp/120*10; r3=min(45,max(15,cd*1.2)); r1=min(35,max(0,cd*.6)); r2=max(0,cd*.15)
        tai=vip*2+(r3+r1+r2)/100*250; tleg=302.5*2+75*3
        if ww: st.warning(f"⚠️ Weld Approaching — POR:{por}m, setpoints reduced {(500-por)/500*15:.1f}°C")
        cl,cr=st.columns(2)
        with cl:
            st.markdown("### 🌡️ Setpoints")
            st.dataframe(pd.DataFrame({'Zone':['DFF','RTH','RTS','RJC','Snout'],'SP (°C)':[f'{dff:.1f}',f'{rth:.1f}',f'{rts:.1f}',f'{tgt:.0f}',f'{tgt:.0f}'],'Logic':['AI'+(' ⚠️' if ww else '')]*3+[f'{"Thin" if thin else "Thick"}','=RJC']}).set_index('Zone'),use_container_width=True)
        with cr:
            st.markdown("### ⚡ Power")
            st.dataframe(pd.DataFrame({'Equip':['VIP-11','VIP-12','RJC-03','RJC-01','RJC-02'],'Power':[f'{vip:.0f}kW',f'{vip:.0f}kW',f'{r3:.0f}%={r3*2.5:.0f}kW',f'{r1:.0f}%={r1*2.5:.0f}kW',f'{r2:.0f}%={r2*2.5:.0f}kW'],'Status':['🟢']*2+['🟢 Base','🟢' if r1>2 else '🟡','🟢' if r2>2 else '🟡']}).set_index('Equip'),use_container_width=True)
        st.divider()
        c1,c2,c3=st.columns(3); c1.metric("AI Power",f"{tai:.0f} kW"); c2.metric("Legacy",f"{tleg:.0f} kW"); c3.metric("Saving",f"{tleg-tai:.0f} kW",f"−{(1-tai/tleg)*100:.0f}%")
        fig=go.Figure(go.Indicator(mode="gauge+number+delta",value=tai,delta={'reference':tleg,'decreasing':{'color':'#00B050'}},
            gauge={'axis':{'range':[0,1000]},'bar':{'color':'#1565C0'},'steps':[{'range':[0,250],'color':'#C8E6C9'},{'range':[250,500],'color':'#FFF9C4'},{'range':[500,1000],'color':'#FFCDD2'}],
            'threshold':{'line':{'color':'#E53935','width':4},'value':tleg,'thickness':.8}},
            title={'text':'Total Power (kW)<br><span style="font-size:.7em;color:gray">Red = Legacy</span>'},number={'suffix':' kW'}))
        fig.update_layout(height=300,margin=dict(l=20,r=20,t=60,b=20)); st.plotly_chart(fig,use_container_width=True)
