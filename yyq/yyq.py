import streamlit as st
from openai import OpenAI
import pandas as pd
import numpy as np
import time

# --- 页面全局配置 ---
st.set_page_config(page_title="GlobalTrade AI Hub", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")

# --- 1. 全局多语言 UI 字典 (i18n) - 5国语言全覆盖 ---
TRANSLATIONS = {
    "English": {
        "nav_workspace": "🧭 Workspace",
        "mod_front": "💬 AI Agent Hub (Front)",
        "mod_back": "📈 Market Intelligence (Back)",
        "lang_label": "🌐 Global Language",
        "dept_select": "🏢 Department Select",
        "agent_sales": "🛒 Sales & Sourcing",
        "agent_logistics": "🚢 Logistics & Customs",
        "agent_support": "🔧 After-Sales Support",
        "agent_sales_name": "Senior Sales Agent",
        "agent_sales_desc": "Handles product specs, quotes, and MOQs.",
        "agent_logistics_name": "Logistics Specialist",
        "agent_logistics_desc": "Handles shipping routes, tracking, and tariffs.",
        "agent_support_name": "Customer Care Agent",
        "agent_support_desc": "Handles warranties, refunds, and support.",
        "params": "📦 Fulfillment Params",
        "origin": "Origin",
        "destination": "Destination",
        "trade_term": "Trade Term",
        "origin_default": "Shenzhen, China",
        "dest_default": "Los Angeles, USA",
        "online": "Online",
        "welcome": "Hello! I am your **{role}**. How can I assist you today?",
        "chat_placeholder": "Ask about products, shipping, or support...",
        "api_error": "My apologies, I encountered a network issue. Please try again.",
        "calc_title": "📦 Quick Volumetric Weight Calculator",
        "map_title": "Live Cargo Fleet Tracking",
        "map_btn": "🚢 Refresh Fleet Positions",
        "fx_title": "Real-Time Exchange Rates",
        "comp_title": "Competitor Price Radar",
        "tabs": ["🚢 Vessel Tracking", "💱 FX Rates", "📊 Competitor Radar"]
    },
    "简体中文": {
        "nav_workspace": "🧭 工作区切换",
        "mod_front": "💬 AI 客服中枢 (前台)",
        "mod_back": "📈 市场情报大盘 (后台)",
        "lang_label": "🌐 全局语言设置",
        "dept_select": "🏢 部门选择",
        "agent_sales": "🛒 销售与采购",
        "agent_logistics": "🚢 物流与清关",
        "agent_support": "🔧 售后服务",
        "agent_sales_name": "资深销售专家",
        "agent_sales_desc": "处理产品规格、报价和起订量。",
        "agent_logistics_name": "国际物流专员",
        "agent_logistics_desc": "处理航线、货流追踪和体积重计算。",
        "agent_support_name": "售后服务专员",
        "agent_support_desc": "处理保修、退款和技术支持。",
        "params": "📦 履约与物流参数",
        "origin": "发货地 (Origin)",
        "destination": "目的地 (Destination)",
        "trade_term": "贸易条款 (Trade Term)",
        "origin_default": "中国 深圳",
        "dest_default": "美国 洛杉矶",
        "online": "在线",
        "welcome": "您好！我是您的专属 **{role}**，请问今天有什么我可以帮您的？",
        "chat_placeholder": "输入关于产品、报价、物流或售后的问题...",
        "api_error": "抱歉，遇到暂时的网络连接问题，请稍后再试。",
        "calc_title": "📦 体积重快速计算器 (内部工具)",
        "map_title": "全球货轮轨迹追踪 (精准定位)",
        "map_btn": "🚢 获取最新航线位置",
        "fx_title": "国际外汇实时盘口 (自动跳动)",
        "comp_title": "竞品价格实时雷达",
        "tabs": ["🚢 货轮追踪", "💱 实时汇率", "📊 竞品雷达"]
    },
    "Español": {
        "nav_workspace": "🧭 Espacio de trabajo",
        "mod_front": "💬 Centro de Agentes IA",
        "mod_back": "📈 Inteligencia de Mercado",
        "lang_label": "🌐 Idioma Global",
        "dept_select": "🏢 Departamento",
        "agent_sales": "🛒 Ventas y Compras",
        "agent_logistics": "🚢 Logística y Aduanas",
        "agent_support": "🔧 Servicio Postventa",
        "agent_sales_name": "Agente de Ventas Senior",
        "agent_sales_desc": "Maneja especificaciones y cotizaciones.",
        "agent_logistics_name": "Especialista en Logística",
        "agent_logistics_desc": "Maneja rutas de envío y aranceles.",
        "agent_support_name": "Agente de Atención",
        "agent_support_desc": "Maneja garantías y soporte.",
        "params": "📦 Parámetros de Envío",
        "origin": "Origen",
        "destination": "Destino",
        "trade_term": "Término Comercial",
        "origin_default": "Shenzhen, China",
        "dest_default": "Los Ángeles, EE.UU.",
        "online": "En línea",
        "welcome": "¡Hola! Soy su **{role}**. ¿En qué puedo ayudarle hoy?",
        "chat_placeholder": "Pregunte sobre productos, envíos o soporte...",
        "api_error": "Error de red. Inténtelo de nuevo.",
        "calc_title": "📦 Calculadora de Peso",
        "map_title": "Rastreo de Flota en Vivo",
        "map_btn": "🚢 Actualizar Posiciones",
        "fx_title": "Tipos de Cambio en Tiempo Real",
        "comp_title": "Radar de Precios de Competencia",
        "tabs": ["🚢 Rastreo de Buques", "💱 Tipos de Cambio", "📊 Radar de Precios"]
    },
    "Français": {
        "nav_workspace": "🧭 Espace de travail",
        "mod_front": "💬 Centre d'Agents IA",
        "mod_back": "📈 Intelligence de Marché",
        "lang_label": "🌐 Langue Globale",
        "dept_select": "🏢 Département",
        "agent_sales": "🛒 Ventes & Achats",
        "agent_logistics": "🚢 Logistique & Douanes",
        "agent_support": "🔧 Service Après-Vente",
        "agent_sales_name": "Agent de Ventes Senior",
        "agent_sales_desc": "Gère les spécifications et devis.",
        "agent_logistics_name": "Spécialiste Logistique",
        "agent_logistics_desc": "Gère l'expédition et les tarifs.",
        "agent_support_name": "Agent de Support",
        "agent_support_desc": "Gère les garanties et remboursements.",
        "params": "📦 Paramètres d'Expédition",
        "origin": "Origine",
        "destination": "Destination",
        "trade_term": "Terme Commercial",
        "origin_default": "Shenzhen, Chine",
        "dest_default": "Los Angeles, États-Unis",
        "online": "En ligne",
        "welcome": "Bonjour ! Je suis votre **{role}**. Comment puis-je vous aider ?",
        "chat_placeholder": "Posez vos questions sur les produits...",
        "api_error": "Désolé, problème de réseau.",
        "calc_title": "📦 Calculatrice de Poids",
        "map_title": "Suivi de la Flotte en Direct",
        "map_btn": "🚢 Actualiser les Positions",
        "fx_title": "Taux de Change en Temps Réel",
        "comp_title": "Radar des Prix Concurrents",
        "tabs": ["🚢 Suivi des Navires", "💱 Taux de Change", "📊 Radar des Prix"]
    },
    "日本語": {
        "nav_workspace": "🧭 ワークスペース",
        "mod_front": "💬 AI エージェントハブ",
        "mod_back": "📈 市場インテリジェンス",
        "lang_label": "🌐 グローバル言語",
        "dept_select": "🏢 部署選択",
        "agent_sales": "🛒 販売と調達",
        "agent_logistics": "🚢 物流と税関",
        "agent_support": "🔧 アフターサポート",
        "agent_sales_name": "シニアセールス",
        "agent_sales_desc": "製品仕様、見積もりを担当します。",
        "agent_logistics_name": "物流スペシャリスト",
        "agent_logistics_desc": "配送ルート、関税を担当します。",
        "agent_support_name": "カスタマーケア",
        "agent_support_desc": "保証、返金を担当します。",
        "params": "📦 配送パラメータ",
        "origin": "発送元",
        "destination": "目的地",
        "trade_term": "貿易条件",
        "origin_default": "中国 深セン",
        "dest_default": "米国 ロサンゼルス",
        "online": "オンライン",
        "welcome": "こんにちは！私はあなたの**{role}**です。ご用件をお伺いします。",
        "chat_placeholder": "製品、配送について質問する...",
        "api_error": "ネットワークエラーが発生しました。",
        "calc_title": "📦 容積重量計算ツール",
        "map_title": "ライブ貨物船追跡",
        "map_btn": "🚢 船団の位置を更新",
        "fx_title": "リアルタイム為替レート",
        "comp_title": "競合価格レーダー",
        "tabs": ["🚢 船舶追跡", "💱 為替レート", "📊 競合レーダー"]
    }
}

# --- 初始化全局语言状态 ---
if "app_lang" not in st.session_state:
    st.session_state.app_lang = "简体中文"

# --- 注入高级自定义 CSS ---
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #f7f9fc 0%, #e8f0f8 100%); }
    .trade-header { display: flex; align-items: center; padding: 1.5rem; background-color: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05); margin-bottom: 2rem; }
    .trade-header h1 { font-family: 'Inter', sans-serif; font-weight: 800; color: #1a202c; margin: 0; font-size: 2.2rem; }
    .trade-header span.brand { color: #0d6efd; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #edf2f7; }
    .agent-card { padding: 12px; border-radius: 8px; background-color: #f8f9fa; border-left: 4px solid #0d6efd; margin-bottom: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    [data-testid="stMetricDelta"] svg { width: 1.5rem; height: 1.5rem; }
</style>
""", unsafe_allow_html=True)

USER_AVATAR = "👤"

# ==========================================
# 顶级导航栏 & 干净利落的全局语言控制
# ==========================================
with st.sidebar:
    st.markdown("## 🌍 GlobalTrade")
    
    # 全局语言切换器：一点即切，干净利落
    lang_options = list(TRANSLATIONS.keys())
    current_lang_idx = lang_options.index(st.session_state.app_lang)
    new_lang = st.selectbox(TRANSLATIONS[st.session_state.app_lang]["lang_label"], lang_options, index=current_lang_idx)
    
    if new_lang != st.session_state.app_lang:
        st.session_state.app_lang = new_lang
        st.rerun() # 立即刷新全局应用新语言
        
    t = TRANSLATIONS[st.session_state.app_lang]
    
    st.divider()
    st.markdown(f"## {t['nav_workspace']}")
    
    app_mode = st.radio(
        "Module:", 
        [t["mod_front"], t["mod_back"]], 
        label_visibility="collapsed"
    )
    st.divider()

# ==========================================
# 模块 B：全球市场情报 Dashboard (专业后台)
# ==========================================
if app_mode == t["mod_back"]:
    st.markdown(f"""
    <div class="trade-header">
        <div style="font-size: 3rem; margin-right: 20px;">📊</div>
        <h1>Global Market <span class="brand">Intelligence</span></h1>
    </div>
    """, unsafe_allow_html=True)
    
    # 初始化静态与动态数据
    if "map_data" not in st.session_state:
        np.random.seed(42)
        # 生成初始的经纬度数据
        map_base = pd.DataFrame(np.random.randn(60, 2) / [2, 2] + [22.5, -150.0], columns=['lat', 'lon'])
        map_base = pd.concat([map_base, pd.DataFrame(np.random.randn(30, 2) / [5, 5] + [34.0, -118.0], columns=['lat', 'lon'])])
        map_base = pd.concat([map_base, pd.DataFrame(np.random.randn(30, 2) / [5, 5] + [22.5, 114.0], columns=['lat', 'lon'])])
        st.session_state.map_data = map_base
        
        st.session_state.fx_cny = 7.2341
        st.session_state.fx_eur = 1.0852
        st.session_state.fx_gbp = 1.2640

    tab1, tab2, tab3 = st.tabs(t["tabs"])
    
    with tab1:
        c1, c2 = st.columns([3, 1])
        c1.subheader(t["map_title"])
        
        # 【功能2：点按钮才刷新轨迹】位置不会自动跳动
        if c2.button(t["map_btn"], use_container_width=True):
            st.session_state.map_data['lat'] += np.random.uniform(-1.0, 1.0, len(st.session_state.map_data))
            st.session_state.map_data['lon'] += np.random.uniform(-1.0, 1.0, len(st.session_state.map_data))
            
        # 【完美回归原生图表】使用最稳定、保证能显示的 st.map，配合我们自己管理的 session_state 数据
        st.map(st.session_state.map_data, zoom=2, use_container_width=True)

    with tab2:
        # 【功能3：利用 st.fragment 实现局部盘口自己跳动】
        if hasattr(st, "fragment"):
            @st.fragment(run_every=2)
            def auto_refresh_fx():
                st.subheader(t["fx_title"])
                st.session_state.fx_cny += np.random.uniform(-0.0020, 0.0020)
                st.session_state.fx_eur += np.random.uniform(-0.0005, 0.0005)
                st.session_state.fx_gbp += np.random.uniform(-0.0008, 0.0008)
                
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("USD / CNY", f"{st.session_state.fx_cny:.4f}", f"{np.random.uniform(-0.01, 0.01):.4f}", delta_color="inverse")
                m2.metric("EUR / USD", f"{st.session_state.fx_eur:.4f}", f"{np.random.uniform(-0.005, 0.005):.4f}")
                m3.metric("GBP / USD", f"{st.session_state.fx_gbp:.4f}", f"{np.random.uniform(-0.005, 0.005):.4f}")
                m4.metric("USD / JPY", "151.20", "+0.45", delta_color="inverse")
                
                st.line_chart(pd.DataFrame(np.random.randn(10, 1) * 0.05 + st.session_state.fx_cny, columns=['USD/CNY Trend']))
            
            auto_refresh_fx()
        else:
            st.warning("⚠️ 您的 Streamlit 版本低于 1.37，请运行 `pip install --upgrade streamlit` 以支持盘口自动刷新。")

    with tab3:
        st.subheader(t["comp_title"])
        df = pd.DataFrame({
            "Platform": ["Amazon", "Alibaba", "Shopee", "AliExpress", "Temu"],
            "Price (USD)": [29.99 + np.random.uniform(-1, 1), 12.50, 18.00, 15.99, 10.99],
            "Stock Status": ["In Stock", "High", "Low", "In Stock", "High"]
        })
        st.dataframe(df, use_container_width=True)
        st.bar_chart(pd.DataFrame({"Price (USD)": df["Price (USD)"].values}, index=df["Platform"]))

# ==========================================
# 模块 A：AI Agent Hub (专业前台)
# ==========================================
elif app_mode == t["mod_front"]:
    
    with st.sidebar:
        st.markdown(f"### {t['dept_select']}")
        
        agent_keys = ["sales", "logistics", "support"]
        agent_options = {
            "sales": t["agent_sales"],
            "logistics": t["agent_logistics"],
            "support": t["agent_support"]
        }
        
        selected_agent_key = st.radio("Agent:", options=agent_keys, format_func=lambda x: agent_options[x], label_visibility="collapsed")
        
        agent_name = t[f"agent_{selected_agent_key}_name"]
        agent_desc = t[f"agent_{selected_agent_key}_desc"]
        
        prompts = {
            "sales": "You are the Sales & Sourcing Expert. Focus on product details, closing deals, and negotiating MOQs.",
            "logistics": "You are the Logistics & Customs Expert. Focus on shipping times, freight costs. Know the Volumetric Weight formula: (Length x Width x Height in cm) / 5000.",
            "support": "You are the After-Sales Support Expert. Focus on empathy, solving product issues, handling claims."
        }
        avatars = {"sales": "🛒", "logistics": "🚢", "support": "🔧"}
        
        st.markdown(f"""
        <div class="agent-card">
            <strong>🟢 {agent_name} ({t['online']})</strong><br>
            <span style="font-size: 0.85em; color: #6c757d;">{agent_desc}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        st.markdown(f"#### {t['params']}")
        origin_val = st.text_input(t["origin"], value=t["origin_default"])
        destination_val = st.text_input(t["destination"], value=t["dest_default"]) 
        term_val = st.text_input(t["trade_term"], value="FOB")

    if "active_agent_key" not in st.session_state:
        st.session_state.active_agent_key = selected_agent_key

    if st.session_state.active_agent_key != selected_agent_key:
        st.session_state.active_agent_key = selected_agent_key
        st.session_state.messages = [] 
        st.rerun() 

    DYNAMIC_SYSTEM_PROMPT = f"""
    {prompts[selected_agent_key]}
    Company Logistics Parameters:
    - Origin: {origin_val}
    - Destination: {destination_val}
    - Trade Term: {term_val}
    - Interface Language: {st.session_state.app_lang} (You MUST reply perfectly in this language).
    """

    st.markdown(f"""
    <div class="trade-header">
        <div style="font-size: 3rem; margin-right: 20px;">{avatars[selected_agent_key]}</div>
        <h1>GlobalTrade <span class="brand">{agent_name}</span></h1>
    </div>
    """, unsafe_allow_html=True)

    try:
        client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
    except KeyError:
        st.error("🚨 密钥未找到！请检查 `.streamlit/secrets.toml` 文件。")
        st.stop()

    if "messages" not in st.session_state or len(st.session_state.messages) == 0:
        st.session_state.messages = [{"role": "system", "content": DYNAMIC_SYSTEM_PROMPT}]

    if len(st.session_state.messages) == 1: 
        with st.chat_message("assistant", avatar=avatars[selected_agent_key]):
            st.markdown(t["welcome"].format(role=agent_name))
            
            if selected_agent_key == "logistics":
                with st.expander(t["calc_title"]):
                    c1, c2, c3 = st.columns(3)
                    l = c1.number_input("L (cm)", value=50)
                    w = c2.number_input("W (cm)", value=40)
                    h = c3.number_input("H (cm)", value=30)
                    st.info(f"**Volumetric Weight:** {(l * w * h) / 5000} kg")

    for msg in st.session_state.messages:
        if msg["role"] != "system":
            avatar = avatars[selected_agent_key] if msg["role"] == "assistant" else USER_AVATAR
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

    if user_input := st.chat_input(t["chat_placeholder"]):
        st.session_state.messages[0]["content"] = DYNAMIC_SYSTEM_PROMPT
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar=avatars[selected_agent_key]):
            message_placeholder = st.empty()
            full_response = ""
            try:
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=st.session_state.messages,
                    stream=True
                )
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            except Exception as e:
                st.error(f"API Error: {e}")
                message_placeholder.markdown(t["api_error"])
                
        st.session_state.messages.append({"role": "assistant", "content": full_response})