"""
Interface texts.

Each text has a key (e.g. "app_title"); t("app_title") returns it.
Texts may contain {placeholders} filled in by keyword: t("duplicates_warning", n=6).
Keeping texts in one place keeps the app code short and the wording consistent.
"""

TEXTS: dict[str, str] = {
    # --- App ------------------------------------------------------------------
    "app_title": "Power Query Cleaner",
    "app_caption": (
        "Upload a CSV or Excel file to see what needs fixing before you load it into Power BI. "
        "Built with Polish data formats in mind."
    ),
    "choose_file": "Choose a file",
    "no_file_hint": "No file at hand? Run `python run.py generate` and upload `data/orders_messy.csv`.",
    "load_error": "Could not read the file: {error}",
    "loaded_csv": "CSV file loaded · encoding: **{encoding}** · separator: **{separator}**",
    "loaded_excel": "Excel file loaded",
    "sep_;": "semicolon",
    "sep_,": "comma",
    "sep_\t": "tab",
    "sep_|": "pipe",
    "preview_raw": "Data preview (first 20 rows)",

    # --- Quality report -------------------------------------------------------
    "metric_rows": "Rows",
    "metric_columns": "Columns",
    "metric_duplicates": "Duplicate rows",
    "metric_issues": "Issues found",
    "columns_header": "Columns",
    "col_name": "Column",
    "col_type": "Detected type",
    "col_match": "Type match",
    "col_missing": "Missing",
    "col_unique": "Unique",
    "col_issues": "Issues",
    "col_examples": "Examples",
    "issues_header": "Issue details",
    "duplicates_warning": "The table contains {n} duplicate rows.",
    "no_issues": "No column issues found.",
    "download_report": "Download quality report (CSV)",
    "report_file": "quality_report.csv",
    "report_col_column": "column",
    "report_col_type": "type",
    "report_col_issue": "issue",

    # --- Data types -----------------------------------------------------------
    "type_integer": "integer",
    "type_decimal_comma": "decimal (comma)",
    "type_decimal_dot": "decimal (dot)",
    "type_date_dot": "date dd.mm.yyyy",
    "type_date_iso": "date yyyy-mm-dd",
    "type_date_slash": "date dd/mm/yyyy",
    "type_date_mixed": "date (mixed formats)",
    "type_postcode": "Polish postcode",
    "type_email": "e-mail",
    "type_text": "text",
    "type_empty": "empty",

    # --- Issue messages -------------------------------------------------------
    "issue_missing": "Missing values: {pct}",
    "issue_placeholders": "Missing data written as a word: {n} (e.g. {examples})",
    "issue_empty_column": "The column is completely empty",
    "issue_spaces": "Leading or trailing spaces: {n}",
    "issue_mixed_separators": "Numbers written with both a comma and a dot as the decimal separator",
    "issue_mixed_dates": "Dates in several formats: {formats}",
    "issue_type_mismatch": "Values not matching the type “{type}”: {n} (e.g. {examples})",
    "issue_comma_decimal": "Decimal comma - needs conversion with Polish regional settings (pl-PL)",
    "issue_outliers": "Outliers: {n} (e.g. {example})",
    "issue_negatives": "Negative values: {n} - check whether they are possible",
    "issue_variants": "Groups of values written in several ways: {n} (e.g. {examples})",
    "issue_nip_invalid": "Invalid NIP (Polish tax ID) numbers - wrong check digit or length: {n} (e.g. {examples})",
    "issue_nip_formats": "Different NIP formats ({n}): {formats}",

    # --- Cleaning plan --------------------------------------------------------
    "plan_header": "Cleaning plan",
    "plan_caption": "Select the steps you want to apply. The preview and the Power Query code update automatically.",
    "plan_outliers_note": (
        "Outliers (e.g. an order for 400 items) are deliberately not removed automatically - "
        "it may be an error or a genuine large order. That decision belongs to the analyst."
    ),
    "step_trim_label": "Remove leading and trailing spaces",
    "step_trim_reason": "Columns: {columns}",
    "step_nulls_label": "Turn blank cells and words like “brak”, “-”, “n/a” into missing values (null)",
    "step_nulls_reason": (
        "Power BI treats empty text and the word “brak” as a normal value - "
        "as null they are correctly skipped in averages and totals."
    ),
    "step_variants_label": "Unify spelling in column “{col}”",
    "step_variants_reason": "{n} replacements, e.g. {examples}. The most frequent spelling wins.",
    "step_numbers_int_label": "Convert “{col}” to whole numbers",
    "step_numbers_dec_label": "Convert “{col}” to decimal numbers",
    "step_numbers_reason": "Detected format: {type}. Thousands separators are removed and the text is converted using {culture} settings.",
    "step_dates_label": "Convert “{col}” to a date",
    "step_dates_reason": "Formats dd.mm.yyyy, dd/mm/yyyy and yyyy-mm-dd are recognised and converted to a single date type.",
    "step_nip_label": "Standardise the NIP format in “{col}”",
    "step_nip_reason": (
        "Dashes, spaces and the PL prefix are removed, leaving 10 digits. "
        "Invalid numbers (wrong check digit) need to be reviewed manually."
    ),
    "step_duplicates_label": "Remove duplicate rows",
    "step_duplicates_reason": "The raw data contains {n} duplicates. They are removed last, because cleaning can reveal more.",

    # --- Preview --------------------------------------------------------------
    "preview_header": "Preview: before and after",
    "rows_before": "Rows before",
    "rows_after": "Rows after",
    "tab_before": "Before cleaning",
    "tab_after": "After cleaning",

    # --- Power Query code ------------------------------------------------------
    "code_header": "Power Query code",
    "path_label": "File path on the computer running Power BI",
    "path_help": "Power BI needs to know where to load the original file from. Enter a Windows path.",
    "path_default_folder": "C:\\data\\",
    "download_code": "Download code (.pq)",
    "code_file": "cleaning.pq",
    "howto_header": "How to use this code in Power BI",
    "howto_body": (
        "1. In Power BI Desktop: **Get data → Blank query**.\n"
        "2. In the Power Query editor: **Advanced Editor**.\n"
        "3. Delete everything there and paste the code from this page.\n"
        "4. Click **Done**, then **Close & Apply**.\n\n"
        "When a new file with the same problems arrives, replace it and click **Refresh** - "
        "the cleaning runs automatically."
    ),

    # --- Step names in M code -------------------------------------------------
    "m_source": "Source",
    "m_headers": "Promoted headers",
    "m_trim": "Trimmed text",
    "m_nulls": "Blanks to null",
    "m_map": "Map: {col}",
    "m_unified": "Unified: {col}",
    "m_no_spaces": "No spaces: {col}",
    "m_number": "Number: {col}",
    "m_date": "Date: {col}",
    "m_nip": "NIP: {col}",
    "m_distinct": "Removed duplicates",
    "m_old_codes": "Old codes: {col}",
    "m_recoded": "Recoded: {col}",
    "m_wide_keys": "Column keys",
    "m_wide_data": "Data rows",
    "m_wide_renamed": "Renamed columns",
    "m_wide_unpivoted": "Unpivoted",
    "m_added": "Added: {col}",
    "m_types": "Changed types",

    # --- Native types (columns that already have a type, e.g. from Excel) -----
    "type_number_native": "number",
    "type_date_native": "date",

    # --- Wide layout (unpivot) ------------------------------------------------
    "col_name_date": "Date",
    "col_name_value": "Value",
    "wide_detected": (
        "**Wide layout detected:** the header takes {header_rows} rows and there are {n} value columns "
        "(one column per “{key}”). Power BI works best with a long table: one row per date and “{key}”."
    ),
    "wide_unpivot_label": "Unpivot the table (one row per date and “{key}”)",
    "wide_unpivot_note": (
        "Empty cells (no measurement) are skipped - Power Query's unpivot does the same, so the row counts match. "
        "Constant header rows are kept as columns: {constants}."
    ),

    # --- Code dictionary ------------------------------------------------------
    "dict_header": "Check codes against a dictionary (optional)",
    "dict_caption": (
        "Upload a reference file (e.g. station metadata) to check that every code in your data can be matched. "
        "Codes that don't match will silently disappear when you filter by city or region in Power BI."
    ),
    "dict_upload": "Dictionary file",
    "dict_sheet": "Sheet",
    "dict_data_col": "Column with codes in your data",
    "dict_key_col": "Column with current codes in the dictionary",
    "dict_old_col": "Column with old codes (optional)",
    "dict_none": "— none —",
    "dict_codes": "Codes in data",
    "dict_matched": "Found in dictionary",
    "dict_via_old": "Matched by old code",
    "dict_unmatched": "Not found",
    "dict_unmatched_list": (
        "Codes not found anywhere in the dictionary: {examples}. Rows with these codes will not match "
        "any entry in Power BI - check them manually or label them as unknown."
    ),
    "dict_all_ok": "Every code in the data matches the dictionary.",
    "step_recode_label": "Replace old codes with current ones in “{col}”",
    "step_recode_reason": "{n} codes appear in the dictionary only as old codes, e.g. {examples}.",
}


def t(key: str, /, **params) -> str:
    """Returns the text with {placeholders} filled in."""
    text = TEXTS[key]
    return text.format(**params) if params else text


def issues_count(n: int) -> str:
    """'1 issue' / '3 issues'."""
    return f"{n} issue" if n == 1 else f"{n} issues"
