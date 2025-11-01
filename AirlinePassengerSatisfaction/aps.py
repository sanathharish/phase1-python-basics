import argparse
import pandas as pd
import os
from utils.semiauto_missing_data_handler import handle_missing_data, classify_feature_importance
from utils.cleaning_utils import standerdize_column_names, normalize_text_columns
from utils.logger_setup import setup_logger  # We'll modify this to use the Logs folder


# ---------------------------
# TRAIN DATA CLEANING
# ---------------------------
def clean_train(train_path, output_path, logger, case_choice):
    logger.info("🔹 Starting TRAIN dataset cleaning...")

    df = pd.read_csv(train_path)
    logger.info(f"Loaded TRAIN dataset with shape: {df.shape}")

    # Standardize column names
    df = standerdize_column_names(df)
    logger.info("Standardized column names to snake_case")

    # Normalize text columns
    df = normalize_text_columns(df, case=case_choice)
    logger.info(f"Normalized text columns to {case_choice} case")

    # Identify important vs non-important features
    important, non_important = classify_feature_importance(df)
    logger.info(f"Identified {len(important)} important and {len(non_important)} non-important features")

    # Handle missing data
    df_cleaned, impute_info = handle_missing_data(df, important, non_important, logger=logger)

    # Save cleaned data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_cleaned.to_csv(output_path, index=False)
    logger.info(f"Saved cleaned TRAIN dataset to {output_path}")

    return df_cleaned, impute_info, important


# ---------------------------
# TEST DATA CLEANING
# ---------------------------
def clean_test(test_path, output_path, train_features, impute_info, logger, case_choice):
    logger.info("🔹 Starting TEST dataset cleaning...")

    df = pd.read_csv(test_path)
    logger.info(f"Loaded TEST dataset with shape: {df.shape}")

    # Standardize & normalize
    df = standerdize_column_names(df)
    df = normalize_text_columns(df, case=case_choice)

    # Ensure same features as train
    missing_cols = set(train_features) - set(df.columns)
    if missing_cols:
        logger.warning(f"Adding missing columns in TEST: {missing_cols}")
        for col in missing_cols:
            df[col] = None

    df = df[train_features]

    # Apply same imputation strategy
    for col, value in impute_info.items():
        if col in df.columns:
            df[col] = df[col].fillna(value)

    # Save cleaned test
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Saved cleaned TEST dataset to {output_path}")

    return df


# ---------------------------
# MAIN EXECUTION FLOW
# ---------------------------
def main():
    print("✨ Airline Passenger Satisfaction — Phase 1: Data Cleaning ✨")
    print("Options:")
    print("  1️⃣  Clean Train dataset")
    print("  2️⃣  Clean Test dataset (requires train first)")
    print("  3️⃣  Clean Both train and test datasets\n")

    choice = input("Select an option [1/2/3]: ").strip()
    if choice not in ["1", "2", "3"]:
        print("❌ Invalid choice.")
        return

    # Ask for log levels
    log_input = input("Enter log levels to include (INFO, WARNING, ERROR, DEBUG, ALL): ").upper().split(',')
    if "ALL" in log_input:
        log_levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
    else:
        log_levels = [lvl.strip() for lvl in log_input if lvl.strip()]

    # Ask case normalization
    case_choice = input("Choose case normalization for text columns (lower/title/upper): ").strip().lower()
    if case_choice not in ["lower", "upper", "title"]:
        print("⚠️ Invalid choice. Defaulting to 'title'.")
        case_choice = "title"

    # Ensure Logs folder exists before creating logger
    os.makedirs("Logs", exist_ok=True)

    # Setup logging — always inside Logs folder
    logger = setup_logger(os.path.join("Logs", "data_processing.log"), log_levels)
    logger.info(f"Logging initialized with levels: {log_levels}")

    train_path = r".\RawData\train.csv"
    test_path = r".\RawData\test.csv"
    train_out = r".\CleanedData\train_cleaned.csv"
    test_out = r".\CleanedData\test_cleaned.csv"

    # Execute based on user selection
    if choice == "1":
        df_train, impute_info, important = clean_train(train_path, train_out, logger, case_choice)
        logger.info("✅ TRAIN dataset cleaning complete.")

    elif choice == "2":
        logger.warning("⚠️ Ensure TRAIN dataset is cleaned first (for impute info and feature reference).")
        df_test = clean_test(test_path, test_out, [], {}, logger, case_choice)
        logger.info("✅ TEST dataset cleaning complete.")

    elif choice == "3":
        logger.info("🧹 Cleaning both train and test datasets...")

        df_train, impute_info, important = clean_train(train_path, train_out, logger, case_choice)
        df_test = clean_test(test_path, test_out, df_train.columns, impute_info, logger, case_choice)

        logger.info("✅ Both TRAIN and TEST datasets cleaned successfully!")

    logger.info("🎯 Data cleaning phase completed successfully!")


if __name__ == "__main__":
    main()
