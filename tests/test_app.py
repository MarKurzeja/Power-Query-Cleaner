"""
Automated tests. Run from the repository root:
    python run.py test

Each test checks one behaviour, so a failing test points straight to what broke.
"""

import sys
from pathlib import Path

import pandas as pd

# Allow importing modules from the python/ folder.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "python"))

from cleaning import apply_steps, steps_to_m, suggest_steps  # noqa: E402
from texts import TEXTS, issues_count  # noqa: E402
from loading import load_file  # noqa: E402
from profiling import is_valid_nip, profile_column, profile_dataframe  # noqa: E402

DATA = Path(__file__).resolve().parent.parent / "data" / "orders_messy.csv"


# --- NIP ----------------------------------------------------------------------
def test_valid_nip_in_different_formats():
    assert is_valid_nip("5260250274")
    assert is_valid_nip("526-025-02-74")
    assert is_valid_nip("PL5260250274")


def test_invalid_nip():
    assert not is_valid_nip("5260250275")   # wrong check digit
    assert not is_valid_nip("123")          # too short


# --- Interface texts ----------------------------------------------------------
def test_every_text_is_filled_in():
    for key, text in TEXTS.items():
        assert isinstance(text, str) and text.strip(), key


def test_issues_plural():
    assert issues_count(1) == "1 issue"
    assert issues_count(2) == "2 issues"


# --- Type detection -----------------------------------------------------------
def test_detects_polish_decimal_comma():
    col = profile_column(pd.Series(["1 234,56", "12,50", "7,00"], name="amount"))
    assert col.detected_type == "decimal_comma"


def test_detects_mixed_date_formats():
    col = profile_column(pd.Series(["05.03.2025", "2025-03-06", "07/03/2025"], name="date"))
    assert col.detected_type == "date_mixed"


def test_placeholder_words_are_not_type_errors():
    col = profile_column(pd.Series(["10,00", "brak", "20,00", "-"], name="amount"))
    assert col.type_match_pct == 1.0
    assert any(i.key == "issue_placeholders" for i in col.issues)


# --- End-to-end on the sample file --------------------------------------------
def _load():
    result = load_file(DATA.read_bytes(), DATA.name)
    return result, profile_dataframe(result.df)


def test_polish_csv_is_detected():
    result, _ = _load()
    assert result.encoding == "cp1250"
    assert result.separator == ";"


def test_cleaning_removes_duplicates_and_fixes_types():
    result, profile = _load()
    cleaned = apply_steps(result.df, suggest_steps(result.df, profile))
    assert len(cleaned) == len(result.df) - profile.duplicate_rows
    assert pd.api.types.is_datetime64_any_dtype(cleaned["order_date"])
    assert pd.api.types.is_float_dtype(cleaned["gross_amount"])
    assert cleaned["order_date"].notna().all()
    assert set(cleaned["city"].dropna()) <= {"Kraków", "Warszawa", "Gdańsk", "Wrocław", "Łódź", "Poznań"}


def test_power_query_code():
    result, profile = _load()
    steps = suggest_steps(result.df, profile)
    m = steps_to_m(steps, "C:\\data\\file.csv", "csv", result.encoding, result.separator)
    assert m.startswith("let") and m.rstrip().endswith('#"Removed duplicates"')
    assert "Encoding=1250" in m


# --- Wide layout (GIOŚ-style files) -------------------------------------------
def _wide_excel():
    """Small GIOŚ-style file: 3 header rows, stations in columns."""
    import io
    from datetime import datetime
    rows = [
        ["Kod stacji", "StA", "StB", "StC", "StOld"],
        ["Wskaźnik", "PM10", "PM10", "PM10", "PM10"],
        ["Jednostka", "ug/m3", "ug/m3", "ug/m3", "ug/m3"],
        [datetime(2024, 1, 1), 10.5, 20.0, None, 7.0],
        [datetime(2024, 1, 2), 55.0, 30.1, 12.0, 8.0],
    ]
    buf = io.BytesIO()
    pd.DataFrame(rows).to_excel(buf, header=False, index=False, sheet_name="PM10")
    return load_file(buf.getvalue(), "wide.xlsx")


def test_detects_wide_layout():
    from reshape import detect_wide_layout
    layout = detect_wide_layout(_wide_excel().raw)
    assert layout is not None
    assert layout.data_start == 3 and layout.key_label == "Kod stacji"
    assert layout.keys == ["StA", "StB", "StC", "StOld"]
    assert set(layout.constants) == {"Wskaźnik", "Jednostka"}


def test_normal_file_is_not_wide():
    from reshape import detect_wide_layout
    result, _ = _load()
    assert detect_wide_layout(result.raw) is None


def test_unpivot_skips_empty_cells():
    from reshape import detect_wide_layout, unpivot
    result = _wide_excel()
    long = unpivot(result.raw, detect_wide_layout(result.raw))
    assert list(long.columns) == ["Date", "Kod stacji", "Value", "Wskaźnik", "Jednostka"]
    assert len(long) == 7                     # 8 cells, one empty
    assert long["Wskaźnik"].eq("PM10").all()


def test_old_codes_are_matched():
    from reshape import check_codes
    lookup = check_codes(pd.Series(["StA", "StB", "StOld", "Ghost"]),
                         current=pd.Series(["StA", "StB", "StNew"]),
                         old=pd.Series([None, None, "StOld"]))
    assert lookup.matched == 2
    assert lookup.old_code_mapping == {"StOld": "StNew"}
    assert lookup.unmatched == ["Ghost"]


def test_wide_power_query_code():
    from reshape import detect_wide_layout
    result = _wide_excel()
    m = steps_to_m([], "C:\\data\\wide.xlsx", "excel", None, None,
                   sheet_name=result.sheet_name, layout=detect_wide_layout(result.raw))
    assert '[Item="PM10", Kind="Sheet"]' in m
    assert 'Table.UnpivotOtherColumns(#"Renamed columns", {"Date"}, "Kod stacji", "Value")' in m


def test_text_parameter_named_key():
    # Regression: a {key} placeholder (e.g. "Kod stacji") must not break t().
    from texts import t
    assert "Kod stacji" in t("wide_unpivot_label", key="Kod stacji")


def test_wide_layout_with_comma_numbers_as_text():
    # Some 2018 GIOŚ files store values as text with a decimal comma.
    import io
    from datetime import datetime
    from reshape import detect_wide_layout, unpivot
    rows = [
        ["Kod stacji", "StA", "StB", "StC"],
        ["Wskaźnik", "BaP", "BaP", "BaP"],
        [datetime(2018, 1, 1), "3,878", "0,5", None],
        [datetime(2018, 1, 2), "1,25", "14,566", "2"],
    ]
    buf = io.BytesIO()
    pd.DataFrame(rows).to_excel(buf, header=False, index=False, sheet_name="BaP")
    result = load_file(buf.getvalue(), "bap.xlsx")
    layout = detect_wide_layout(result.raw)
    assert layout is not None and layout.decimal_comma
    long = unpivot(result.raw, layout)
    assert long["Value"].tolist() == [3.878, 1.25, 0.5, 14.566, 2.0]
    m = steps_to_m([], "C:\\data\\bap.xlsx", "excel", None, None,
                   sheet_name=result.sheet_name, layout=layout)
    assert '{"Value", type number}}, "pl-PL")' in m


def test_excel_with_numeric_headers():
    # Regression: an Excel file with numeric headers (1, 2, 3) must not crash the app.
    import io
    buf = io.BytesIO()
    pd.DataFrame({1: ["a", "b"], 2: ["1,5", "2,5"]}).to_excel(buf, index=False)
    result = load_file(buf.getvalue(), "numbers.xlsx")
    assert list(result.df.columns) == ["1", "2"]
    suggest_steps(result.df, profile_dataframe(result.df))
