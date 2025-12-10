### PySpark Program Analysis

This PySpark program implements a fraud detection pipeline, mirroring the functionality of SAS programs. It imports, validates, cleans, and transforms transaction data, applies rule-based and machine learning (ML) scoring, and generates reports.

**Overall Structure:**

*   **Initialization:** Sets up a SparkSession with configurations for performance.
*   **Data Import and Validation:** Reads transaction data from a CSV, defines a schema, and validates data quality.
*   **Data Cleaning and Standardization:** Cleans and standardizes various transaction attributes like transaction type, merchant name, and country code.
*   **Feature Engineering:** Calculates new features such as velocity, amount deviation, time-based, and location-based features.
*   **Rule-Based Detection:** Applies a set of predefined rules to identify potentially fraudulent transactions.
*   **ML Scoring:** Simulates a logistic regression model to assign fraud scores.
*   **Score Combination and Reporting:** Combines rule-based and ML scores, generates a final fraud assessment, and produces reports.

**Detailed Analysis of Each Program/Function:**

1.  **`01_transaction_data_import.sas`**

    *   **Spark SQL Queries:** None
    *   **Analytical Operations:** None
    *   **Statistical Functions:** None
    *   **Machine Learning/Predictive Logic:** None
    *   **Report Generation and Formatting Logic:** None
    *   **Business Application:** Imports transaction data from a CSV file, which is the initial step for any analysis.

    ```python
    def import_transactions(spark: SparkSession, filepath: str, schema: T.StructType) -> T.DataFrame:
        """
        Imports transaction data from a CSV file.
        Maps to SAS macro IMPORT_TRANSACTIONS.
        """
        logger.info(f"Attempting to import data from {filepath}...")
        try:
            df = spark.read \
                .option("header", "true") \
                .schema(schema) \
                .csv(filepath)
            logger.info(f"Successfully imported {filepath}.")
            return df
        except Exception as e:
            logger.error(f"ERROR: Failed to import {filepath}. Error: {e}")
            sys.exit(1) # Abort program as in SAS %ABORT

    def validate_transactions(df: T.DataFrame) -> T.DataFrame:
        """
        Validates the imported transaction data by checking for missing values and invalid amounts.
        Filters out invalid records.
        Maps to SAS macro VALIDATE_DATA.
        """
        logger.info("Starting data validation...")

        total_count = df.count()
        logger.info(f"Total records before validation: {total_count}")

        # SAS: Create validation flags based on missing values and amount <= 0
        # PySpark: Use F.when().otherwise() for conditional logic
        validated_df = df.withColumn(
            "validation_status",
            F.when(F.col("transaction_id").isNull(), F.lit("MISSING_ID"))
            .when(F.col("customer_id").isNull(), F.lit("MISSING_CUSTOMER"))
            .when(F.col("amount").isNull(), F.lit("MISSING_AMOUNT"))
            .when(F.col("transaction_date").isNull(), F.lit("MISSING_DATE"))
            .when(F.col("amount") <= 0, F.lit("INVALID_AMOUNT"))
            .otherwise(F.lit("VALID"))
        )

        # SAS: Keep only valid records
        # PySpark: Use .filter()
        validated_df = validated_df.filter(F.col("validation_status") == "VALID")

        valid_count = validated_df.count()
        logger.info(f"Validated {valid_count} of {total_count} records.")

        return validated_df
    ```

    *   **Spark SQL Queries:** None
    *   **Analytical Operations:** `withColumn` (conditional logic using `F.when().otherwise()`) and `filter`
    *   **Statistical Functions:** None
    *   **Machine Learning/Predictive Logic:** None
    *   **Report Generation and Formatting Logic:** Logs the number of valid and invalid records.
    *   **Business Application:** Validates the imported data to ensure data quality by checking for missing values and invalid amounts.

2.  **`02_data_quality_cleaning.sas`**

    ```python
    def clean_transactions(df: T.DataFrame) -> T.DataFrame:
        """
        Cleans and standardizes transaction data.
        Maps to SAS macro CLEAN_TRANSACTIONS.
        """
        logger.info("Starting transaction data cleaning and standardization...")

        # SAS: Standardize transaction type (UPCASE, STRIP)
        # PySpark: F.upper(), F.trim()
        df = df.withColumn("transaction_type_clean", F.upper(F.trim(F.col("transaction_type"))))

        # SAS: Clean merchant name (PROPCASE, STRIP)
        # PySpark: F.initcap(), F.trim()
        df = df.withColumn("merchant_name_clean", F.initcap(F.trim(F.col("merchant_name"))))

        # SAS: Standardize country code (UPCASE, SUBSTR(country_code, 1, 2))
        # PySpark: F.upper(), F.substring()
        df = df.withColumn("country_code_clean", F.upper(F.substring(F.col("country_code"), 1, 2)))

        # SAS: Handle missing amounts - replace with 0
        # PySpark: F.coalesce()
        df = df.withColumn("amount", F.coalesce(F.col("amount"), F.lit(0)))

        # SAS: Convert transaction date to SAS date format (INPUT(transaction_date, YYMMDD10.))
        # PySpark: F.to_date()
        df = df.withColumn("transaction_date_sas", F.to_date(F.col("transaction_date"), "yyyy-MM-dd"))

        # SAS: Create transaction timestamp (DHMS(transaction_date_sas, HOUR(transaction_time), ...))
        # PySpark: F.to_timestamp() by concatenating date and time strings
        df = df.withColumn(
            "transaction_datetime",
            F.to_timestamp(F.concat_ws(" ", F.col("transaction_date"), F.col("transaction_time")), "yyyy-MM-dd HH:mm:ss")
        )

        logger.info("Transaction data cleaned and standardized.")
        return df

    def remove_duplicates(df: T.DataFrame, key_cols: list) -> T.DataFrame:
        """
        Removes duplicate records based on specified key columns.
        Maps to SAS macro REMOVE_DUPLICATES.
        """
        logger.info(f"Starting duplicate removal based on key: {key_cols}...")

        before_count = df.count()
        # SAS: PROC SORT DATA=&inds OUT=&outds NODUPKEY BY &key;
        # PySpark: .dropDuplicates()
        deduped_df = df.dropDuplicates(key_cols)
        after_count = deduped_df.count()

        dup_count = before_count - after_count
        logger.info(f"Removed {dup_count} duplicate records.")

        return deduped_df

    def handle_outliers(df: T.DataFrame, var_col: str, method: str = "WINSORIZE") -> T.DataFrame:
        """
        Handles outliers in a specified variable using Winsorization or removal.
        Maps to SAS macro HANDLE_OUTLIERS.
        """
        logger.info(f"Handling outliers in '{var_col}' using '{method}' method...")

        # SAS: PROC MEANS ... OUTPUT OUT=percentiles P1=p1 P99=p99;
        # PySpark: .approxQuantile()
        # Note: approxQuantile returns a list of values for the specified probabilities
        percentiles = df.approxQuantile(var_col, [0.01, 0.99], 0.01)
        p1_value = percentiles[0]
        p99_value = percentiles[1]

        logger.info(f"1st percentile for '{var_col}': {p1_value}")
        logger.info(f"99th percentile for '{var_col}': {p99_value}")

        if method.upper() == "WINSORIZE":
            # SAS: if &var < &p1_value then &var = &p1_value; else if &var > &p99_value then &var = &p1_value;
            # PySpark: F.when().otherwise()
            df = df.withColumn(
                var_col,
                F.when(F.col(var_col) < p1_value, p1_value)
                .when(F.col(var_col) > p99_value, p99_value)
                .otherwise(F.col(var_col))
            )
        elif method.upper() == "REMOVE":
            # SAS: if &var >= &p1_value AND &var <= &p99_value;
            # PySpark: .filter()
            df = df.filter((F.col(var_col) >= p1_value) & (F.col(var_col) <= p99_value))
        else:
            logger.warning(f"Unknown outlier handling method: {method}. No action taken.")

        logger.info(f"Outliers in '{var_col}' handled using '{method}' method.")
        return df
    ```

    *   **Spark SQL Queries:** None
    *   **Analytical Operations:** `withColumn`, `dropDuplicates`, and `filter`
    *   **Statistical Functions:** `approxQuantile`
    *   **Machine Learning/Predictive Logic:** None
    *   **Report Generation and Formatting Logic:** Logs information about the number of duplicate records removed and outlier handling.
    *   **Business Application:** Cleans and standardizes the data by cleaning transaction types, merchant names, country codes, handling missing amounts, and converting date and time formats. Removes duplicate transactions and handles outliers in the amount variable.

3.  **`03_feature_engineering.sas`**

    ```python
    def calculate_velocity_features(df: T.DataFrame, window_days: int = 7) -> T.DataFrame:
        """
        Calculates velocity features (transaction counts and amounts within a rolling window)
        and days since last transaction for each customer.
        Maps to SAS macro CALCULATE_VELOCITY.
        """
        logger.info(f"Calculating velocity features for a {window_days}-day window...")

        # SAS: PROC SORT DATA=&inds; BY customer_id transaction_date_sas transaction_time;
        # PySpark: Define window specification for customer-level ordering
        window_spec_customer = Window.partitionBy("customer_id").orderBy("transaction_datetime")

        # SAS: days_since_last_txn = transaction_date_sas - last_txn_date;
        # PySpark: F.lag() to get previous date, F.datediff()
        df = df.withColumn(
            "prev_transaction_date_sas",
            F.lag("transaction_date_sas", 1).over(window_spec_customer)
        ).withColumn(
            "days_since_last_txn",
            F.when(
                F.col("prev_transaction_date_sas").isNotNull(),
                F.datediff(F.col("transaction_date_sas"), F.col("prev_transaction_date_sas"))
            ).otherwise(None) # SAS uses '.' for missing, PySpark uses None
        ).drop("prev_transaction_date_sas")

        # SAS: Rolling window calculations (txn_count_&window_days.d, txn_amount_&window_days.d, avg_txn_amount_&window_days.d)
        # The SAS RETAIN logic with conditional reset is complex to map directly to standard Spark window functions.
        # We'll use a fixed-interval rolling window, which is a common and performant interpretation of "velocity" in Spark.
        # This window includes transactions from 'window_days' ago up to the current transaction.
        window_spec_rolling = Window.partitionBy("customer_id").orderBy("transaction_datetime").rangeBetween(
            -F.expr(f"INTERVAL {window_days} DAYS"), 0
        )

        df = df.withColumn(f"txn_count_{window_days}d", F.count("transaction_id").over(window_spec_rolling)) \
               .withColumn(f"txn_amount_{window_days}d", F.sum("amount").over(window_spec_rolling)) \
               .withColumn(f"avg_txn_amount_{window_days}d", F.avg("amount").over(window_spec_rolling))

        # Handle potential nulls from window functions for first records
        df = df.withColumn(f"txn_count_{window_days}d", F.coalesce(F.col(f"txn_count_{window_days}d"), F.lit(0)))
        df = df.withColumn(f"txn_amount_{window_days}d", F.coalesce(F.col(f"txn_amount_{window_days}d"), F.lit(0.0)))
        df = df.withColumn(f"avg_txn_amount_{window_days}d", F.coalesce(F.col(f"avg_txn_amount_{window_days}d"), F.lit(0.0)))

        logger.info("Velocity features calculated.")
        return df

    def calculate_amount_deviation(df: T.DataFrame) -> T.DataFrame:
        """
        Calculates amount deviation features (average amount, standard deviation, Z-score,
        and percentage deviation) for each customer.
        Maps to SAS macro CALCULATE_AMOUNT_DEVIATION.
        """
        logger.info("Calculating amount deviation features...")

        # SAS: PROC MEANS ... BY customer_id ... OUTPUT OUT=customer_stats ...
        # PySpark: .groupBy().agg()
        customer_stats_df = df.groupBy("customer_id").agg(
            F.avg("amount").alias("customer_avg_amount"),
            F.stddev("amount").alias("customer_std_amount"),
            F.count("transaction_id").alias("customer_txn_count")
        )

        # SAS: PROC SQL ... LEFT JOIN customer_stats ...
        # PySpark: .join() with broadcast hint for efficiency if customer_stats_df is small
        df = df.join(F.broadcast(customer_stats_df), on="customer_id", how="left")

        # SAS: CASE WHEN b.customer_std_amount > 0 THEN ... ELSE 0 END AS amount_zscore
        # PySpark: F.when().otherwise()
        df = df.withColumn(
            "amount_zscore",
            F.when(F.col("customer_std_amount") > 0,
                   (F.col("amount") - F.col("customer_avg_amount")) / F.col("customer_std_amount"))
            .otherwise(0.0)
        )

        # SAS: CASE WHEN b.customer_avg_amount > 0 THEN ... ELSE 0 END AS amount_pct_deviation
        # PySpark: F.when().otherwise()
        df = df.withColumn(
            "amount_pct_deviation",
            F.when(F.col("customer_avg_amount") > 0,
                   ((F.col("amount") - F.col("customer_avg_amount")) / F.col("customer_avg_amount")) * 100)
            .otherwise(0.0)
        )

        # Fill potential nulls from join for new customers or if no stats
        df = df.withColumn("customer_avg_amount", F.coalesce(F.col("customer_avg_amount"), F.lit(0.0)))
        df = df.withColumn("customer_std_amount", F.coalesce(F.col("customer_std_amount"), F.lit(0.0)))
        df = df.withColumn("customer_txn_count", F.coalesce(F.col("customer_txn_count"), F.lit(0)))

        logger.info("Amount deviation features calculated.")
        return df

    def create_time_features(df: T.DataFrame) -> T.DataFrame:
        """
        Creates time-based features from the transaction date and time.
        Maps to SAS macro CREATE_TIME_FEATURES.
        """
        logger.info("Creating time-based features...")

        # SAS: HOUR(transaction_time), WEEKDAY(transaction_date_sas), DAY(transaction_date_sas), MONTH(transaction_date_sas)
        # PySpark: F.hour(), F.dayofweek(), F.dayofmonth(), F.month()
        df = df.withColumn("txn_hour", F.hour(F.col("transaction_datetime"))) \
               .withColumn("txn_day_of_week", F.dayofweek(F.col("transaction_date_sas"))) \
               .withColumn("txn_day_of_month", F.dayofmonth(F.col("transaction_date_sas"))) \
               .withColumn("txn_month", F.month(F.col("transaction_date_sas")))

        # SAS: Create time-of-day categories (IF/ELSE IF)
        # PySpark: F.when().otherwise()
        df = df.withColumn(
            "time_of_day",
            F.when((F.col("txn_hour") >= 0) & (F.col("txn_hour") < 6), F.lit("NIGHT"))
            .when((F.col("txn_hour") >= 6) & (F.col("txn_hour") < 12), F.lit("MORNING"))
            .when((F.col("txn_hour") >= 12) & (F.col("txn_hour") < 18), F.lit("AFTERNOON"))
            .otherwise(F.lit("EVENING"))
        )

        # SAS: Create weekend flag (txn_day_of_week IN (1, 7))
        # PySpark: F.isin()
        df = df.withColumn("is_weekend", F.col("txn_day_of_week").isin([1, 7]).cast(T.IntegerType()))

        # SAS: Create unusual hour flag (txn_hour >= 0 AND txn_hour < 6)
        # PySpark: Boolean expression cast to IntegerType
        df = df.withColumn("is_unusual_hour", ((F.col("txn_hour") >= 0) & (F.col("txn_hour") < 6)).cast(T.IntegerType()))

        logger.info("Time-based features created.")
        return df

    def create_location_features(df: T.DataFrame) -> T.DataFrame:
        """
        Creates location-based features.
        Maps to SAS macro CREATE_LOCATION_FEATURES.
        """
        logger.info("Creating location-based features...")

        # SAS: PROC SQL ... GROUP BY country_code_clean ...
        # PySpark: .groupBy().agg()
        country_counts_df = df.groupBy("country_code_clean").agg(
            F.count("transaction_id").alias("country_txn_count")
        )

        # SAS: PROC SQL ... LEFT JOIN country_counts ...
        # PySpark: .join() with broadcast hint
        df = df.join(F.broadcast(country_counts_df), on="country_code_clean", how="left")

        # SAS: CASE WHEN b.country_txn_count < 10 THEN 1 ELSE 0 END AS is_rare_country
        # PySpark: F.when().otherwise()
        df = df.withColumn(
            "is_rare_country",
            F.when(F.col("country_txn_count") < 10, 1).otherwise(0)
        )

        # SAS: CASE WHEN a.country_code_clean NE 'US' THEN 1 ELSE 0 END AS is_international
        # PySpark: Boolean expression cast to IntegerType
        df = df.withColumn(
            "is_international",
            (F.col("country_code_clean") != "US").cast(T.IntegerType())
        )

        # Fill potential nulls from join
        df = df.withColumn("country_txn_count", F.coalesce(F.col("country_txn_count"), F.lit(0)))

        logger.info("Location-based features created.")
        return df
    ```

    *   **Spark SQL Queries:** None
    *   **Analytical Operations:** `withColumn`, `groupBy().agg()`, `join`, `Window.partitionBy().orderBy().rangeBetween()`
    *   **Statistical Functions:** `avg`, `stddev`, `count`
    *   **Machine Learning/Predictive Logic:** None
    *   **Report Generation and Formatting Logic:** None
    *   **Business Application:** Calculates features used for fraud detection. These include:
        *   **Velocity Features:** Calculates rolling transaction counts, amounts, and average transaction amounts over a 7-day window.
        *   **Amount Deviation Features:** Calculates average amount, standard deviation, Z-score, and percentage deviation for each customer.
        *   **Time-Based Features:** Extracts hour, day of the week, day of the month, and month from the transaction datetime. Creates flags for time of day, weekend, and unusual hours.
        *   **Location-Based Features:** Calculates transaction counts by country and creates flags for rare countries and international transactions.

4.  **`04_rule_based_detection.sas`**

    ```python
    def apply_fraud_rules(df: T.DataFrame) -> T.DataFrame:
        """
        Applies rule-based fraud detection logic and calculates a rule score.
        Maps to SAS macro APPLY_FRAUD_RULES.
        """
        logger.info("Applying fraud detection rules...")

        # Initialize rule flags and scores
        # In PySpark, we build up the score and triggered rules iteratively or in one go.
        # Let's create individual rule flags first, then sum scores and concatenate names.

        # Rule 1: High velocity (>10 transactions in 7 days)
        df = df.withColumn("rule_high_velocity", (F.col("txn_count_7d") > 10).cast(T.IntegerType()))
        # Rule 2: Large amount deviation (>3 standard deviations)
        df = df.withColumn("rule_amount_deviation", (F.abs(F.col("amount_zscore")) > 3).cast(T.IntegerType()))
        # Rule 3: High amount (>$5000)
        df = df.withColumn("rule_high_amount", (F.col("amount") > 5000).cast(T.IntegerType()))
        # Rule 4: Unusual hour transaction
        df = df.withColumn("rule_unusual_hour", (F.col("is_unusual_hour") == 1).cast(T.IntegerType()))
        # Rule 5: International transaction
        df = df.withColumn("rule_international", (F.col("is_international") == 1).cast(T.IntegerType()))
        # Rule 6: Rare country
        df = df.withColumn("rule_rare_country", (F.col("is_rare_country") == 1).cast(T.IntegerType()))
        # Rule 7: Multiple transactions in short time (less than 1 hour = 0.042 days)
        # Handle potential nulls in days_since_last_txn by treating them as not rapid succession
        df = df.withColumn("rule_rapid_succession",
                           (F.col("days_since_last_txn").isNotNull() & (F.col("days_since_last_txn") < 0.042)).cast(T.IntegerType()))
        # Rule 8: Round amount (multiple of 100 and >= 1000)
        df = df.withColumn("rule_round_amount",
                           ((F.col("amount") % 100 == 0) & (F.col("amount") >= 1000)).cast(T.IntegerType()))

        # Calculate rule_score by summing points for triggered rules
        df = df.withColumn("rule_score",
            (F.col("rule_high_velocity") * 25) +
            (F.col("rule_amount_deviation") * 30) +
            (F.col("rule_high_amount") * 20) +
            (F.col("rule_unusual_hour") * 15) +
            (F.col("rule_international") * 10) +
            (F.col("rule_rare_country") * 15) +
            (F.col("rule_rapid_succession") * 25) +
            (F.col("rule_round_amount") * 10)
        )

        # Concatenate triggered rule names
        rule_names = [
            F.when(F.col("rule_high_velocity") == 1, F.lit("HIGH_VELOCITY")),
            F.when(F.col("rule_amount_deviation") == 1, F.lit("AMOUNT_DEVIATION")),
            F.when(F.col("rule_high_amount") == 1, F.lit("HIGH_AMOUNT")),
            F.when(F.col("rule_unusual_hour") == 1, F.lit("UNUSUAL_HOUR")),
            F.when(F.col("rule_international") == 1, F.lit("INTERNATIONAL")),
            F.when(F.col("rule_rare_country") == 1, F.lit("RARE_COUNTRY")),
            F.when(F.col("rule_rapid_succession") == 1, F.lit("RAPID_SUCCESSION")),
            F.when(F.col("rule_round_amount") == 1, F.lit("ROUND_AMOUNT"))
        ]
        # Filter out None values from the array before concatenating
        df = df.withColumn("rule_triggered_array", F.array_remove(F.array(*rule_names), F.lit(None)))
        df = df.withColumn("rule_triggered", F.concat_ws(", ", F.col("rule_triggered_array")))
        df = df.drop("rule_triggered_array") # Clean up intermediate column

        # Calculate final rule-based risk level
        df = df.withColumn(
            "rule_risk_level",
            F.when(F.col("rule_score") >= 75, F.lit("CRITICAL"))
            .when(F.col("rule_score") >= 50, F.lit("HIGH"))
            .when(F.col("rule_score") >= 25, F.lit("MEDIUM"))
            .otherwise(F.lit("LOW"))
        )

        # Flag for investigation
        df = df.withColumn("is_suspicious", (F.col("rule_score") >= 50).cast(T.IntegerType()))

        logger.info("Fraud detection rules applied.")
        return df

    def generate_rule_alerts(df: T.DataFrame, threshold: int = 50) -> T.DataFrame:
        """
        Generates alerts based on the rule score and provides a summary.
        Maps to SAS macro GENERATE_RULE_ALERTS.
        """
        logger.info(f"Generating rule-based alerts with threshold >= {threshold}...")

        total_transactions = df.count()

        # SAS: Filter suspicious transactions (WHERE rule_score >= &threshold;)
        # PySpark: .filter()
        alerts_df = df.filter(F.col("rule_score") >= threshold)

        # SAS: Sort by risk score (PROC SORT BY DESCENDING rule_score transaction_date_sas;)
        # PySpark: .orderBy()
        alerts_df = alerts_df.orderBy(F.col("rule_score").desc(), F.col("transaction_date_sas").desc())

        # SAS: Count alerts by risk level (PROC FREQ TABLES rule_risk_level / NOCUM;)
        # PySpark: .groupBy().count()
        risk_level_counts = alerts_df.groupBy("rule_risk_level").count().orderBy("rule_risk_level")
        logger.info("Rule-Based Alerts by Risk Level:")
        risk_level_counts.show(truncate=False)

        alert_count = alerts_df.count()
        alert_rate = (alert_count / total_transactions * 100) if total_transactions > 0 else 0.0
        logger.info(f"Generated {alert_count} alerts ({alert_rate:.2f}% of transactions).")

        return alerts_df

    def rule_summary_report(df: T.DataFrame) -> T.DataFrame:
        """
        Creates a summary report of rule triggers.
        Maps to SAS macro RULE_SUMMARY_REPORT.
        """
        logger.info("Generating rule summary report...")

        # SAS: PROC SQL ... UNION ALL for each rule
        # PySpark: Aggregate individual rule flags and then union
        rule_summary_df = df.groupBy().agg(
            F.sum(F.col("rule_high_velocity")).alias("HIGH_VELOCITY"),
            F.sum(F.col("rule_amount_deviation")).alias("AMOUNT_DEVIATION"),
            F.sum(F.col("rule_high_amount")).alias("HIGH_AMOUNT"),
            F.sum(F.col("rule_unusual_hour")).alias("UNUSUAL_HOUR"),
            F.sum(F.col("rule_international")).alias("INTERNATIONAL"),
            F.sum(F.col("rule_rare_country")).alias("RARE_COUNTRY"),
            F.sum(F.col("rule_rapid_succession")).alias("RAPID_SUCCESSION"),
            F.sum(F.col("rule_round_amount")).alias("ROUND_AMOUNT")
        ).collect()[0].asDict() # Get the single row as a dictionary

        # Convert dictionary to a DataFrame for display
        summary_data = []
        for rule_name, trigger_count in rule_summary_df.items():
            summary_data.append((rule_name, trigger_count))

        summary_schema = T.StructType([
            T.StructField("rule_name", T.StringType(), True),
            T.StructField("trigger_count", T.LongType(), True)
        ])
        rule_summary_df = df.sparkSession.createDataFrame(summary_data, schema=summary_schema) \
            .orderBy(F.col("trigger_count").desc())

        logger.info("Fraud Rule Trigger Summary:")
        rule_summary_df.show(truncate=False)

        return rule_summary_df
    ```

    *   **Spark SQL Queries:** None
    *   **Analytical Operations:** `withColumn`, `filter`, `groupBy().count()`, `orderBy` and `F.array_remove`
    *   **Statistical Functions:** `sum`
    *   **Machine Learning/Predictive Logic:** None
    *   **Report Generation and Formatting Logic:**
        *   Generates a summary report of rule triggers.
        *   Logs the rule-based alerts by risk level and alert rate.
        *   Displays the rule summary report.
    *   **Business Application:** Implements rule-based fraud detection. Rules are applied based on the calculated features to generate a rule score. Based on the rule score, a risk level is assigned, and suspicious transactions are flagged.

5.  **`05_ml_scoring_model.sas`**

    ```python
    def prepare_ml_data(df: T.DataFrame) -> T.DataFrame:
        """
        Prepares the data for ML scoring by creating binary flags, normalizing continuous variables,
        and creating interaction features.
        Maps to SAS macro PREPARE_ML_DATA.
        """
        logger.info("Preparing data for ML scoring...")

        # SAS: Create binary flags for categorical variables
        df = df.withColumn("is_high_amount", (F.col("amount") > 1000).cast(T.IntegerType())) \
               .withColumn("is_very_high_amount", (F.col("amount") > 5000).cast(T.IntegerType()))

        # SAS: Normalize continuous variables (simple min-max scaling)
        # PySpark: Direct division
        df = df.withColumn("amount_normalized", F.col("amount") / 10000) # Assuming max ~$10k
        df = df.withColumn("txn_count_normalized", F.col("txn_count_7d") / 20) # Assuming max ~20

        # SAS: Handle missing values
        # PySpark: F.coalesce()
        df = df.withColumn("amount_zscore", F.coalesce(F.col("amount_zscore"), F.lit(0.0)))
        df = df.withColumn("days_since_last_txn", F.coalesce(F.col("days_since_last_txn"), F.lit(999.0)))

        # SAS: Create interaction features
        df = df.withColumn("amount_x_velocity", F.col("amount_normalized") * F.col("txn_count_normalized")) \
               .withColumn("amount_x_deviation", F.col("amount_normalized") * F.abs(F.col("amount_zscore")))

        logger.info("Data prepared for ML scoring.")
        return df

    def calculate_ml_score(df: T.DataFrame) -> T.DataFrame:
        """
        Calculates an ML-based fraud score using a simulated logistic regression model.
        Maps to SAS macro CALCULATE_ML_SCORE.
        """
        logger.info("Calculating ML fraud scores (simulated logistic regression)...")

        # Simulated logistic regression coefficients
        # SAS: logit_score = ...
        # PySpark: Direct arithmetic calculation
        df = df.withColumn(
            "logit_score",
            F.lit(-2.5) +                                   # Intercept
            F.lit(0.8) * F.col("amount_normalized") +       # Amount effect
            F.lit(0.6) * F.col("txn_count_normalized") +    # Velocity effect
            F.lit(0.4) * F.abs(F.col("amount_zscore")) +    # Deviation effect
            F.lit(0.5) * F.col("is_unusual_hour") +         # Time effect
            F.lit(0.3) * F.col("is_international") +        # Location effect
            F.lit(0.7) * F.col("amount_x_velocity") +       # Interaction 1
            F.lit(0.5) * F.col("amount_x_deviation") +