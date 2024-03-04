import pandas as pd
import matplotlib.pyplot as plt
from data_clean import douban, rottentomatoes


# rottentomatoes analysis
# different time period
rottentomatoes["time_period"] = pd.cut(
    rottentomatoes["year"],
    bins=[1999, 2010, 2020, 2024],
    labels=["2000-2010", "2010-2020", "2020-2024"],
)
# summarize the rating distribution
# simplify the distribution by rounding the ratings to the nearest integer
rottentomatoes["rounded_score"] = rottentomatoes["rating"].round()
rating_distribution = (
    rottentomatoes.groupby(["time_period", "rounded_score"], observed=True)
    .size()
    .unstack(fill_value=0)
)
# calculate the average rating for each time period
average_rating_per_period = rottentomatoes.groupby("time_period", observed=True)[
    "rating"
].mean()

# plot the data
fig, ax1 = plt.subplots(figsize=(12, 8))
# bar chart: number of movies in each rating category
colors = ["lightblue", "skyblue", "blue"]
rating_distribution.plot(kind="bar", ax=ax1, width=0.8, color=colors, alpha=0.7)
ax1.set_xlabel("Time Period")
ax1.set_ylabel("Number of Ratings", color="b")
ax1.tick_params(axis="y", labelcolor="b")
ax1.set_title("Rottentomatoes Rating Distribution and Average Rating by Time Period")

# line chart: average rating for each time period
ax2 = ax1.twinx()
average_rating_per_period.plot(
    kind="line",
    ax=ax2,
    marker="o",
    color="darkblue",
    linewidth=2,
    markersize=8,
    label="Average Rating",
)
ax2.set_ylabel("Average Rating", color="r")
ax2.tick_params(axis="y", labelcolor="r")

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc="upper left")
plt.tight_layout()
plt.savefig("image/Rottentomatoes_time.jpg")


# douban analysis
# convert ratings to numeric values
rating_conversion = {"力荐": 5, "推荐": 4, "还行": 3, "较差": 2, "很差": 1}
douban["numeric_rating"] = douban["score"].map(rating_conversion)
# different time period
douban["time_period"] = pd.cut(
    douban["year"],
    bins=[1999, 2010, 2020, 2024],
    labels=["2000-2010", "2010-2020", "2020-2024"],
)
# summarize the rating distribution
rating_distribution = (
    douban.groupby(["time_period", "numeric_rating"], observed=True)
    .size()
    .unstack(fill_value=0)
)
# calculate the average rating for each time period
average_rating_per_period = douban.groupby("time_period", observed=True)[
    "numeric_rating"
].mean()

# plot the data
fig2, ax1 = plt.subplots(figsize=(12, 8))

# bar chart: number of movies in each rating category
colors = ["lightgreen", "mediumseagreen", "green"]
rating_distribution.plot(kind="bar", ax=ax1, width=0.8, color=colors, alpha=0.7)
ax1.set_xlabel("Time Period")
ax1.set_ylabel("Number of Ratings", color="g")
ax1.tick_params(axis="y", labelcolor="g")
ax1.set_title("Douban Rating Distribution and Average Rating by Time Period")

# line chart: average rating for each time period
ax2 = ax1.twinx()
average_rating_per_period.plot(
    kind="line",
    ax=ax2,
    marker="o",
    color="darkgreen",
    linewidth=2,
    markersize=8,
    label="Average Rating",
)
ax2.set_ylabel("Average Rating", color="r")
ax2.tick_params(axis="y", labelcolor="r")

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc="upper left")
plt.tight_layout()
plt.savefig("image/Douban_time.jpg")
plt.show()
