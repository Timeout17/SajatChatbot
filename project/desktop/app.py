import streamlit as st
import requests

# 1. Beállítjuk a közös memóriát (Session State), hogy a Streamlit ne felejtsen el semmit
if "user_id" not in st.session_state:
    st.session_state.user_id = None  # Alapból senki sincs bejelentkezve

if "chat_id" not in st.session_state:
    st.session_state.chat_id = None  # Alapból nincs aktív chat szoba

if "oldal" not in st.session_state:
    st.session_state.oldal = "login"  # Alapból a login oldalt mutatjuk

# 2. Logikai kapu: eldöntjük, melyik felületet rajzoljuk ki
if st.session_state.user_id is None:
    # Ha nincs bejelentkezve senki
    if st.session_state.oldal == "login":
        st.subheader("🔑 Bejelentkezés a RAG Rendszerbe")
                
        # Kirakjuk a két szövegdobozt a képernyőre
        username = st.text_input("Felhasználónév:")
        password = st.text_input("Jelszó:", type="password")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Bejelentkezés", type="primary"):
                if username and password:
                    try:
                        url = "http://localhost:8000/Login"
                                
                        # Szötárba rakjuk a paramétereket az URL-kódolás miatt
                        adatok = {
                            "username": username,
                            "password": password
                        }
                                
                        # Elküldjük a kérést params-ként
                        response = requests.post(url, params=adatok)
                                
                        if response.status_code == 200:
                            adat = response.json()
                                    
                            # Ellenőrizzük, mit küldött a backend
                            if adat.get("user_id"):
                                st.session_state.user_id = adat["user_id"]
                                st.success("Sikeresen bejelentkeztél!")
                                st.rerun() 
                            else:
                                hiba_reszlet = adat.get("detail", "Hibás felhasználónév vagy jelszó!")
                                st.error(hiba_reszlet)
                        else:
                            st.error(f"Szerver hiba! Kód: {response.status_code}")
                    except Exception as e:
                        st.error(f"Nem érhető el a backend: {str(e)}")
                else:
                    st.warning("Töltsd ki mind a két mezőt!")
            
        with col2:
            if st.button("Nincs még fiókom (Regisztráció)"):
                st.session_state.oldal = "register"
                st.rerun()
        
    elif st.session_state.oldal == "register":
        st.subheader("📝 Fiók Regisztráció")
        
        username = st.text_input("Felhasználónév:")
        firstname = st.text_input("Keresztnév:")
        lastname = st.text_input("Vezetéknév:")
        email = st.text_input("Email címed:")
        password = st.text_input("Jelszó:", type="password")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Regisztráció indítása", type="primary"):
                if username and firstname and lastname and email and password:
                    try:
                        url = "http://localhost:8000/registration"
                        
                        adatok = {
                            "username": username,
                            "firstname": firstname,
                            "lastname": lastname,
                            "email": email,
                            "password": password
                        }
                        
                        response = requests.post(url, params=adatok)
                        
                        if response.status_code == 200:
                            adat = response.json()
                            if adat.get("status") == "sikeres regisztráció":
                                st.success("Sikeres regisztráció! Most már bejelentkezhetsz.")
                                st.session_state.oldal = "login"
                                st.rerun()
                            else:
                                st.error(adat.get("status"))
                        else:
                            st.error(f"Szerver hiba! Kód: {response.status_code}")
                    except Exception as e:
                        st.error(f"A backend nem elérhető: {str(e)}")
                else:
                    st.warning("Minden mezőt kötelező kitölteni!")
                    
        with col2:
            if st.button("Mégis inkább bejelentkezek"):
                st.session_state.oldal = "login"
                st.rerun()

else:
    # --- EZ A FŐ CHAT FELÜLET (SIKERES LOGIN UTÁN) ---
    
    # 1. ELKÉSZÍTJÜK A BAL OLDALI SÁVOT (SIDEBAR) WITH ADATBÁZIS INTEGRÁCIÓ
    with st.sidebar: 
        st.subheader("💬 Beszélgetések")
        
        # --- ÚJ CHAT INDÍTÁSA DINAMIKUSAN ---
        if st.button("➕ Új beszélgetés indítása", use_container_width=True):
            try:
                url = f"http://localhost:8000/new_chat?user_id={st.session_state.user_id}"
                response = requests.post(url)
                
                if response.status_code == 200:
                    adat = response.json()
                    st.session_state.chat_id = adat.get("chat_id")
                    st.success(f"Új szoba megnyitva! ID: {st.session_state.chat_id}")
                    st.rerun()
                else:
                    st.error("Nem sikerült új szobát létrehozni.")
            except Exception as e:
                st.error(f"A backend nem elérhető: {str(e)}")
            
        st.divider()
        st.write("Korábbi chatek:")
        
        # --- KORÁBBI CHATEK LEKÉRDEZÉSE AZ SQL-BŐL ---
        try:
            url = f"http://localhost:8000/get_user_chats?user_id={st.session_state.user_id}"
            response = requests.get(url)
            
            if response.status_code == 200:
                chat_lista = response.json()
                
                if not chat_lista:
                    st.caption("Még nincsenek beszélgetéseid.")
                
                for chat in chat_lista:
                    c_id = chat.get("id")  # Átírtuk chat_id-ról id-ra!
                    c_title = chat.get("title", "Nincs cím")
                    
                    if c_id is not None:
                        if st.button(f"📂 {c_title} (ID: {c_id})", use_container_width=True, key=f"chat_btn_{c_id}"):
                            st.session_state.chat_id = c_id
                            st.rerun()
            else:
                st.error("Nem sikerült betölteni a szobákat.")
        except Exception as e:
            st.error(f"Hiba a szobák lekérésekor: {str(e)}")
            
        st.divider()
        if st.button("🚪 Kijelentkezés", type="secondary", use_container_width=True):
            st.session_state.user_id = None
            st.session_state.chat_id = None
            st.session_state.oldal = "login"
            st.rerun()

    # 2. EZ A FŐ KÉPERNYŐ (JOBB OLDAL)
    st.title("🤖 Vállalati RAG Asszisztens")
    st.write(f"Üdvözlünk! Felhasználó ID: `{st.session_state.user_id}` | Aktív Chat ID: `{st.session_state.chat_id}`")
    
    if st.session_state.chat_id is None:
        st.info("👈 Válassz egy beszélgetést a bal oldali sávban az indításhoz!")
    else:
        st.subheader("📝 Kérdezz a dokumentumokból:")
        
        user_prompt = st.text_input("Írd ide a kérdésed a könyvből (pl. Statistical Learning):", key="chat_input")
        
        if st.button("Küldés az AI Agentnek", type="primary"):
            if user_prompt:
                with st.spinner("A Llama-3.3 éppen a ChromaDB-ben kutat... 🧠"):
                    try:
                        url = "http://localhost:8000/query"
                        
                        # Összerakjuk a teljes JSON törzset a Pydantic Message modellnek
                        csomag = {
                            "user_id": st.session_state.user_id,
                            "chat_id": st.session_state.chat_id,
                            "prompt": user_prompt
                        }
                        
                        response = requests.post(url, json=csomag)
                        
                        if response.status_code == 200:
                            adat = response.json()
                            ai_valasz = adat.get("result", "Nincs válasz.")
                            
                            st.markdown("### 🤖 Az AI Agent válasza:")
                            st.info(ai_valasz)
                        else:
                            st.error(f"Szerver hiba! Kód: {response.status_code}")
                    except Exception as e:
                        st.error(f"A backend nem elérhető: {str(e)}")
            else:
                st.warning("Írj be egy kérdést!")
