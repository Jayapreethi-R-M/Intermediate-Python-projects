# Project 2
# Import library and load dataset
import pandas as pd

artists_df = pd.read_table('artists.dat', encoding="utf-8", sep="\t", index_col='id')
user_artists_df = pd.read_csv('/content/user_artists.dat', encoding="utf-8", sep="\t")
user_friends_df = pd.read_csv('/content/user_friends.dat', encoding="utf-8", sep="\t")

# This chunk of code was to get an initial view of the data
artists_df.head()
artists_df.info()
user_artists_df.head()
user_artists_df.info()
user_friends_df.head()
user_friends_df.info()

# Query 1

# Calculate the total plays for each artists by grouping them by artist ID
artist_play_count = user_artists_df.groupby("artistID")["weight"].sum().reset_index()

# Sort them by descending order and select the top 10
top_artist = artist_play_count.sort_values(by="weight", ascending=False).head(10)

# Merge it with the artist information data to get names
top_artist = top_artist.merge(artists_df, left_on="artistID", right_on="id")

# Prints the result and removes the index nad header to fit the format
print("\n", "!" * 40, "\n\n", "1. Who are the top artists?", "\n")
print(top_artist[["name", "artistID", "weight"]].to_string(index=False, header=False))

# Query 2

# Group by artist, get the number of unique user IDs and rename the column in the new df
artist_listen_counts = user_artists_df.groupby("artistID")["userID"].nunique().reset_index()
artist_listen_counts = artist_listen_counts.rename(columns={"userID": "listener_count"})

# Sort them in descending order and filter out the top 10 results
top_listen_artists = artist_listen_counts.sort_values(by="listener_count", ascending=False).head(10)

# Use join function to get the artist ID
top_listen_artists = top_listen_artists.merge(artists_df, left_on="artistID", right_on="id")

# Prints the result and removes the index and header to fit the format
print("\n", "!" * 40, "\n\n", "2. What artists have the more listeners?", "\n")
print(top_listen_artists[["name", "artistID", "listener_count"]].to_string(index=False, header=False))

# Query 3

# Group by on userID and sum  to calculate total play counts for each user and rename in new df
user_play_counts = user_artists_df.groupby("userID")["weight"].sum().reset_index()
user_play_counts = user_play_counts.rename(columns={"weight": "total_play_count"})

# Sort by descending order and get the top 10 results
top_users = user_play_counts.sort_values(by="total_play_count", ascending=False).head(10)

# Prints the result and removes the index and header to fit the format
print("\n", "!" * 40, "\n\n", "3. Who are the top users?", "\n")
print(top_users.to_string(index=False, header=False))

# Query 4

# Reset index for merging
artists_df = artists_df.reset_index()

# Calculate total plays and total unique listener for each artist
artist_plays = user_artists_df.groupby('artistID')['weight'].sum().reset_index()
artist_listeners = user_artists_df.groupby('artistID')['userID'].nunique().reset_index()

# Merge total plays and listeners data & rename columns for differentiation
artist_stats = pd.merge(artist_plays, artist_listeners, on='artistID')
artist_stats.columns = ['artistID', 'tot_plays', 'tot_listeners']

# Add new column with average plays per listener
artist_stats['avg_plays_per_listener'] = artist_stats['tot_plays'] / artist_stats['tot_listeners']

# Merge artists stats with artist_df using 'id' column & rename columns for differentiation
artist_stats = pd.merge(artist_stats, artists_df[['id', 'name']], left_on='artistID', right_on='id')
artist_stats = artist_stats[['name', 'artistID', 'tot_plays', 'tot_listeners', 'avg_plays_per_listener']]

# Sort artists by top 10 average number of plays per listener
top_artists = artist_stats.sort_values(by='avg_plays_per_listener', ascending=False).head(10)

# Print the results
print("\n", "!" * 40, "\n\n", "4. What artists have the highest average number of plays per listener?", "\n")
print(top_artists.to_string(index=False, float_format='%.2f'))

# Query 5

# Following chunk of code is same as the previous question
# Calculate total plays and total unique listener for each artist
artist_plays = user_artists_df.groupby('artistID')['weight'].sum().reset_index()
artist_listeners = user_artists_df.groupby('artistID')['userID'].nunique().reset_index()

# Merge total plays and listeners data & rename columns for differentiation
artist_stats = pd.merge(artist_plays, artist_listeners, on='artistID')
artist_stats.columns = ['artistID', 'tot_plays', 'tot_listeners']

# Add new column with average plays per listener
artist_stats['avg_plays_per_listener'] = artist_stats['tot_plays'] / artist_stats['tot_listeners']

# New code
# Filter artists based on whether they have at least 50 unique listeners
artist_stats_50 = artist_stats[artist_stats['tot_listeners'] >= 50]

# Merge new artists_stats with artist df & rename columns for differentiation
artist_stats_50 = pd.merge( artist_stats_50, artists_df[['id', 'name']], left_on='artistID', right_on='id')
artist_stats_50 = artist_stats_50[['name', 'artistID', 'tot_plays', 'tot_listeners', 'avg_plays_per_listener']]

# Sort artists by top 10 average plays per listener
top_artists = artist_stats_50.sort_values(by='avg_plays_per_listener', ascending=False).head(10)

# Print the results
print("\n", "!" * 40, "\n\n", "5. What artists with at least 50 listeners have the highest average number of plays per listener?", "\n")
print(top_artists.to_string(index=False, float_format='%.2f'))

# Advanced Functionalities
# Query 6

# Create a list with userID grouped by artist ID
artist_listeners = user_artists_df.groupby('artistID')['userID'].apply(list)

# Converted the list to set so we can use it Jaccard similarity function
artist_listeners = {key: set(value) for key, value in artist_listeners.items()}

# Create a dictionary to map artist IDs to their names
artist_names = artists_df.set_index('id')['name'].to_dict()

# This function is to calculate Jaccard similarity
def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union

# This function is to calculate Jaccard similarity between two artists
def artist_sim(aid1, aid2):
    listeners_aid1 = artist_listeners.get(aid1, set())
    listeners_aid2 = artist_listeners.get(aid2, set())
    return jaccard_similarity(listeners_aid1, listeners_aid2)

# The list of artist pairs
test_pairs = [(735, 562), (735, 89), (735, 289), (89, 289), (89, 67), (67, 735)]

# Print output and use for loop to get similarity
print("\n", "!" * 40, "\n\n", "6. How similar are two artists?", "\n")
for aid1, aid2 in test_pairs:
    similarity_score = artist_sim(aid1, aid2)
    name1 = artist_names.get(aid1, f"Artist ID {aid1}")
    name2 = artist_names.get(aid2, f"Artist ID {aid2}")
    print(f"artist_sim({aid1},{aid2}) = {name1} and {name2}: Jaccard Index = {similarity_score:.3f}")


# Query 7

# Create mappings for user_friends_df and user_artists_df & converts them to dictionaries
friends_mapping = user_friends_df.groupby('userID')['friendID'].apply(set).to_dict()
user_artists_mapping = user_artists_df.groupby('userID')['artistID'].apply(set).to_dict()

# Calculate total plays for each userID and artistID
artist_plays_df = user_artists_df.groupby(['userID', 'artistID'])['weight'].sum().reset_index()

# Function to recommend artists based on friends
def Recommendations(user_id):
    # Get the friends and artists the user has listen to and converts them as sets
    friends = friends_mapping.get(user_id, set())
    user_artists_listened = user_artists_mapping.get(user_id, set())

    # Filter the artist_plays_df to include only the artists that the friends are listening to.
    friends_artists = artist_plays_df.loc[artist_plays_df['userID'].isin(friends)]

    # Use lambda function to filter out the artists the user is already listening to
    candidate_artists = friends_artists.loc[friends_artists['artistID'].apply(lambda x: x not in user_artists_listened)]

    # This code filters out candidate_artists who are listened to by at least two of the user's friends (here its filtered using twofr_artists).
    artist_friend_counts = candidate_artists.groupby('artistID')['userID'].nunique()
    twofr_artists = artist_friend_counts[artist_friend_counts >= 2].index
    candidate_artists = candidate_artists.loc[candidate_artists['artistID'].isin(twofr_artists)]

    # Calculates the average plays by the user's friends for each artist
    artist_avg_plays = candidate_artists.groupby('artistID')['weight'].mean().reset_index()
    artist_avg_plays.columns = ['artistID', 'avg_plays']

    # Sort artists by top 10 average plays
    top_artists_df = artist_avg_plays.sort_values(by='avg_plays', ascending=False).head(10)

    # Merge the top_artists_df with artist_df to get artist names
    top_artists_df = pd.merge(top_artists_df, artists_df[['id', 'name']], left_on='artistID', right_on='id')

    # Print top 10 artist recommendations
    print("\n", "!" * 40, "\n\n", "7. Recommend artists based on friends ?", "\n")
    print(f"Artists recommended to user {user_id}:")
    print(top_artists_df[['name', 'artistID', 'avg_plays']].to_string(index=False, float_format='%.2f'))

# Tested the function
Recommendations(2)
