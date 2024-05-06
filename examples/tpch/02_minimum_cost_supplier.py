import pyarrow as pa
import datafusion
from datafusion import SessionContext, col, lit, functions as F

"""
The Minimum Cost Supplier Query finds, in a given region, for each part of a certain type and size, the supplier who
can supply it at minimum cost. If several suppliers in that region offer the desired part type and size at the same
(minimum) cost, the query lists the parts from suppliers with the 100 highest account balances. For each supplier,
the query lists the supplier's account balance, name and nation; the part's number and manufacturer; the supplier's
address, phone number and comment information.
"""

# This is the part we're looking for
size_of_interest = 15
type_of_interest = "BRASS"
region_of_interest = "EUROPE"

# Load the dataframes we need

ctx = SessionContext()

df_part = ctx.read_parquet("data/part.parquet").select_columns(
    "p_partkey", "p_mfgr", "p_type", "p_size"
)
df_supplier = ctx.read_parquet("data/supplier.parquet").select_columns(
    "s_acctbal",
    "s_name",
    "s_address",
    "s_phone",
    "s_comment",
    "s_nationkey",
    "s_suppkey",
)
df_partsupp = ctx.read_parquet("data/partsupp.parquet").select_columns(
    "ps_partkey", "ps_suppkey", "ps_supplycost"
)
df_nation = ctx.read_parquet("data/nation.parquet").select_columns(
    "n_nationkey", "n_regionkey", "n_name"
)
df_region = ctx.read_parquet("data/region.parquet").select_columns(
    "r_regionkey", "r_name"
)

# Filter down parts. Part names contain the type of interest, so we can use strpos to find where
# in the p_type column the word is. `strpos` will return 0 if not found, otherwise the position
# in the string where it is located.

df_part = df_part.filter(
    F.strpos(col("p_type"), lit(type_of_interest)) > lit(0)
).filter(col("p_size") == lit(size_of_interest))

# Filter regions down to the one of interest

df_region = df_region.filter(col("r_name") == lit(region_of_interest))

# Now that we have the region, find suppliers in that region. Suppliers are tied to their nation
# and nations are tied to the region.

df_nation = df_nation.join(df_region, (["n_regionkey"], ["r_regionkey"]), how="inner")
df_supplier = df_supplier.join(
    df_nation, (["s_nationkey"], ["n_nationkey"]), how="inner"
)

# Now that we know who the potential suppliers are for the part, we can limit out part
# supplies table down. We can further join down to the specific parts we've identified
# as matching the request

df = df_partsupp.join(df_supplier, (["ps_suppkey"], ["s_suppkey"]), how="inner")
df = df.join(df_part, (["ps_partkey"], ["p_partkey"]), how="inner")

# Locate the minimum cost across all suppliers. There are multiple ways you could do this,
# but one way is to create a window function across all suppliers, find the minimum, and
# create a column of that value. We can then filter down any rows for which the cost and
# minimum do not match.

# The default window frame as of 5/6/2024 is from unbounded preceeding to the current row.
# We want to evaluate the entire data frame, so we specify this.
window_frame = datafusion.WindowFrame("rows", None, None)
df = df.with_column(
    "min_cost", F.window("min", [col("ps_supplycost")], window_frame=window_frame)
)

df = df.filter(col("min_cost") == col("ps_supplycost"))

# From the problem statement, these are the values we wish to output

df = df.select_columns(
    "s_acctbal",
    "s_name",
    "n_name",
    "p_partkey",
    "p_mfgr",
    "s_address",
    "s_phone",
    "s_comment",
)

# Sort and display 100 entries
df = df.sort(
    col("s_acctbal").sort(),
    col("n_name").sort(),
    col("s_name").sort(),
    col("p_partkey").sort(),
)

df = df.limit(100)

# Show results

df.show()
