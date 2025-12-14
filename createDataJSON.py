import pandas

df = pandas.read_excel(
    'KSK Le Loi 2025.xlsx',
    sheet_name=0,
    usecols="B:R",
    skiprows=2,
    header=None,
    dtype=str
)

header_df = pandas.read_excel(
    'KSK Le Loi 2025.xlsx',
    sheet_name=0,
    usecols="B:R",
    nrows=2,
    header=None
)

header_df.iloc[0] = header_df.iloc[0].ffill()

columns = [
    f"{p}_{c}" if pandas.notna(c) else str(p)
    for p, c in zip(header_df.iloc[0], header_df.iloc[1])
]

df.columns = columns
df = df.replace(r"^\s*$", pandas.NA, regex=True)
df = df.dropna(how='all')

df['Ngày sinh'] = (
    pandas.to_datetime(df['Ngày sinh'], errors='coerce')
    .dt.strftime('%d/%m/%Y')
)

df.to_json(
    'KSK Le Loi 2025.json',
    orient='records',
    force_ascii=False,
    indent=4
)