import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# KONFIGURASI & TEMA WARNA
# ==========================================
st.set_page_config(page_title="E-Commerce Dashboard", page_icon="🛍️", layout="wide")

# Palet seragam: satu warna netral + satu warna sorotan (maksimal dua warna).
# Warna tidak lagi dipakai untuk membedakan kategori (sudah diwakili sumbu),
# melainkan hanya untuk menyoroti nilai tertinggi.
NEUTRAL_COLOR = "#94A3B8"    # Slate-400 : bar biasa
HIGHLIGHT_COLOR = "#EF4444"  # Red-500   : sorotan nilai ekstrem
GRID_COLOR = "#E2E8F0"
SEGMENT_ORDER = ["Low", "Mid", "High", "VIP"]


# ==========================================
# LOAD DATA
# ==========================================
@st.cache_data
def load_data():
    df_main = pd.read_csv("main_data.csv")
    df_rfm = pd.read_csv("rfm_data.csv")

    # Konversi tipe data tanggal
    df_main["order_purchase_timestamp"] = pd.to_datetime(df_main["order_purchase_timestamp"])

    # Buang baris RFM tanpa segmen agar agregasi tidak menghasilkan grup NaN
    df_rfm = df_rfm.dropna(subset=["Segment"]).copy()

    return df_main, df_rfm


main_df, rfm_df = load_data()

min_date = main_df["order_purchase_timestamp"].min().date()
max_date = main_df["order_purchase_timestamp"].max().date()
available_years = sorted(main_df["order_purchase_timestamp"].dt.year.unique().tolist())
available_categories = sorted(main_df["product_category_name"].dropna().unique().tolist())
available_segments = [segment for segment in SEGMENT_ORDER if segment in set(rfm_df["Segment"])]


# ==========================================
# HELPER
# ==========================================
def resolve_selection(selected, available):
    """Opsi 'All' (atau kosong) berarti semua nilai tersedia dipakai."""
    if not selected or "All" in selected:
        return list(available)
    return [item for item in selected if item in available]


def filter_by_date(df, start_date, end_date):
    """Saring df berdasarkan rentang tanggal. Lempar ValueError bila tidak valid."""
    if start_date is None or end_date is None:
        raise ValueError("Start Date dan End Date belum lengkap.")
    if start_date > end_date:
        raise ValueError("Start Date tidak boleh lebih besar daripada End Date.")
    mask = (df["order_purchase_timestamp"].dt.date >= start_date) & (
        df["order_purchase_timestamp"].dt.date <= end_date
    )
    return df.loc[mask]


def style_figure(fig, title, x_title, y_title, grid_axis="x", height=460):
    """Terapkan gaya visual yang konsisten ke seluruh grafik Plotly."""
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        xaxis_title=x_title,
        yaxis_title=y_title,
        height=height,
        margin=dict(l=10, r=20, t=60, b=10),
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
    )
    if grid_axis == "x":
        fig.update_xaxes(showgrid=True, gridcolor=GRID_COLOR, zeroline=False)
        fig.update_yaxes(showgrid=False)
    else:
        fig.update_yaxes(showgrid=True, gridcolor=GRID_COLOR, zeroline=False)
        fig.update_xaxes(showgrid=False)
    return fig


# ==========================================
# SIDEBAR FILTER
# ==========================================
st.sidebar.image("https://img.icons8.com/color/96/000000/shop.png", width=96)
st.sidebar.title("Filter Data")
st.sidebar.markdown("Gunakan filter di bawah ini untuk mengeksplorasi data.")

# --- Filter rentang tanggal (dengan penanganan error) ---
st.sidebar.markdown("**Rentang Tanggal**")
date_col1, date_col2 = st.sidebar.columns(2)
start_date = date_col1.date_input(
    "Start Date",
    value=None,
    min_value=min_date,
    max_value=max_date,
    format="DD/MM/YYYY",
)
end_date = date_col2.date_input(
    "End Date",
    value=None,
    min_value=min_date,
    max_value=max_date,
    format="DD/MM/YYYY",
)

# --- Filter tahun (multiselect + opsi "All") ---
year_options = ["All"] + [str(year) for year in available_years]
selected_years = st.sidebar.multiselect(
    "Tahun Analisis",
    options=year_options,
    default=["All"],
)

category_options = ["All"] + available_categories
selected_categories = st.sidebar.multiselect(
    "Kategori Produk",
    options=category_options,
    default=["All"],
)

# --- Filter lain: segmen RFM & jumlah kategori ---
segment_options = ["All"] + available_segments
selected_segments = st.sidebar.multiselect(
    "Segmen Pelanggan (RFM)",
    options=segment_options,
    default=["All"],
)

top_n = st.sidebar.slider(
    "Jumlah Kategori Ditampilkan (Top N)",
    min_value=5,
    max_value=20,
    value=10,
    step=1,
)

# Terapkan filter non-tanggal
df_filtered = main_df.copy()
active_years = [int(year) for year in resolve_selection(selected_years, year_options[1:])]
df_filtered = df_filtered[df_filtered["order_purchase_timestamp"].dt.year.isin(active_years)]
df_filtered = df_filtered[
    df_filtered["product_category_name"].isin(resolve_selection(selected_categories, available_categories))
]

# Terapkan filter tanggal dengan try-except agar dashboard tetap berjalan
date_warning = None
try:
    df_filtered = filter_by_date(df_filtered, start_date, end_date)
except ValueError as err:
    date_warning = f"⚠️ {err} Menampilkan seluruh rentang data yang tersedia."
except Exception as err:  # jaring pengaman terakhir
    date_warning = f"⚠️ Terjadi kesalahan pada filter tanggal: {err}. Menampilkan seluruh rentang data."

if date_warning:
    st.warning(date_warning)

# Ringkasan filter aktif
active_year_label = "Semua Tahun" if "All" in selected_years or not selected_years else ", ".join(str(y) for y in selected_years)
active_cat_label = "Semua Kategori" if "All" in selected_categories or not selected_categories else f"{len(selected_categories)} kategori terpilih"
if start_date and end_date:
    date_label = f"{start_date:%d/%m/%Y} – {end_date:%d/%m/%Y}"
else:
    date_label = f"{min_date:%d/%m/%Y} – {max_date:%d/%m/%Y} (default)"

# ==========================================
# HEADER UTAMA
# ==========================================
st.title("🛍️ E-Commerce Public Data Dashboard")
st.markdown(
    "Dashboard ini menyajikan hasil analisis **Waktu Pengiriman vs Kepuasan Pelanggan** "
    "serta **Segmentasi Pelanggan (RFM)**."
)
st.caption(f"Filter aktif — Tahun: {active_year_label} | Kategori: {active_cat_label} | Tanggal: {date_label}")

st.markdown("---")

# ==========================================
# BAGIAN 1: PERTANYAAN 1
# ==========================================
st.subheader("1. Analisis Waktu Pengiriman & Kepuasan Pelanggan")
st.markdown(
    f"Menampilkan **{top_n} kategori produk** dengan waktu pengiriman terlama pada rentang filter terpilih. "
    f"Kartu metrik di bawah merangkum data dari **{top_n} kategori** yang tampil di grafik batang, "
    "bukan seluruh data. Arahkan kursor ke batang untuk melihat detail, gunakan scroll untuk zoom, "
    "dan seret untuk memilih data."
)

if df_filtered.empty:
    st.warning("Tidak ada data yang cocok dengan filter yang dipilih. Silakan sesuaikan filter di sidebar.")
else:
    cat_analysis = (
        df_filtered.groupby("product_category_name")
        .agg(
            delivery_days=("delivery_days", "mean"),
            review_score=("review_score", "mean"),
            total_orders=("order_purchase_timestamp", "count"),
        )
        .reset_index()
    )

    top_categories = (
        cat_analysis.sort_values(by="delivery_days", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    # DataFrame yang hanya memuat kategori pada grafik batang (Top N)
    df_top_categories = df_filtered[
        df_filtered["product_category_name"].isin(top_categories["product_category_name"])
    ]

    # Ringkasan metrik dihitung dari Top N kategori yang ditampilkan
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Rata-rata Waktu Kirim", f"{df_top_categories['delivery_days'].mean():.1f} hari")
    metric_col2.metric("Rata-rata Review Score", f"{df_top_categories['review_score'].mean():.2f} / 5")
    metric_col3.metric("Total Pesanan", f"{len(df_top_categories):,}")

    # Urutkan terbalik agar kategori terlama muncul di paling atas
    plot_df = top_categories.iloc[::-1].reset_index(drop=True)
    longest_category = top_categories.iloc[0]["product_category_name"]
    bar_colors = [
        HIGHLIGHT_COLOR if name == longest_category else NEUTRAL_COLOR
        for name in plot_df["product_category_name"]
    ]

    fig1 = go.Figure(
        go.Bar(
            x=plot_df["delivery_days"],
            y=plot_df["product_category_name"],
            orientation="h",
            marker=dict(color=bar_colors),
            customdata=plot_df[["review_score", "total_orders"]].to_numpy(dtype=float),
            text=plot_df.apply(
                lambda row: f"⭐{row['review_score']:.1f} · {int(row['total_orders']):,}", axis=1
            ),
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Rata-rata waktu kirim: %{x:.1f} hari<br>"
                "Review score: %{customdata[0]:.2f}<br>"
                "Total pesanan: %{customdata[1]:,.0f}<extra></extra>"
            ),
        )
    )
    style_figure(
        fig1,
        f"{top_n} Kategori dengan Waktu Pengiriman Terlama",
        "Rata-rata Waktu Pengiriman (Hari)",
        "Kategori Produk",
        grid_axis="x",
        height=max(420, 40 * top_n + 120),
    )
    fig1.update_xaxes(range=[0, plot_df["delivery_days"].max() * 1.45])
    st.plotly_chart(fig1, width="stretch")

    st.info(
        "💡 **Insight:** Terdapat korelasi negatif antara waktu pengiriman dan review score. "
        "Kategori dengan waktu kirim paling lama (disorot merah) cenderung memiliki review score rendah. "
        "(Catatan: kategori dengan total pesanan sangat sedikit tidak representatif untuk dijadikan acuan.)"
    )

st.markdown("---")

# ==========================================
# BAGIAN 2: PERTANYAAN 2 (RFM)
# ==========================================
st.subheader("2. Segmentasi Pelanggan Berdasarkan RFM (2016-2018)")
st.markdown(
    "Analisis RFM (Recency, Frequency, Monetary) membagi pelanggan ke dalam 4 segmen: "
    "Low, Mid, High, dan VIP. Batang dengan nilai tertinggi pada tiap grafik disorot."
)

active_segments = resolve_selection(selected_segments, available_segments)
rfm_clean = rfm_df[rfm_df["Segment"].isin(active_segments)].copy()
present_segments = [segment for segment in SEGMENT_ORDER if segment in set(rfm_clean["Segment"])]

if not present_segments:
    st.warning("Tidak ada data segmen yang cocok dengan filter yang dipilih.")
else:
    rfm_summary = (
        rfm_clean.groupby("Segment")
        .agg(
            total_customers=("customer_unique_id", "count"),
            total_monetary=("Monetary", "sum"),
        )
        .reindex(present_segments)
        .reset_index()
    )

    col1, col2 = st.columns(2)

    with col1:
        max_customers = rfm_summary["total_customers"].max()
        fig2 = go.Figure(
            go.Bar(
                x=rfm_summary["Segment"],
                y=rfm_summary["total_customers"],
                marker=dict(
                    color=[
                        HIGHLIGHT_COLOR if value == max_customers else NEUTRAL_COLOR
                        for value in rfm_summary["total_customers"]
                    ]
                ),
                text=rfm_summary["total_customers"],
                textposition="outside",
                cliponaxis=False,
                hovertemplate="<b>%{x}</b><br>Jumlah pelanggan: %{y:,}<extra></extra>",
            )
        )
        style_figure(
            fig2,
            "Jumlah Pelanggan per Segmen",
            "Segmen Pelanggan",
            "Jumlah Pelanggan",
            grid_axis="y",
        )
        fig2.update_yaxes(range=[0, max_customers * 1.2])
        st.plotly_chart(fig2, width="stretch")

    with col2:
        max_monetary = rfm_summary["total_monetary"].max()
        fig3 = go.Figure(
            go.Bar(
                x=rfm_summary["Segment"],
                y=rfm_summary["total_monetary"],
                marker=dict(
                    color=[
                        HIGHLIGHT_COLOR if value == max_monetary else NEUTRAL_COLOR
                        for value in rfm_summary["total_monetary"]
                    ]
                ),
                text=rfm_summary["total_monetary"].map(lambda value: f"{value:,.0f}"),
                textposition="outside",
                cliponaxis=False,
                customdata=rfm_summary["total_monetary"],
                hovertemplate="<b>%{x}</b><br>Total revenue: R$ %{customdata:,.2f}<extra></extra>",
            )
        )
        style_figure(
            fig3,
            "Total Revenue per Segmen",
            "Segmen Pelanggan",
            "Total Revenue (R$)",
            grid_axis="y",
        )
        fig3.update_yaxes(range=[0, max_monetary * 1.2])
        st.plotly_chart(fig3, width="stretch")

    st.info(
        "💡 **Insight:** Pelanggan segmen **Mid** dan **High** memberikan kontribusi pendapatan "
        "terbesar. Segmen **VIP** jumlahnya sangat sedikit, namun memiliki nilai transaksi yang "
        "sangat tinggi. Perusahaan harus fokus pada strategi retensi untuk segmen Mid, High, dan VIP."
    )

st.markdown("---")
st.caption("Copyright © 2026 | Proyek Analisis Data: E-Commerce Public Dataset")
