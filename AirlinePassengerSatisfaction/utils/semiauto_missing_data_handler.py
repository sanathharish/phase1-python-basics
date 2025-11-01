import pandas as pd
import logging
import traceback
import os

# ==========================================
# LOGGER SETUP
# ==========================================
def setup_logger(log_levels=None):
    """
    Sets up a logger that writes logs to Logs/data_cleaning.log file.
    Allows user to select multiple logging levels.
    """

    # Ensure Logs directory exists
    log_dir = "Logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "data_cleaning.log")

    # Default levels
    if log_levels is None:
        log_levels = ["INFO", "ERROR"]

    log_levels = [lvl.strip().upper() for lvl in log_levels]

    # Create or get logger
    logger = logging.getLogger("DataCleaningLogger")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()  # avoid duplicate logs

    # File handler (append mode)
    file_handler = logging.FileHandler(log_file, mode='a')
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Multiple level filtering
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR
    }

    if "ALL" in log_levels:
        selected_levels = list(level_map.values())
    else:
        selected_levels = [level_map[lvl] for lvl in log_levels if lvl in level_map]

    class MultiLevelFilter(logging.Filter):
        def filter(self, record):
            return record.levelno in selected_levels

    file_handler.addFilter(MultiLevelFilter())
    logger.addHandler(file_handler)

    print(f"📜 Logging started — levels: {', '.join(log_levels)} (Logs/{os.path.basename(log_file)})")

    return logger


# ==========================================
# FEATURE IMPORTANCE CLASSIFICATION
# ==========================================
def classify_feature_importance(df):
    """
    Automatically classifies features as 'important' or 'non-important' 
    based on missing data percentage.
    """
    missing = df.isnull().mean()
    important = [col for col, val in missing.items() if val < 0.1]
    non_important = [col for col, val in missing.items() if val >= 0.1]

    return important, non_important


# ==========================================
# MISSING DATA HANDLER
# ==========================================
def handle_missing_data(df, important_features, non_important_features, logger=None):
    """
    Handles missing data with user-guided or semi-automatic logic.
    Records imputation info for reuse.
    """
    impute_info = {}

    for col in df.columns:
        if df[col].isnull().sum() == 0:
            continue

        try:
            if col in important_features:
                if df[col].dtype in ['float64', 'int64']:
                    fill_value = df[col].median()
                    df[col] = df[col].fillna(fill_value)
                    impute_info[col] = fill_value
                    if logger: logger.info(f"[IMPUTE] {col}: median={fill_value}")
                else:
                    fill_value = df[col].mode()[0]
                    df[col] = df[col].fillna(fill_value)
                    impute_info[col] = fill_value
                    if logger: logger.info(f"[IMPUTE] {col}: mode='{fill_value}'")


            elif col in non_important_features:
                df.drop(columns=[col], inplace=True)
                impute_info[col] = "DROPPED"
                if logger: logger.warning(f"[DROP] {col} (too many missing values)")

        except Exception as e:
            if logger:
                logger.error(f"[ERROR] Failed on column '{col}' — {str(e)}")
                logger.error(traceback.format_exc())

    return df, impute_info
