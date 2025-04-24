from flask import Flask, render_template, request
import preprocces
import helpflask

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    user_list = []
    num_messages, words, num_media_messages, num_links = 0, 0, 0, 0
    selected_user = None
    monthly_timeline = daily_timeline = busy_day = busy_month = heatmap = None
    wordcloud = common_words = emoji_path = busy_users_path = None
    busy_user_df = emoji_df = None

    if request.method == "POST":
        uploaded_file = request.files['file']
        if uploaded_file:
            data = uploaded_file.read().decode("utf-8")
            df = preprocces.preprocess(data)

            user_list = df['users'].unique().tolist()
            user_list.sort()
            user_list.insert(0, "Overall")

            selected_user = request.form.get("selected_user", "Overall")

            # Basic stats
            num_messages, words, num_media_messages, num_links = helpflask.fetch_stats(selected_user, df)

            # Visualizations
            monthly_timeline = helpflask.monthly_timeline(selected_user, df)
            daily_timeline = helpflask.daily_timeline(selected_user, df)
            busy_day = helpflask.week_activity_map(selected_user, df)
            busy_month = helpflask.month_activity_map(selected_user, df)
            heatmap = helpflask.activity_heatmap(selected_user, df)
            wordcloud = helpflask.create_wordcloud(selected_user, df)
            common_words = helpflask.most_common_words(selected_user, df)

            # Emoji data + plot
            emoji_df, emoji_path = helpflask.emoji_helper(selected_user, df)

            # Only show most busy users when "Overall" is selected
            if selected_user == "Overall":
                _, busy_user_df, busy_users_path = helpflask.most_busy_userss(df)
            else:
                busy_user_df = None
                busy_users_path = None

    return render_template(
        "index.html",
        user_list=user_list,
        selected_user=selected_user,
        num_messages=num_messages,
        words=words,
        num_media_messages=num_media_messages,
        num_links=num_links,
        monthly_timeline="static/monthly_timeline.png" if monthly_timeline else None,
        daily_timeline="static/daily_timeline.png" if daily_timeline else None,
        busy_day="static/busy_day.png" if busy_day else None,
        busy_month="static/busy_month.png" if busy_month else None,
        heatmap="static/heatmap.png" if heatmap else None,
        wordcloud="static/wordcloud.png" if wordcloud else None,
        common_words="static/common_words.png" if common_words else None,
        emoji=emoji_path,
        emoji_df=emoji_df,
        busy_user_df=busy_user_df,
        busy_users_path=busy_users_path
    )

if __name__ == "__main__":
    app.run(debug=True)
