from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components
import src.charts as charts
from src.utils import thousand_sep, dateformat, tested_percent, fetch_metadata


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)


def hide_menu():
    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)


def main():
    st.markdown(
        """
        <div class="siteTitle">c19norge.no</div>
        <div class="siteSubTitle">
            <i class="fa fa-twitter" aria-hidden="true" style="color:#1DA1F2"></i>
            <a href="https://twitter.com/covid19norge">@covid19norge</a>
            &emsp;
            <i class="fa fa-telegram" aria-hidden="true" style="color:#1DA1F2"></i>
            <a href="https://t.me/covid19norge">@covid19norge</a>
        </div>
        <div class="siteBorder"></div>
        """,
        unsafe_allow_html=True,
    )

    # metadata
    tested = fetch_metadata("tested")
    confirmed = fetch_metadata("confirmed")
    dead = fetch_metadata("dead")
    admissions = fetch_metadata("admissions")
    respiratory = fetch_metadata("respiratory")
    tested_pct_w1 = tested_percent()[0]
    tested_pct_w2 = tested_percent()[1]

    # totals
    tested_total = thousand_sep(tested.get("total"))
    confirmed_total = thousand_sep(confirmed.get("total", "-"))
    dead_total = thousand_sep(dead.get("total", "-"))
    admissions_total = thousand_sep(admissions.get("total", "-"))
    respiratory_total = thousand_sep(respiratory.get("total", "-"))

    # newToday
    tested_newToday = thousand_sep(tested.get("newToday", 0))
    confirmed_newToday = thousand_sep(confirmed.get("newToday", 0))
    dead_newToday = thousand_sep(dead.get("newToday", 0))
    admissions_newToday = admissions.get("changeToday", 0)
    respiratory_newToday = respiratory.get("changeToday", 0)

    # newYesterday
    tested_newYesterday = thousand_sep(tested.get("newYesterday", 0))
    confirmed_newYesterday = thousand_sep(confirmed.get("newYesterday", 0))
    dead_newYesterday = thousand_sep(dead.get("newYesterday", 0))
    admissions_newYesterday = admissions.get("newYesterday", 0)
    respiratory_newYesterday = respiratory.get("newYesterday", 0)

    if admissions_newToday > 0:
        admissions_newToday = f"+{admissions_newToday}"
    if respiratory_newToday > 0:
        respiratory_newToday = f"+{respiratory_newToday}"
    if admissions_newYesterday > 0:
        admissions_newYesterday = f"+{admissions_newYesterday}"
    if respiratory_newYesterday > 0:
        respiratory_newYesterday = f"+{respiratory_newYesterday}"

    # updated
    tested_updated = dateformat(tested.get("updated", {}).get("timestamp"))
    confirmed_updated = dateformat(confirmed.get("updated", {}).get("timestamp"))
    dead_updated = dateformat(dead.get("updated", {}).get("timestamp"))
    admissions_updated = dateformat(admissions.get("updated", {}).get("timestamp"))
    respiratory_updated = dateformat(respiratory.get("updated", {}).get("timestamp"))
    tested_pct_updated = tested_percent()[2]

    confirmed, dead, admissions, respiratory = st.beta_columns(4)
    tested, tested_pct = st.beta_columns(2)

    if datetime.now().hour in range(0, 11):
        desc = "Nye i går"
        desc_hospitalized = "Endring i går"
        tested_new = tested_newYesterday
        confirmed_new = confirmed_newYesterday
        dead_new = dead_newYesterday
        admissions_new = admissions_newYesterday
        respiratory_new = respiratory_newYesterday
    else:
        desc = "Nye i dag"
        desc_hospitalized = "Endring i dag"
        tested_new = tested_newToday
        confirmed_new = confirmed_newToday
        dead_new = dead_newToday
        admissions_new = admissions_newToday
        respiratory_new = respiratory_newToday

    # infoboxes
    with confirmed:
        st.markdown(
            f"""
        <div class="cardContainer">
            <div class="cardHeader cardConfirmed">Smittet</div>
            <div class="motherNumber">{confirmed_total}</div>
            <div class="smallerNumber">{confirmed_new}</div>
            <div class="cardFooterText">{desc}</div>
        </div>
        <div class="cardUpdated">{confirmed_updated}</div>
        """,
            unsafe_allow_html=True,
        )

    with dead:
        st.markdown(
            f"""
        <div class="cardContainer">
            <div class="cardHeader cardDead">Døde</div>
            <div class="motherNumber">{dead_total}</div>
            <div class="smallerNumber">{dead_new}</div>
            <div class="cardFooterText">{desc}<br></div>
        </div>
        <div class="cardUpdated">{dead_updated}</div>
        """,
            unsafe_allow_html=True,
        )

    with tested:
        st.markdown(
            f"""
        <div class="cardContainer">
            <div class="cardHeader cardTested">Testet</div>
            <div class="motherNumber">{tested_total}</div>
            <div class="smallerNumber">{tested_new}</div>
            <div class="cardFooterText">{desc}</div>
        </div>
        <div class="cardUpdated">{tested_updated}</div>
        """,
            unsafe_allow_html=True,
        )

    with admissions:
        st.markdown(
            f"""
        <div class="cardContainer">
            <div class="cardHeader cardAdmissions">Innlagte</div>
            <div class="motherNumber">{admissions_total}</div>
            <div class="smallerNumber">{admissions_new}</div>
            <div class="cardFooterText">{desc_hospitalized}</div>
        </div>
        <div class="cardUpdated">{admissions_updated}</div>
        """,
            unsafe_allow_html=True,
        )

    with respiratory:
        st.markdown(
            f"""
        <div class="cardContainer">
            <div class="cardHeader cardRespiratory">Respirator</div>
            <div class="motherNumber">{respiratory_total}</div>
            <div class="smallerNumber">{respiratory_new}</div>
            <div class="cardFooterText">{desc_hospitalized}</div>
        </div>
        <div class="cardUpdated">{respiratory_updated}</div>
        """,
            unsafe_allow_html=True,
        )

    with tested_pct:
        st.markdown(
            f"""
        <div class="cardContainer">
            <div class="cardHeader cardTestedPos">Positive tester siste uke</div>
            <div class="motherNumber">{tested_pct_w1} %</div>
            <div class="smallerNumber">{tested_pct_w2} %</div>
            <div class="cardFooterText">Foregående uke</div>
        </div>
        <div class="cardUpdated">{tested_pct_updated}</div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("___")

    # graphs
    period, category = st.beta_columns(2)

    PERIODS = {
        "Hele perioden": 0,
        "Siste 30 dager": 30,
        "Siste 14 dager": 14,
    }

    with category:
        cummulative = st.selectbox("", ["Nye per dag", "Total"])
    with period:
        selection = st.selectbox("", list(PERIODS.keys()))

    st.header("Smittet")
    st.altair_chart(
        charts.confirmed(cummulative, PERIODS[selection]), use_container_width=True
    )

    st.header("Døde")
    st.altair_chart(
        charts.dead(cummulative, PERIODS[selection]), use_container_width=True
    )

    st.header("Testet")
    st.altair_chart(
        charts.tested(cummulative, PERIODS[selection]), use_container_width=True
    )

    st.header("Sykehusinnleggelser")
    st.altair_chart(charts.hospitalized(PERIODS[selection]), use_container_width=True)

    # data sources
    with st.beta_expander("Datakilder"):
        with open("static/html/sources.html") as f:
            data = f.read()
            components.html(data, height=700)

    # footer
    st.markdown("")
    st.markdown("Laget av [Fredrik Haarstad](https://github.com/frefrik/)")


if __name__ == "__main__":
    st.set_page_config(
        page_title="c19norge.no",
        page_icon="static/img/coronavirus.png",
        initial_sidebar_state="collapsed",
    )

    local_css("static/css/style.css")
    remote_css(
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
    )
    hide_menu()
    main()
