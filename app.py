import streamlit as st
import requests

import pickle
import pandas as pd

movies_dict = pickle.load(open('pickle_files\movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
movies_list = movies['title'].tolist()

movies_cos_sim = pickle.load(open('pickle_files\movies_cos_sim.pkl', 'rb'))

print(movies)


def get_recommendations(movie):
    if movie in movies['title'].tolist():
        index = movies[movies['title']==movie].index[0]
        ascending_indices = movies_cos_sim[index].argsort()
        descending_indices = ascending_indices[::-1]
        return movies.iloc[descending_indices[1:21]]['title'].tolist()
    else:
        return 0




TMDB_API_KEY = 'API KEY HERE'


def fetch_movie_poster(movie_name):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
    response = requests.get(search_url).json()
    
    if response['results']:
        poster_path = response['results'][0]['poster_path']
        full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        return full_poster_url
    else:
        return None



st.title("Movie Recommendation System")

movie_name = st.selectbox("Enter a movie name:", movies_list)



if st.button("Get Recommendations"):
    if movie_name:
        recommendations = get_recommendations(movie_name)
        if recommendations:
            st.write("Here are some movies you might like:")
            cols = st.columns(5)
            for idx, movie in enumerate(recommendations):
                col = cols[idx % 5]
                with col:
                    st.write(movie)
                    poster_url = fetch_movie_poster(movie)
                    if poster_url:
                        st.image(poster_url, width=250)
                    else:
                        st.write("Poster not found.")
        else:
            st.write("No recommendations found. Please check the movie name and try again.")
    else:
        st.write("Please enter a movie name.")
